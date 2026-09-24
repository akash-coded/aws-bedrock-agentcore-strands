// The tutorial's diagrams, drawn in the page's theme and redrawn when the theme changes.
//
// The mermaid source stays in the page as a <pre> — it is what a reader without script, a crawler
// or an assistant reads — and the drawing goes in a sibling. The pinned mermaid URL comes from the
// script tag, so the version lives in one place: site/pages/learn.py.

const tag = document.querySelector("script[data-mermaid]");
const sources = [...document.querySelectorAll("pre.mermaid")];

// The lesson list and the contents box are open in the HTML so they work without script; on a
// phone both start closed, so the lesson itself is the first thing on screen.
if (matchMedia("(max-width: 900px)").matches) {
  for (const d of document.querySelectorAll(".lnav, .otp")) d.removeAttribute("open");
}

const dark = () => {
  const t = document.documentElement.getAttribute("data-theme");
  return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
};

if (sources.length && tag) {
  const { default: mermaid } = await import(tag.dataset.mermaid);
  let drawn = null;
  let n = 0;
  const draw = async () => {
    const mode = dark() ? "dark" : "default";
    if (mode === drawn) return;
    drawn = mode;
    mermaid.initialize({
      startOnLoad: false, theme: mode, securityLevel: "strict",
      fontFamily: "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif",
      themeVariables: { fontSize: "15px", fontFamily: "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif" },
      flowchart: { htmlLabels: true, curve: "basis", padding: 14, nodeSpacing: 34, rankSpacing: 44 },
    });
    for (const pre of sources) {
      let out = pre.nextElementSibling;
      if (!out || !out.classList.contains("mm-out")) {
        out = document.createElement("div");
        out.className = "mm-out";
        pre.after(out);
      }
      try {
        const { svg } = await mermaid.render(`mmd-${n++}`, pre.textContent);
        out.innerHTML = svg;
        pre.classList.add("drawn");
        // mermaid sizes a drawing to its content; a small one may grow, up to a third, to read
        const el = out.querySelector("svg");
        const nat = parseFloat((el.style.maxWidth || "").replace("px", "")) || el.viewBox?.baseVal?.width || 0;
        if (nat) { el.style.maxWidth = Math.round(nat * 1.32) + "px"; el.style.width = "100%"; }
      } catch (e) {
        // leave the source visible: a readable diagram beats an empty box
        out.remove();
        pre.classList.remove("drawn");
        console.warn("diagram did not render", e);
      }
    }
  };
  // mermaid sizes every label from the font it measures with, so measure with the one readers get
  try {
    await Promise.all(["400 16px Inter", "italic 400 16px Inter", "700 16px Inter"]
      .map((f) => document.fonts.load(f)));
  } catch {}
  await draw();
  new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", draw);
}
