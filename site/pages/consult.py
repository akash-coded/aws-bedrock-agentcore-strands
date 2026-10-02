"""The home page's close: work with the consultancy that wrote this manual.

:func:`band` builds the band, its heading, its line and one way to write. The four offers, each ending in
what a buyer leaves with, the panel they sit in, the line beside the button and the drawer's own topic for
it (verdict-home 1.8) are parcel H8's. Until they land the button is a plain link to the repository's
discussions page, a way to write that prints no address. "SkyWays Consultancy" is always written in full:
the fictional airline in the case shares the name.
"""
from __future__ import annotations


def band() -> str:
    """The home page's last band (verdict-home 1.8)."""
    import render
    return f"""<section class="band" id="work-with-us" aria-labelledby="h-work"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">SkyWays Consultancy</p>
    <h2 id="h-work">Work with the consultancy that wrote this manual.</h2>
    <p>We publish the method free. The paid work is applying it with your teams, on your own cases, with every
    decision written down for the people who audit you.</p></header>
  <div class="ba"><a class="btn pri" href="{render.REPO}/discussions">Write to {render.AUTHOR}</a></div>
</div></section>"""


def offers_ld() -> list[dict]:
    """The offers as schema.org entries for the organisation in the home page's data (``makesOffer``), in the
    page's own words and with no prices. Empty until the offers are on the page: the data says nothing the
    page does not."""
    return []
