"""The home page's tutorial band: learn to run agent projects one question at a time.

:func:`band` builds the band, its heading, its line, its body and its button. The four people from the
game, each asking one question and getting the lesson's answer beside a drawing (verdict-home 1.5), are
parcel H5's. Until they land the body is what they replace: the tutorial's tracks in order, and one
lesson sketch as a sample of how the lessons explain. Every number in the line comes from the lessons.
"""
from __future__ import annotations

from html import escape as _E

HOME_SKETCH = "four-pebbles-one-rock"            # the lesson sketch shown in the band, as a sample


def band() -> str:
    """The home page's fifth band (verdict-home 1.5)."""
    import render
    from pages import learn, sketch
    _meta, tracks, lessons = learn.load()
    first = tracks[0].lessons[0]                 # lesson one, where the band's button goes
    tracks_html = "".join(f'<li><a href="learn/{t.id}/"><b>{_E(t.title)}</b>'
                          f'<span>{len(t.lessons)} lessons</span></a></li>' for t in tracks)
    # one sketch from a lesson, as a sample of how the lessons explain: the picture, and where it is from
    sk = learn.sketches().get(HOME_SKETCH)
    sample = ""
    if sk:
        les = lessons[sk["lesson"]]
        sample = (f'<a class="learn-s" href="learn/{les.slug}/">{sketch.render(sk)[0]}'
                  f'<span class="learn-k">From lesson {les.n} of {_E(les.track.title)}: {_E(les.short)}\u00a0<i aria-hidden="true">→</i></span></a>')
    return f"""<section class="band" id="tutorial" aria-labelledby="h-learn"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The tutorial</p>
    <h2 id="h-learn">Learn to run agent projects one question at a time.</h2>
    <p>{len(lessons)} lessons in {render.NUM.get(len(tracks), len(tracks))} tracks, each answering a question a team asks.
    These four come from the fictional airline the manual follows. Lesson one takes {learn.minutes(first.body)} minutes.</p></header>
  <div class="learn-g">
    <ol class="jump tracks">{tracks_html}</ol>
    {sample}
  </div>
  <div class="ba"><a class="btn pri" href="learn/{first.slug}/">Start with lesson one</a></div>
</div></section>"""
