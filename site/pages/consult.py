"""The home page's close: work with the consultancy that wrote this manual.

:func:`band` builds the band (verdict-home 1.8): one framed panel with the heading and its line, four offers as
ruled columns, each ending in what a buyer leaves with, and one way to write. :func:`offers_ld` hands the same
four offers to the organisation in the home page's data, in the same words and with no prices. Both read
:data:`OFFERS`, so the page and the data cannot drift apart.

The button is a link to the repository's discussions page, a way to write that prints no address (the address
in ``frame/config.js`` stays in two parts). With script, ``frame/frame.js`` opens the contact drawer instead,
with the topic "Work with SkyWays Consultancy" chosen, because the link carries ``data-sw-open="consultancy"``.
"SkyWays Consultancy" is always written in full: the fictional airline in the case shares the name.
"""
from __future__ import annotations

from html import escape as _E

# Each offer: its name, what we do, and what a buyer leaves with. The owner's question 2 (verdict-home 5):
# these four services in this order, until the owner says otherwise. No client, figure or price is named here or
# in the data; one named client with one number is the owner's to give (question 3), never invented.
OFFERS = (
    ("Decide where AI pays",
     "We sort your list of AI ideas, with the people who own them, into plain code, a person's job or an agent, "
     "each with a number on it.",
     "A ranked list your finance team can check."),
    ("Teach every role the method",
     "Sessions for product, architecture, engineering, QA and platform teams, run on your own cases with the "
     "simulator and the labs.",
     "People in every role who can run their steps without us."),
    ("Put an agent into one workflow",
     "We build it with your engineers, from the signed spec to a pass mark proven on real cases, and hand it "
     "over running.",
     "A system your team runs, and the evidence to fund the next one."),
    ("Build tools that teach your case",
     "Simulators, calculators and explainers made around your own process, like the ones on this site.",
     "A simulator or calculator of your own case, on your own numbers."),
)


def band() -> str:
    """The home page's last band (verdict-home 1.8)."""
    import render
    offers = "".join(f'<li><h3>{_E(name)}</h3><p>{_E(does)}</p>'
                     f'<p class="cx-k"><span>You leave with</span> {_E(leave)}</p></li>' for name, does, leave in OFFERS)
    return f"""<section class="band cx" id="work-with-us" aria-labelledby="h-work"><div class="wrap"><div class="cx-in">
  <header class="sec-h split"><p class="eyebrow">SkyWays Consultancy</p>
    <h2 id="h-work">Work with the consultancy that wrote this manual.</h2>
    <p>We publish the method free. The paid work is applying it with your teams, on your own cases, with every
    decision written down for the people who audit you.</p></header>
  <ul class="cx-o">{offers}</ul>
  <div class="ba"><a class="btn pri" href="{render.REPO}/discussions" data-sw-open="consultancy">Write to {render.AUTHOR}</a>
    <small>Say what you want to change, and by&nbsp;when.</small></div>
</div></div></section>"""


def offers_ld() -> list[dict]:
    """The offers as schema.org entries for the organisation in the home page's data (``makesOffer``): each a
    service with the page's own name and words, and what a buyer leaves with as its output. No prices, and no
    word the page does not show."""
    return [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": name, "description": does,
                                                "serviceOutput": {"@type": "Thing", "name": leave}}}
            for name, does, leave in OFFERS]
