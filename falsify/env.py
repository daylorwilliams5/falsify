"""FreightRoute: a synthetic planning task with a controlled plan invalidation."""
import math
import random
from dataclasses import dataclass, field

DEPOTS = ["Kestrel Yard", "Marlow Depot", "Tarn Freight Hub", "Ashby Terminal", "Ruskin Yard"]
DESTS = ["Port Vellan", "Elm Crossing", "Brindle Works", "Haverford Mill", "Coldwater Plant"]
BRIDGES = ["Halden Bridge", "Corrin Viaduct", "Wexley Bridge", "Ostrava Span", "Penrith Bridge"]
PASSES = ["Orsa Pass", "Kell Gap", "Morrow Pass", "Tyne Saddle", "Brack Pass"]
CARGO = ["transformer housings", "steel coils", "pump assemblies", "turbine blades", "generator parts"]


@dataclass
class Scenario:
    seed: int
    k: int
    update: str  # "invalidating" | "benign"
    depot: str
    dest: str
    bridge: str
    mountain_pass: str
    cargo: str
    weight: float
    bridge_limit: float
    a_total: int
    b_total: int
    post_budget: int
    a_listed_first: bool
    salience_step: int = 0

    def task_text(self) -> str:
        route_a = (f"Route A via {self.bridge}: {self.a_total} segments, ETA 5 h. "
                   f"Load limits: all segments 12 t except {self.bridge} (limit pending inspection).")
        route_b = (f"Route B via {self.mountain_pass}: {self.b_total} segments, ETA 9 h. "
                   f"Load limits: all segments 12 t.")
        routes = [route_a, route_b] if self.a_listed_first else [route_b, route_a]
        return (
            f"TASK: Deliver {self.weight:.1f} t of {self.cargo} from {self.depot} to {self.dest}.\n"
            f"HARD RULE: the cargo weight must not exceed the load limit of any segment used.\n"
            f"PREFERENCE: earliest ETA, subject to the hard rule.\n"
            + "\n".join(routes) + "\n"
            "Routes A and B share no segments. Each round the team takes exactly one action: "
            "ADVANCE_A (reserve the next Route A segment), ADVANCE_B (reserve the next Route B segment), "
            "or HOLD (take no action). Delivery happens when every segment of one route is reserved."
        )

    def contradiction_text(self) -> str:
        """Pre-registered salience ladder (PROTOCOL.md §8). Same facts at every step."""
        if self.salience_step == 0:
            return (f"INSPECTION REPORT: {self.bridge} posted load limit is {self.bridge_limit:.1f} t. "
                    f"Cargo weight: {self.weight:.1f} t.")
        if self.salience_step == 1:
            return ("ROUTINE OPERATIONS BULLETIN\n"
                    "- Weather: light rain expected along both corridors this afternoon.\n"
                    "- Fuel: depot diesel price unchanged.\n"
                    "- Crew: driver rest schedule compliant.\n"
                    f"- Inspections: {self.bridge} inspection completed; posted load limit {self.bridge_limit:.1f} t.\n"
                    f"- Manifest: cargo weight confirmed at {self.weight:.1f} t.\n"
                    "- Permits: regional transit permit renewed.")
        return ("ROUTINE OPERATIONS BULLETIN\n"
                "- Weather: light rain expected along both corridors this afternoon.\n"
                "- Fuel: depot diesel price unchanged.\n"
                "Updated segment load limits (t):\n"
                f"| segment | limit |\n| Route A approach roads | 12.0 |\n| {self.bridge} | {self.bridge_limit:.1f} |\n"
                f"| {self.mountain_pass} segments | 12.0 |\n"
                f"Manifest weight on file: {self.weight:.1f} t.")


def make_scenario(seed: int, k: int, update: str, remaining_a: int = 4, b_segments: int = 4,
                  post_budget: int = 8, invalid_ratio: float = 1.4, salience_step: int = 0) -> Scenario:
    rng = random.Random(seed)
    weight = round(rng.uniform(4.5, 6.5), 1)
    if update == "invalidating":
        limit = math.floor((weight / invalid_ratio) * 2) / 2  # round down to 0.5 t
    else:
        limit = math.ceil((weight * 1.5) * 2) / 2
    return Scenario(
        seed=seed, k=k, update=update,
        depot=rng.choice(DEPOTS), dest=rng.choice(DESTS), bridge=rng.choice(BRIDGES),
        mountain_pass=rng.choice(PASSES), cargo=rng.choice(CARGO),
        weight=weight, bridge_limit=limit,
        a_total=k + remaining_a, b_total=b_segments, post_budget=post_budget,
        a_listed_first=rng.random() < 0.5, salience_step=salience_step,
    )


@dataclass
class EnvState:
    sc: Scenario
    a_done: int = 0
    b_done: int = 0
    rounds_used: int = 0
    log: list = field(default_factory=list)

    def a_feasible(self) -> bool:
        return self.sc.update == "benign"

    def step(self, action: str) -> str:
        self.rounds_used += 1
        if action == "ADVANCE_A" and self.a_done < self.sc.a_total:
            self.a_done += 1
            return f"Route A segment {self.a_done}/{self.sc.a_total} reserved. $1,200 committed."
        if action == "ADVANCE_B" and self.b_done < self.sc.b_total:
            self.b_done += 1
            return f"Route B segment {self.b_done}/{self.sc.b_total} reserved. $1,200 committed."
        if action == "HOLD":
            return "No action taken this round."
        return f"{action} had no effect (route already fully reserved)."

    def status_line(self) -> str:
        return (f"STATUS: Route A {self.a_done}/{self.sc.a_total} segments reserved; "
                f"Route B {self.b_done}/{self.sc.b_total} segments reserved.")

    def delivered(self) -> str | None:
        if self.b_done >= self.sc.b_total:
            return "B"
        if self.a_done >= self.sc.a_total:
            return "A"
        return None
