"""Calculator specifications, defined once and embedded wherever the reader needs the arithmetic.

The maths lives in ``theme/engine.js``; this is only the shape of the controls and the readout.
Defaults are the SkyWays case, so a calculator that has not been touched still shows a worked
example — which is what a reader without JavaScript sees, and what a printed page carries.
"""
from __future__ import annotations

from . import _kit as k

SPECS: dict[str, dict] = {
    "bar": dict(
        title="Derive the bar for one slice",
        sub="drag the two costs; the bar falls out",
        formula="N = damage ÷ saving · bar = N ÷ (N + 1)",
        inputs=[
            {"key": "saving", "label": "Value of one right answer ($)", "min": 1, "max": 100, "value": 9},
            {"key": "damage", "label": "Cost of one wrong answer ($)", "min": 1, "max": 1000, "value": 36},
            {"key": "holdcut", "label": "A person checks it first — damage falls to (%)",
             "min": 1, "max": 100, "value": 25}],
        outputs=[{"key": "n", "label": "Right answers one mistake undoes"},
                 {"key": "bar", "label": "Required accuracy", "big": True},
                 {"key": "barheld", "label": "…with a person in the loop"},
                 {"key": "verdict", "verdict": True,
                  "value": "Reachable. Prove it with the lower bound, not the score."}]),
    "value": dict(
        title="What the work is worth, net",
        sub="the two terms teams leave out are already in here",
        formula="net = cases × minutes × rate − run − review",
        inputs=[
            {"key": "cases", "label": "Cases per day", "min": 10, "max": 5000, "step": 10, "value": 240},
            {"key": "minutes", "label": "Minutes saved per case", "min": 1, "max": 60, "value": 8},
            {"key": "rate", "label": "Loaded cost per minute ($)", "min": 0.2, "max": 3, "step": 0.05, "value": 0.75},
            {"key": "runcost", "label": "Token cost per case ($)", "min": 0, "max": 5, "step": 0.05, "value": 0.6},
            {"key": "reviewshare", "label": "Share of cases a human checks (%)", "min": 0, "max": 100, "value": 30},
            {"key": "reviewmin", "label": "Minutes to check one", "min": 0, "max": 20, "step": 0.5, "value": 3}],
        outputs=[{"key": "gross", "label": "Gross saving"}, {"key": "run", "label": "Token cost"},
                 {"key": "review", "label": "Review load"},
                 {"key": "net", "label": "Net", "big": True},
                 {"key": "year", "label": "Per working year"},
                 {"key": "verdict", "verdict": True, "value": "Positive, with review under control."}]),
    "proof": dict(
        title="Has the bar actually been proven?",
        sub="the lower bound decides, never the score",
        formula="lower bound = p − 1.96√(p(1−p)/n) · Wilson under n=100",
        inputs=[{"key": "score", "label": "Score on this slice (%)", "min": 1, "max": 100, "step": 0.1, "value": 82},
                {"key": "n", "label": "Cases in the sample", "min": 5, "max": 2000, "step": 5, "value": 40},
                {"key": "bar", "label": "The bar for this slice (%)", "min": 1, "max": 99, "value": 80}],
        outputs=[{"key": "normal", "label": "Normal approximation"},
                 {"key": "wilson", "label": "Wilson"},
                 {"key": "bound", "label": "Lower bound in force", "big": True},
                 {"key": "verdict", "verdict": True, "value": "Not proven."}]),
    "evidence": dict(
        title="How long will the evidence take?",
        sub="you cannot learn faster than the sample arrives",
        formula="days = cases needed ÷ (traffic share × cases per day)",
        inputs=[{"key": "needed", "label": "Cases needed to prove the bar", "min": 20, "max": 2000,
                 "step": 10, "value": 500},
                {"key": "share", "label": "Share of live traffic (%)", "min": 1, "max": 100, "value": 5},
                {"key": "cases", "label": "Cases per day, this slice", "min": 5, "max": 2000,
                 "step": 5, "value": 240}],
        outputs=[{"key": "perday", "label": "Cases you will see"},
                 {"key": "days", "label": "Days of evidence", "big": True},
                 {"key": "verdict", "verdict": True, "value": "Workable."}]),
    "cache": dict(
        title="Does caching pay on this prompt?",
        sub="break-even is the second use, always",
        formula="cost = (w + 0.1 × (N − 1)) vs N · w = 1.25 (5 min) or 2 (1 hour)",
        inputs=[{"key": "uses", "label": "Times the prefix is reused", "min": 1, "max": 100, "value": 10},
                {"key": "window", "label": "Cache window", "type": "select", "value": "five",
                 "options": [("five", "Five minutes (write 1.25×)"), ("hour", "One hour (write 2×)")]}],
        outputs=[{"key": "withc", "label": "With caching"}, {"key": "without", "label": "Without"},
                 {"key": "saving", "label": "Saved", "big": True},
                 {"key": "verdict", "verdict": True, "value": "Pays."}]),
    "bill": dict(
        title="Decompose a bill that left its estimate",
        sub="four habits, and they multiply",
        formula="context × tier × cache × attempts · f is the cacheable share of spend",
        inputs=[{"key": "tokens_base", "label": "Tokens per call, baseline", "type": "number",
                 "value": 2100, "step": 50},
                {"key": "tokens_now", "label": "Tokens per call, now", "type": "number",
                 "value": 3360, "step": 50},
                {"key": "tier_base", "label": "Blended tier price, baseline", "min": 0.5, "max": 5,
                 "step": 0.05, "value": 1},
                {"key": "tier_now", "label": "Blended tier price, now", "min": 0.5, "max": 5,
                 "step": 0.05, "value": 1.5},
                {"key": "hit_base", "label": "Cache hit ratio, baseline (%)", "min": 0, "max": 100, "value": 71},
                {"key": "hit_now", "label": "Cache hit ratio, now (%)", "min": 0, "max": 100, "value": 9},
                {"key": "cacheshare", "label": "Share of spend in the cacheable prefix, f (%)",
                 "min": 5, "max": 100, "value": 40},
                {"key": "retry_base", "label": "Retries per conversation, baseline", "min": 0, "max": 5,
                 "step": 0.1, "value": 0.2},
                {"key": "retry_now", "label": "Retries per conversation, now", "min": 0, "max": 5,
                 "step": 0.1, "value": 0.7}],
        outputs=[{"key": "ctx", "label": "Context factor"}, {"key": "tier", "label": "Tier factor"},
                 {"key": "cache", "label": "Cache factor"}, {"key": "retry", "label": "Attempts factor"},
                 {"key": "product", "label": "The multiple", "big": True},
                 {"key": "verdict", "verdict": True, "value": "Fix in order of (factor − 1) ÷ days."}]),
    "queue": dict(
        title="What routing review by band does to the queue",
        sub="capacity is fixed by people; slots needed is a policy choice",
        formula="queue = slots needed ÷ slots available per day",
        inputs=[{"key": "r45", "label": "Changes touching money or identity (R4–R5)", "min": 0, "max": 30, "value": 2},
                {"key": "r23", "label": "Changes touching real work (R2–R3)", "min": 0, "max": 30, "value": 3},
                {"key": "r1", "label": "Read-only or docs changes (R1)", "min": 0, "max": 30, "value": 4},
                {"key": "capacity", "label": "Review slots available per day", "min": 0.5, "max": 20,
                 "step": 0.5, "value": 4.5}],
        outputs=[{"key": "slotsall", "label": "Slots, two readers on everything"},
                 {"key": "slotsrouted", "label": "Slots, routed by band"},
                 {"key": "before", "label": "Queue before"},
                 {"key": "after", "label": "Queue after", "big": True},
                 {"key": "verdict", "verdict": True,
                  "value": "Capacity is fixed by people. Slots needed is a policy choice."}]),
}


def render(name: str) -> str:
    s = SPECS[name]
    return k.calc(name, s["title"], s["sub"], s["inputs"], s["outputs"], s["formula"])
