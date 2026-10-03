"""Model backends for the target organization. Returns parsed JSON plus token counts."""
import json
import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"


class ParseFailure(Exception):
    pass


def call_ollama(model: str, messages: list[dict], schema: dict, seed: int, temperature: float) -> dict:
    """One schema-constrained chat call. Retries once with seed+1000 on unparseable output."""
    last_raw = None
    for attempt, s in enumerate((seed, seed + 1000)):
        resp = httpx.post(OLLAMA_URL, json={
            "model": model, "messages": messages, "stream": False, "think": False,
            "format": schema, "options": {"temperature": temperature, "seed": s},
        }, timeout=600).json()
        raw = resp["message"]["content"]
        try:
            parsed = json.loads(raw)
            missing = [k for k in schema["required"] if k not in parsed]
            if missing:
                raise ValueError(f"missing {missing}")
            return {"output": parsed, "tokens_in": resp.get("prompt_eval_count", 0),
                    "tokens_out": resp.get("eval_count", 0), "retried": attempt > 0}
        except (ValueError, json.JSONDecodeError):
            last_raw = raw
    raise ParseFailure(last_raw)


# ---------------- Anthropic backend (Claude Haiku 4.5 subject) with a hard spend cap ----------------
import os  # noqa: E402
import pathlib  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEND_LEDGER = ROOT / "data" / "spend_ledger.jsonl"
# USD per million tokens (Claude API first-party rates); cache writes 1.25x input, cache reads 0.1x input.
PRICES = {"claude-haiku-4-5": {"in": 1.00, "out": 5.00}}
_lock = threading.Lock()
_client = None


class BudgetExceeded(Exception):
    pass


def spend_cap_usd() -> float:
    return float(os.environ.get("FALSIFY_SPEND_CAP_USD", "20"))


def spent_usd() -> float:
    if not SPEND_LEDGER.exists():
        return 0.0
    return sum(json.loads(l)["usd"] for l in SPEND_LEDGER.read_text().splitlines() if l.strip())


def _anthropic_client():
    global _client
    if _client is None:
        import anthropic
        if not os.environ.get("ANTHROPIC_API_KEY"):
            env = ROOT / ".env"
            if env.exists():
                for line in env.read_text().splitlines():
                    if line.startswith("ANTHROPIC_API_KEY="):
                        os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip()
        _client = anthropic.Anthropic(max_retries=4)
    return _client


def _strict(schema: dict) -> dict:
    """Anthropic structured outputs require additionalProperties: false on objects."""
    return {**schema, "additionalProperties": False}


def call_anthropic(model: str, messages: list[dict], schema: dict, seed: int, temperature: float) -> dict:
    """Schema-constrained call. `seed` is recorded only (the API has no sampling seed). Retries once on an
    unparseable reply. Every call's real cost is appended to data/spend_ledger.jsonl; calls are refused once the
    ledger reaches FALSIFY_SPEND_CAP_USD (default $20)."""
    price = PRICES[model]
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    convo = [{"role": m["role"], "content": m["content"]} for m in messages if m["role"] != "system"]
    last_raw = None
    for attempt in range(2):
        with _lock:
            if spent_usd() >= spend_cap_usd():
                raise BudgetExceeded(f"spend cap ${spend_cap_usd():.2f} reached (${spent_usd():.4f} spent)")
        r = _anthropic_client().messages.create(
            # anthropic SDK 1.x removed sampling kwargs from create(); Haiku 4.5 still honours temperature, and the
            # preregistered spec fixes it at 0.7, so it is passed through extra_body (SDK upgrade guide, Step 6).
            model=model, max_tokens=1024, system=system, messages=convo, extra_body={"temperature": temperature},
            cache_control={"type": "ephemeral"},
            output_config={"format": {"type": "json_schema", "schema": _strict(schema)}},
        )
        u = r.usage
        cache_w = getattr(u, "cache_creation_input_tokens", 0) or 0
        cache_r = getattr(u, "cache_read_input_tokens", 0) or 0
        usd = (u.input_tokens * price["in"] + cache_w * price["in"] * 1.25 + cache_r * price["in"] * 0.1
               + u.output_tokens * price["out"]) / 1e6
        with _lock:
            SPEND_LEDGER.parent.mkdir(exist_ok=True)
            with SPEND_LEDGER.open("a") as f:
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "model": model, "seed": seed,
                                    "in": u.input_tokens, "cache_w": cache_w, "cache_r": cache_r,
                                    "out": u.output_tokens, "usd": round(usd, 6)}) + "\n")
        raw = next((b.text for b in r.content if b.type == "text"), "")
        if r.stop_reason == "refusal":
            last_raw = f"REFUSAL: {raw}"
            continue
        try:
            parsed = json.loads(raw)
            missing = [k for k in schema["required"] if k not in parsed]
            if missing:
                raise ValueError(f"missing {missing}")
            return {"output": parsed, "tokens_in": u.input_tokens + cache_w + cache_r, "tokens_out": u.output_tokens,
                    "retried": attempt > 0, "usd": usd}
        except (ValueError, json.JSONDecodeError):
            last_raw = raw
    raise ParseFailure(last_raw)
