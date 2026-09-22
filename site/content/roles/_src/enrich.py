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
