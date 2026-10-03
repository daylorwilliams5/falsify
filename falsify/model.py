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
