"""Build dist/earth_analog_finder.html from template.html + lib/. Run: python3 build.py"""
from pathlib import Path
here = Path(__file__).parent
t = (here / "template.html").read_text(encoding="utf-8")
for placeholder, name in [("/*D3*/", "d3.min.js"), ("/*TOPO*/", "topojson-client.min.js"),
                          ("/*THREE*/", "three.min.js"), ("/*WORLD*/", "countries-110m.json")]:
    assert placeholder in t, f"missing {placeholder} in template.html"
    t = t.replace(placeholder, (here / "lib" / name).read_text(encoding="utf-8"), 1)
out = here / "dist" / "earth_analog_finder.html"
out.parent.mkdir(exist_ok=True)
out.write_text(t, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size/1e6:.2f} MB)")
