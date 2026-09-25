"""The order of the tutorial. Change it here and every sidebar, prev/next link, track page, sitemap
entry and llms.txt line follows. A lesson file that is not listed, or a listed lesson with no file,
stops the build: see site/pages/learn.py.

Titles are chosen for the query a practitioner actually types (the first four tracks' titles were
checked against live results in September 2026), then made more specific than what already ranks.
Track ids are URL paths: /learn/<id>/. Lesson slugs are flat, /learn/<slug>/, so a lesson can move
track without its URL changing.
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
                 "hand-off: the model every other track builds on.",
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
    {
        "id": "methods",
        "title": "Methods decoded",
        "short": "Methods",
        "wiki": "Tutorial-Methods-Decoded",
        "blurb": "AWS AI-DLC, AIDD, the BMAD Method and spec-driven development: what each one is, who "
                 "coined it, where it sits on the four phases, and what it leaves for you to decide.",
        "promise": "AI-DLC, AIDD, BMAD and SDD, placed",
        "lessons": [
            "ai-dlc-vs-aidd-vs-agentic-sdlc",
            "what-is-ai-dlc",
            "what-is-aidd",
            "what-is-the-bmad-method",
            "what-is-spec-driven-development",
            "one-lifecycle-for-every-method",
            "how-much-process-does-a-change-need",
        ],
    },
    {
        "id": "delivery",
        "title": "Running delivery",
        "short": "Delivery",
        "wiki": "Tutorial-Running-Delivery",
        "blurb": "The practical core: the twelve steps, bolts and boards, cutting delivery time, reviewing "
                 "AI-written code, setting and proving the bar, launching safely, cost, guardrails, "
                 "governance, drift and postmortems.",
        "promise": "Boards, bolts, launches and the bill",
        "lessons": [
            "how-to-run-an-agentic-ai-project",
            "bolts-vs-sprints",
            "agentic-kanban-board",
            "cut-delivery-time",
            "review-ai-generated-code",
            "how-accurate-must-an-ai-agent-be",
            "prove-ai-accuracy",
            "shadow-mode-and-cutover",
            "ai-agent-costs",
            "ai-guardrails-that-hold",
            "ai-governance-gates",
            "ai-drift-monitoring",
            "ai-incident-postmortem",
        ],
    },
    {
        "id": "roles",
        "title": "By role",
        "short": "By role",
        "wiki": "Tutorial-By-Role",
        "blurb": "How each discipline works in the agentic PDLC, product, programme, architecture, "
                 "engineering, forward-deployed, QA, DevOps, the sponsor and the executive: what "
                 "changes, what is theirs, and what is not.",
        "promise": "Your job, phase by phase",
        "lessons": [
            "agentic-pdlc-for-product-managers",
            "agentic-pdlc-for-program-managers",
            "agentic-pdlc-for-solution-architects",
            "agentic-pdlc-for-engineers",
            "ai-dlc-for-forward-deployed-engineers",
            "agentic-pdlc-for-qa",
            "agentic-pdlc-for-devops",
            "agentic-pdlc-for-business-sponsors",
            "agentic-ai-for-executives",
        ],
    },
    {
        "id": "organisation",
        "title": "Teams and organisation",
        "short": "Organisation",
        "wiki": "Tutorial-Teams-and-Organisation",
        "blurb": "How to structure teams, measure productivity without fooling yourself, assess maturity "
                 "by controls rather than tools, and roll the method out in ninety days.",
        "promise": "Structure, measures and rollout",
        "lessons": [
            "team-structure-for-agentic-ai",
            "measure-ai-productivity",
            "ai-delivery-maturity-model",
            "rolling-out-agentic-delivery",
        ],
    },
    {
        "id": "practice",
        "title": "Practice",
        "short": "Practice",
        "wiki": "Tutorial-Practice",
        "blurb": "The SkyWays case study in thirteen episodes, the operating rhythm from daily to "
                 "quarterly, the simulator, and twelve exercises with worked answers.",
        "promise": "A case, a simulator, twelve problems",
        "lessons": [
            "skyways-case-study",
            "agentic-delivery-cadence",
            "agentic-delivery-simulator",
            "agentic-pdlc-exercises",
        ],
    },
    {
        "id": "interviews",
        "title": "Interviews and careers",
        "short": "Interviews",
        "wiki": "Tutorial-Interviews-and-Careers",
        "blurb": "What a forward deployed engineer does, six frameworks for answering AI interview "
                 "questions, and deep question banks with strong answers for AI product managers, "
                 "forward deployed engineers, GenAI engineers, agentic AI engineers and AWS roles.",
        "promise": "Five roles, frameworks, real depth",
        "lessons": [
            "what-is-a-forward-deployed-engineer",
            "how-to-answer-ai-interview-questions",
            "ai-product-manager-interview-questions",
            "forward-deployed-engineer-interview-questions",
            "genai-engineer-interview-questions",
            "agentic-ai-engineer-interview-questions",
            "aws-generative-ai-interview-questions",
        ],
    },
]
