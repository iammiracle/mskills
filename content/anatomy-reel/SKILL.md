---
name: anatomy-reel
description: Make the organic TikToks that anatomy apps farm views with (the @rita.havis6 format, 187K-3.2M views per post). A 3D bone, heart, skull or muscle turns, zooms, lights up or gets an arrow drawn on it, filmed on an iPad or shown as a screen recording, with one lowercase TikTok caption on top ("if you have an A in anatomy what is this artery called"). Two modes. Code only (free, the default): Claude renders real human anatomy meshes (BodyParts3D) itself with Three.js, for zero credits. AI video: Gemini Omni on Higgsfield, for shots that need real hands. One config goes to finished 1080x1920 mp4s. Use when asked for "anatomy videos", "the anatomy app TikToks", "med student quiz videos", "3D anatomy app reel", "videos like rita.havis6", or "/anatomy-reel".
---

# Anatomy reel

The format, measured from the reference account:

| What | Detail |
|---|---|
| Length | 7-12s, one continuous shot, no cuts |
| Screen recording | A 3D model turns slowly on pure black, with a thin column of white icons on the right edge. The user zooms in, taps a part so it lights up, or fades the rest to see-through. |
| Filmed iPad | A phone films an iPad on a wooden desk, with a ceiling-light streak on the glass. The app's tab bar sits at the bottom (Skeletal, Muscular, Heart…). |
| Caption | One caption for the whole video, lowercase like a student typed it, in the TikTok font: white SemiBold with a thin black outline. It sits at 60-80% of the height, two lines. |
| Sound | A trending or lo-fi sound. |

Quiz captions get the most views because people comment their answer. One in four videos uses the app line ("my life became easier when i found this app"). That's the one that sells the app.

## Pick a mode

| | Code only (default) | AI video |
|---|---|---|
| What makes it | Claude writes a scene and renders real anatomy meshes with Three.js | `gpt_image_2_6` start frame + `gemini_omni_flash_1_2` |
| Cost | Free | about 33 Higgsfield credits per 10s video |
| Anatomy | Real, from the BodyParts3D atlas, so the quiz answer is right | Made up by the model, so check every part |
| Can do | Turntable, zoom, tap to highlight, fade others to see-through, pencil arrow, iPad on a desk | All of that plus a real hand pinching, tapping and drawing |
| Can't do | Hands | Guaranteed-correct anatomy |

Use code only unless the brief needs a visible hand.

## What you need
- `ffmpeg` and Python 3 with Pillow (both modes).
- **Code only:** Node 18+. Run `npm install` once in `scripts/render3d/`. It installs Puppeteer and a headless Chrome.
- **AI video:** the Higgsfield MCP.
- **Optional:** an ElevenLabs key for a music bed, or add a trending sound in the TikTok app.

## Steps (code only)

1. **Brief.** Get the app name and its tab names, and how many videos to make. Default: 4 videos, with 2 quiz captions, 1 confession and 1 app line.

2. **Pick subjects.** Run `python3 scripts/render3d/fetch_parts.py --find "<word>"` to see what the atlas has.
   - It has 934 parts: every bone, the skull bones one by one, the arm, leg and trunk muscles one by one, the heart wall with every coronary artery and cardiac vein, and the brain regions.
   - Nerves outside the head, skin and fascia aren't in it.
   - Pick a structure people get wrong in exams: sphenoid, palmaris longus, the LAD, the hamate, the pterygoid plates.

3. **Write a scene.** Start from the closest file in `examples/scenes/`. `scenes.md` explains every key.
   - `heart-lad.json`: zoom, then a pencil arrow on the LAD.
   - `skull-sphenoid.json`: the skull turns, then everything except the sphenoid fades.
   - `forearm-palmaris.json`: the whole arm, a pinch-zoom, a tap, then the palmaris lights up.
   - `forearm-ipad.json` (with `forearm-screen.json`): the same arm on an iPad on a desk.

4. **Fetch the meshes.** Run `python3 scripts/render3d/fetch_parts.py scene.json`. It downloads them into `~/.cache/bodyparts3d` and writes `scene.resolved.json`.

5. **Check stills.** Run `node scripts/render3d/render.cjs scene.resolved.json check.png --at <seconds>` for the opening, the zoomed view and the highlight or arrow moment, and look at each one.
   - The model should fill the width without being cut off.
   - The part that lights up should face the camera.
   - The arrow should touch the structure.
   - The lower third should leave room for the caption.

   If something's wrong, change `yaw`, `distance`, `target` or `offset` and check again. A still takes about 5 seconds.

6. **Render.** Run `node scripts/render3d/render.cjs scene.resolved.json clips/<id>.mp4`. A 10s video takes 10-20 seconds.

7. **Caption and sound.** Add each clip to `videos.json`, run `python3 scripts/make.py videos.json --preview` to check the line breaks, then `python3 scripts/make.py videos.json`.
   - Use `"grain": 7` on iPad shots so they look filmed.
   - Put the caption's `y` where it doesn't cover the arrow or the lit part.

8. **Check.** Watch each mp4 once all the way through.

9. **Credit.** The meshes are CC BY-SA 2.1 Japan. Put "3D models: BodyParts3D, © DBCLS, CC BY-SA 2.1 JP" in the post caption or the account bio.

## Steps (AI video)

Follow steps 1-2 and 7-8 above. In between:

- **Frames.** Generate one `gpt_image_2_6` 9:16 start frame per video from `prompts.md`, using `generate_image_batch` with 8 or fewer at a time. Check each one: clean anatomy, readable tab text, room for the caption.
- **Animation.** Run `gemini_omni_flash_1_2` with `mode: image-to-video`, `resolution: 1080p`, `duration: 10`, `aspect_ratio: 9:16`, and the frame's job id as `start_image`. That's 32.5 credits a clip.

## Gotchas
- **Ink has to contrast with the model.** Red ink on a red heart disappears. Use yellow on the heart and muscles, and red on bone.
- **The arrow is aimed once, when it starts drawing.** Stop the model turning before the arrow's `at`, the way a real user would. If the renderer says "arrow is off screen", pull the camera back.
- **`distance` is measured in model sizes.** Adding or removing a big part (the pulmonary arteries reach into the lungs) changes the size, so recheck the framing.
- **One right arm.** The atlas has left and right copies of most parts. Load one side, or the camera frames both arms.
- **AI mode:** Gemini sometimes adds a cut or melts a bone while it turns. Run it again with the same frame. Its clips come out at 24fps, and `make.py` converts them to 30fps.

## Files
- `scripts/render3d/fetch_parts.py`: finds parts by name in the atlas, downloads them and resolves a scene.
- `scripts/render3d/render.cjs`: renders a scene to an mp4 or a still. iPad scenes render in two passes.
- `scripts/render3d/viewer.html`: the 3D anatomy app (lighting, bone, muscle and vessel looks, app UI, tap, highlight, fade, arrow).
- `scripts/render3d/ipad.html`: the desk, the iPad, the light streak and the handheld camera.
- `scripts/make.py`: burns in the caption, mixes the sound and exports a 1080x1920 mp4 at -14 LUFS.
- `scenes.md`: every scene key with examples.
- `prompts.md`: the hook bank with real views, plus the AI-mode image and motion prompts.
- `examples/`: the demo scenes and `videos.json`.
- `assets/TikTokSans.ttf`: TikTok's own font (SIL OFL, license next to it).
