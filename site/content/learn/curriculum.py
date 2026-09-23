"""The order of the tutorial. Change it here and every sidebar, prev/next link, track page, sitemap
entry and llms.txt line follows. A lesson file that is not listed, or a listed lesson with no file,
stops the build — see site/pages/learn.py.

Titles are chosen for the query a practitioner actually types (checked against live results in
September 2026), then made more specific than what already ranks. Track ids are URL paths:
/learn/<id>/. Lesson slugs are flat, /learn/<slug>/, so a lesson can move track without its URL
changing.
"""

START = "start-here"

TRACKS = [
    {
        "id": "getting-started",
        "title": "Getting started",
        "short": "Start",
        "wiki": "Tutorial-Getting-Started",
        "blurb": "What the agentic PDLC is, in one sitting, and how to get the most out of the lessons "
                 "that follow.",
        "promise": "Read these two first",
        "lessons": [
            "what-is-the-agentic-pdlc",
            "how-this-tutorial-works",
        ],
    },
    {
        "id": "fundamentals",
        "title": "Agentic PDLC fundamentals",
        "short": "Fundamentals",
        "wiki": "Tutorial-Fundamentals",
        "blurb": "The four phases, the one hard gate, the eight loops and the evidence that crosses each "
                 "hand-off — the model every other track builds on.",
        "promise": "The spine, phase by phase",
        "lessons": [
            "evolution-of-the-pdlc",
            "why-agentic-ai-projects-fail",
            "p0-frame",
            "p1-design-and-spec",
            "the-hard-gate",
            "p2-build-and-prove",
            "p3-run-and-learn",
            "the-eight-loops",
            "the-evidence-pack",
        ],
    },
]

# The rest of the plan, in the order it will be written. Not read by the build.
PLANNED = {
    "methods": ("Methods decoded: AI-DLC, AIDD, BMAD and spec-driven development", [
        "ai-dlc-vs-aidd-vs-agentic-sdlc", "what-is-ai-dlc", "what-is-aidd", "what-is-the-bmad-method",
        "what-is-spec-driven-development", "one-lifecycle-for-every-method",
        "how-much-process-does-a-change-need"]),
    "delivery": ("Running delivery: boards, bolts and speed", [
        "how-to-run-an-agentic-ai-project", "bolts-vs-sprints", "agentic-kanban-board", "cut-delivery-time",
        "review-ai-generated-code", "how-accurate-must-an-ai-agent-be", "prove-ai-accuracy",
        "shadow-mode-and-cutover", "ai-agent-costs", "ai-guardrails-that-hold", "ai-governance-gates",
        "ai-drift-monitoring", "ai-incident-postmortem"]),
    "roles": ("By role: how each discipline works in the agentic PDLC", [
        "agentic-pdlc-for-product-managers", "agentic-pdlc-for-program-managers",
        "agentic-pdlc-for-solution-architects", "agentic-pdlc-for-engineers",
        "ai-dlc-for-forward-deployed-engineers", "agentic-pdlc-for-qa", "agentic-pdlc-for-devops",
        "agentic-pdlc-for-business-sponsors", "agentic-ai-for-executives"]),
    "organisation": ("Teams and organisation", [
        "team-structure-for-agentic-ai", "measure-ai-productivity", "ai-delivery-maturity-model",
        "rolling-out-agentic-delivery"]),
    "practice": ("Practice: a case study, simulations and exercises", [
        "skyways-case-study", "a-week-in-agentic-delivery", "agentic-delivery-simulator",
        "agentic-pdlc-exercises"]),
}
