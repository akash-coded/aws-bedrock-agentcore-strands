"""check.py [lesson-slug ...]: run the build's sketch checks without building the site. Prints problems, or "ok"."""
import sys
sys.path.insert(0, "site")
from pages import learn

meta, tracks, lessons = learn.load()
errs = learn.check_sketches(lessons)
want = sys.argv[1:]
mine = [e for e in errs if not want or any(w in e for w in want)]
others = len(errs) - len(mine)
print("\n".join(mine) if mine else "ok")
if others:
    print(f"({others} problems in other lessons, not shown)")
