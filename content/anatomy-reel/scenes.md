# Scene files (code-only mode)

A scene is one JSON file per video. `fetch_parts.py` turns it into `scene.resolved.json`, and `render.cjs` renders that.

## Parts

```json
"parts": [
  { "match": "^anterior interventricular branch of left coronary artery, nsn$", "id": "lad", "look": "artery" },
  { "match": "^(great cardiac vein|middle cardiac vein|coronary sinus)$", "look": "vein" },
  { "match": "^wall of heart$", "look": "heart" }
]
```

- **`match`:** a regex over the atlas's English part names. One entry can load many parts. Use `fetch_parts.py --find "<word>"` to see the exact names.
- **`id`:** gives a part a name, so the timeline can point at it (`highlight`, `tap`, `arrow`, `ghost`). It only works when `match` hits exactly one part.
- **`look`:** `bone`, `muscle`, `tendon`, `tooth`, `artery`, `vein`, `nerve`, `heart`, `brain` or `organ`. Leave it out and it's guessed from the name.

## Camera and model, over time

Every timed key is a list of `[seconds, value]` pairs. Values ease smoothly from one pair to the next.

| Key | Value | Notes |
|---|---|---|
| `yaw` | degrees | Turns the model left and right. 0 is the front of the body. |
| `pitch` | degrees | Tilts the top toward the camera (positive) or away (negative). |
| `distance` | model sizes | 1 is very close. The whole arm fits at about 4, the heart at about 4.9, the skull at about 6. |
| `target` | `[x, y, z]` in model sizes | The point the camera looks at. Negative y moves down the model. |
| `fov` | degrees | Default 30. |
| `drift` | `true` | A small handheld wobble. |

## Moments

| Key | Example | What it does |
|---|---|---|
| `highlight` | `{"part": "palmaris", "at": 5.15, "color": "#ffd21f"}` | The part turns that colour and glows a little. |
| `tap` | `{"part": "palmaris", "at": 5.0, "along": 0.72}` | The iOS touch dot appears on the part. `along` runs from 0 (bottom of the part) to 1 (top). |
| `ghost` | `{"at": 3.0, "opacity": 0.14}` | Every part except the lit one (or `keep: [ids]`) fades to see-through. |
| `arrow` | `{"part": "lad", "along": 0.55, "at": 4.6, "offset": [-240, -220], "color": "#ffd21f"}` | A pencil arrow is drawn on the glass and points at the part. `offset` is where the tail starts, in pixels from the tip. |

## App look

| Key | Default | Notes |
|---|---|---|
| `rail` | `["scissors", "sun", "eye", "AI"]` | The icon column on the right. Icons: scissors, sun, eye, pen, home, layers, or any short text. |
| `tabs` | none | The tab bar at the bottom, e.g. `[{"icon": "muscle", "label": "Muscular", "on": true}]`. Icons: bone, muscle, heart, artery, nerve, lungs. |
| `ui` | | Set it to `"none"` for no app UI. |
| `width`, `height` | 1080 x 1920 | Use 1116 x 1598 for the screen of an iPad scene. |
| `exposure`, `envIntensity`, `background` | 0.9, 0.22, `#000000` | Lighting. |

## iPad on a desk

```json
{ "page": "ipad.html", "screen": "forearm-screen.resolved.json", "duration": 10,
  "camY": 300, "camZ": 150, "fov": 49, "lookZ": 0 }
```

The screen scene renders first at iPad proportions (give it `width: 1116, height: 1598` and `tabs`). Then it plays on an iPad lying on a wooden desk, filmed by a slightly shaky phone.

| Key | What it changes |
|---|---|
| `camY`, `camZ` | How high and how far back the phone is |
| `ipadTurn` | How far the iPad is turned on the desk (degrees) |
| `wood` | The desk colour, as `[r, g, b]` |
| `streakX`, `streakAngle` | The ceiling-light streak |
| `shake` | 0 for a steady camera |

Add `"grain": 7` to the video in `videos.json`.
