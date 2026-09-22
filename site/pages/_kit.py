"""Small builders for the interactive components, so a page reads as content not markup.

Every one of these degrades: the engine only makes them faster to use. With JavaScript off a
calculator still shows its worked default, a self-check is still a readable list, a stepper shows
every panel, and both lenses are visible.
"""
from __future__ import annotations

import html

E = lambda s: html.escape(str(s), quote=False)  # noqa: E731


def lens_toggle(black: str = "What it means", white: str = "How it works") -> str:
    return (f'<div class="lens" data-lens-toggle role="group" aria-label="Level of detail">'
            f'<button type="button" data-lens-set="black" aria-pressed="true">'
            f'<span class="sw"></span>{E(black)}</button>'
            f'<button type="button" data-lens-set="white" aria-pressed="false">'
            f'<span class="sw"></span>{E(white)}</button></div>')


def lens(black: str, white: str, black_label: str = "What it means",
         white_label: str = "How it works") -> str:
    """Two readings of one idea. Both render without JavaScript."""
    return (f'<div data-lens="black"><span class="lk">{E(black_label)}</span>{black}</div>'
            f'<div data-lens="white"><span class="lk">{E(white_label)}</span>{white}</div>')


def calc(name: str, title: str, subtitle: str, inputs: list[dict], outputs: list[dict],
         formula: str = "") -> str:
    """A live calculator. ``inputs`` are dicts of key/label/type/min/max/step/value/options."""
    fields = []
    for i in inputs:
        key, label = i["key"], i["label"]
        if i.get("type") == "select":
            opts = "".join(f'<option value="{E(v)}"{" selected" if v == i.get("value") else ""}>'
                           f'{E(t)}</option>' for v, t in i["options"])
            ctrl = f'<select data-in="{E(key)}">{opts}</select>'
            head = f"<span>{E(label)}</span>"
        elif i.get("type") == "number":
            ctrl = (f'<input type="number" data-in="{E(key)}" value="{i["value"]}" '
                    f'min="{i.get("min", 0)}" step="{i.get("step", 1)}">')
            head = f"<span>{E(label)}</span>"
        else:
            ctrl = (f'<input type="range" data-in="{E(key)}" min="{i["min"]}" max="{i["max"]}" '
                    f'step="{i.get("step", 1)}" value="{i["value"]}">')
            head = (f'<span class="lv"><span>{E(label)}</span>'
                    f'<b data-echo="{E(key)}">{i["value"]}</b></span>')
        fields.append(f"<label>{head}{ctrl}</label>")
    rows = []
    for o in outputs:
        cls = " big" if o.get("big") else ""
        if o.get("verdict"):
            rows.append(f'<div class="cv" data-out="{E(o["key"])}">{E(o.get("value", ""))}</div>')
        else:
            rows.append(f'<div class="cr{cls}"><span>{E(o["label"])}</span>'
                        f'<output data-out="{E(o["key"])}">{E(o.get("value", "—"))}</output></div>')
    foot = f'<div class="cf">{E(formula)}</div>' if formula else ""
    return (f'<div class="calc" data-calc="{E(name)}">'
            f'<div class="ch"><b>{E(title)}</b><span>{E(subtitle)}</span></div>'
            f'<div class="cg"><div class="ci">{"".join(fields)}</div>'
            f'<div class="co">{"".join(rows)}</div></div>{foot}</div>')


def check(items: list[tuple[str, str]], bands: list[str], question: str = "") -> str:
    """A self-check that totals itself. ``items`` are (control, the test that proves it)."""
    lis = []
    for n, (title, test) in enumerate(items):
        lis.append(f'<li><input type="checkbox" id="ck{n}-{abs(hash(title)) % 9999}" '
                   f'data-label="{E(title)}"><label for="ck{n}-{abs(hash(title)) % 9999}">'
                   f'<b>{E(title)}</b><span>{E(test)}</span></label></li>')
    q = f"<p><strong>{E(question)}</strong></p>" if question else ""
    return (f'<div class="chk" data-score data-score-bands="{E("|".join(bands))}">{q}'
            f'<ul>{"".join(lis)}</ul>'
            f'<div class="cs"><span class="n" data-score-out>0 of {len(items)}</span>'
            f'<span class="v" data-score-verdict>{E(bands[0])}</span></div>'
            f'<p class="nx">Next control to build: <b data-score-next></b></p></div>')


def stepper(steps: list[tuple[str, str]], label: str = "") -> str:
    """A sequence you walk. Every panel prints."""
    panels = "".join(f'<div data-step="{E(t)}"{" hidden" if i else ""}>{b}</div>'
                     for i, (t, b) in enumerate(steps))
    return (f'<div class="stp" data-stepper tabindex="0" aria-label="{E(label or "Steps")}">'
            f'<div class="sh2"><span class="sl" data-step-label></span>'
            f'<span data-step-dots></span></div>{panels}'
            f'<div class="sn2"><button type="button" data-step-prev>Back</button>'
            f'<button type="button" data-step-next>Next</button></div></div>')
