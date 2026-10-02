"""The home page's library band: take the tools, templates and prompts with you.

:func:`band` builds the band, its heading, its line and its body. The three by three grid, three tools on
the material of what each opens and six shelves under them, every count computed (verdict-home 1.7), is
parcel H7's. Until it lands the body is the shelf it replaces: four tiles, each a count, a name and a line.
"""
from __future__ import annotations


def band() -> str:
    """The home page's seventh band (verdict-home 1.7)."""
    import render
    from pages import pictures
    roles = render.load_roles()
    total_steps = sum(len(r["steps"]) for r in roles)
    total_prompts = sum(len(s["prompts"]) for r in roles for s in r["steps"])
    n_pics = len(pictures.catalogue())
    return f"""<section class="band" id="library" aria-labelledby="h-lib"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The library</p>
    <h2 id="h-lib">Take the tools, templates and prompts with you.</h2>
    <p>Start with one of the three tools, or copy what you need from the shelves. All of it is free to reuse under the MIT licence.</p></header>
  <div class="shelf">
    <a class="tile" href="templates/"><span class="tile-k">{total_steps} templates</span><b>Templates</b>
      <span class="tile-d">One document to fill in for every step.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="prompts/"><span class="tile-k">{total_prompts} prompts</span><b>Prompts</b>
      <span class="tile-d">Each states the job, the inputs and the shape of the answer.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="models/"><span class="tile-k">12 rules of thumb</span><b>Mental models</b>
      <span class="tile-d">Each one names the mistake it prevents.</span><span class="tile-go" aria-hidden="true">→</span></a>
    <a class="tile" href="pictures/"><span class="tile-k">{n_pics} pictures</span><b>The picture pack</b>
      <span class="tile-d">Every diagram here, light and dark, free to reuse.</span><span class="tile-go" aria-hidden="true">→</span></a>
  </div>
</div></section>"""
