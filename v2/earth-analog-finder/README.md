# Earth Analog Finder

Interactive heat map that scores places on Earth against Mars and the Moon.

## Run it
Open `dist/earth_analog_finder.html` in a browser (double-click). With internet access it fetches live NASA POWER climate data for the 30 named sites; otherwise it uses published estimates.

## Edit it
1. Edit `template.html`. Everything lives there:
   - **DATA MODEL** script block: factors (`PARAMS`), Mars/Moon reference values (`TARGETS`), regional estimates (`REGIONS`) and the 30 sites (`SITES`).
   - **APP** script block: map/globe drawing, scoring, weights, hover/click, NASA POWER fetch, 3D terrain.
2. Rebuild: `python3 build.py` (Python 3, no extra packages). This writes `dist/earth_analog_finder.html`.

## Files
| Path | What it is |
| --- | --- |
| `template.html` | Master source (HTML, CSS, data, app code) with library placeholders |
| `build.py` | Inserts the libraries and writes the finished page |
| `lib/d3.min.js` | D3.js v7: projections, drawing, radar chart |
| `lib/topojson-client.min.js` | Reads the world map data |
| `lib/countries-110m.json` | Country outlines and names (Natural Earth, via world-atlas) |
| `lib/three.min.js` | three.js r149: 3D terrain viewer |
| `dist/earth_analog_finder.html` | Built, ready-to-open page |

## Data status
- Site climate values (temperature, swing, aridity, solar, wind): NASA POWER when fetched live, otherwise published estimates.
- Roughness and dust: estimates. Heat map between named sites: interpolated. 3D terrain: generated stand-ins.
- To make the map fully data-driven, export gridded scores (see the data spec in the project plan) and replace the `REGIONS`/`SITES` blending.

Library licences: D3 (ISC), topojson-client (ISC), three.js (MIT), world-atlas / Natural Earth (public domain).
