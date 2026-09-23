"""Presentation hints per step: which figure to draw, which calculator to embed.

These live apart from the prose files on purpose. A step's Python module is about what the role
does; this is about how one step is shown. Keeping them separate means a content edit never has to
step around markup, and a presentation change never touches a sentence.

A step earns a figure only where the *shape* is the lesson, and a calculator only where the reader
is about to do arithmetic. Most steps get neither, which is what keeps the ones that do meaningful.

    (role id, step id) -> {"figure": <name in pages/figures.py>, "calc": <name in theme/engine.js>}
"""

ENRICH = {
    # ---- product manager -------------------------------------------------
    ("product-manager", "frame"): {"calc": "value"},
    ("product-manager", "specify"): {"figure": "bar_sheet", "calc": "bar"},
    ("product-manager", "plan"): {"figure": "bolt_days"},
    ("product-manager", "launch"): {"figure": "shadow_widen", "calc": "evidence"},
    ("product-manager", "learn"): {"figure": "two_numbers"},

    # ---- solution architect ----------------------------------------------
    ("solution-architect", "bound"): {"figure": "authority_ladder"},
    ("solution-architect", "detail"): {"figure": "chain"},
    ("solution-architect", "evolve"): {"figure": "cache_prefix", "calc": "cache"},

    # ---- engineering lead -------------------------------------------------
    ("engineering", "gate"): {"figure": "authority_ladder"},
    ("engineering", "ship"): {"figure": "bolt_days"},
    ("engineering", "operate"): {"figure": "cache_prefix", "calc": "cache"},

    # ---- QA lead -----------------------------------------------------------
    ("qa", "define"): {"figure": "bar_sheet", "calc": "bar"},
    ("qa", "measure"): {"calc": "proof"},
    ("qa", "shadow"): {"figure": "shadow_widen", "calc": "evidence"},

    # ---- DevOps and platform ----------------------------------------------
    ("devops", "pipeline"): {"calc": "queue"},
    ("devops", "observe"): {"figure": "bill_factors", "calc": "bill"},
}


# ---------------------------------------------------------------------------
# Which PDLC phase each step belongs to.
#
# The phases are the spine (see the wiki's The-Agentic-PDLC); the role steps are
# the walk. This is the only place the two are joined, so the site boards, the
# wiki journeys and the role pages cannot drift apart. The build fails if any
# step is missing, named twice, or given a phase that does not exist.
# ---------------------------------------------------------------------------
PDLC = {
    "product-manager": {"discover": "P0", "qualify": "P0", "frame": "P0",
                        "specify": "P1", "plan": "P1",
                        "gate": "P2",
                        "launch": "P3", "learn": "P3"},
    "solution-architect": {"elicit": "P0", "constrain": "P0",
                           "map": "P1", "shape": "P1", "decide": "P1",
                           "bound": "P1", "detail": "P1",
                           "evolve": "P3"},
    "engineering": {"prepare": "P1",
                    "slice": "P2", "floor": "P2", "layer": "P2",
                    "gate": "P2", "harness": "P2", "ship": "P2",
                    "operate": "P3"},
    "qa": {"define": "P1", "curate": "P1",
           "check": "P2", "harness": "P2", "measure": "P2",
           "attack": "P2", "shadow": "P2",
           "watch": "P3"},
    "devops": {"baseline": "P0",
               "access": "P1", "environments": "P1",
               "pipeline": "P2", "deploy": "P2",
               "observe": "P3", "protect": "P3", "recover": "P3"},
}

# A phase a role produces nothing in is not a gap in the manual — it is the
# point. These are the two most expensive habits in agentic delivery, named.
PDLC_ABSENT = {
    ("engineering", "P0"): "Not on the clock — reads the brief, starts nothing",
    ("qa", "P0"): "Asks one question: what will <i>right</i> mean, and who says so?",
    ("solution-architect", "P2"): "Answers against the map; does not re-open it",
}
