# Prompts for the anatomy reel

The hook bank (section 3) is for both modes. Sections 1 and 2 are for AI-video mode only. Code-only scenes are in `scenes.md`.

Two shot types carry these accounts:

- **A. Filmed iPad:** a phone films an iPad lying on a desk while a hand zooms, taps or draws on a 3D model. This type has the biggest numbers.
- **B. Screen recording:** a phone screen recording of a 3D model turning on black. It's cheaper and simpler, and it still pulls 200K to 2.7M views.

Every video uses one caption from the hook bank for its whole length.

## 1. Start frames: `gpt_image_2_6`, aspect `9:16`

### A. Filmed iPad

```
Candid smartphone photo, vertical 9:16, looking down at a slight angle at an iPad Pro lying flat on a warm honey-colored wooden desk. The tablet fills most of the frame and is rotated a few degrees, the far edge of the desk and the iPad's black bezel visible at the top. The iPad screen shows a professional 3D human anatomy app: deep black background, {SUBJECT}, medical visualization quality. Along the bottom of the screen a row of rounded dark grey app buttons with small white line icons and tiny labels: {BUTTONS}. A long soft vertical white reflection streak from a ceiling light runs down the glass. Real phone camera look: slight screen moire, natural warm indoor light, a little soft at the edges. No hands, no people, no captions, no watermark.
```

- **Buttons:** the default is `Skeletal, Muscular, Heart, Arterial, Nervous, Digestive`. Change them to whatever the app's real tabs are.
- **Your own app:** pass 1-2 screenshots of the app as `image_references` and add "the iPad screen shows the app from the reference screenshots, same layout and colors". The video then shows your real UI.
- **Other desks:** white desk, desk with a coffee cup and a notebook, or a library table. Change the desk every few videos so an account doesn't look like one take reused.

### B. Screen recording

```
Vertical 9:16 iPhone screen recording frame of a 3D human anatomy app. Pure black background. {SUBJECT}, lit like a medical visualization, centered slightly above the middle. A thin vertical column of three or four small white outline icons on the right edge (scissors, a sun, an eye, the letters AI) inside dark circles. No status bar, no text, no captions, no watermark.
```

Leave the lower third fairly empty. The caption sits there.

### Subjects that work

| Subject | Prompt text |
|---|---|
| Heart | a photoreal glossy 3D human heart model, slightly turned, with red coronary arteries and blue veins running over its surface |
| Skull + nerves | a photoreal 3D human skull, three-quarter view, with thin yellow cranial nerves branching over the face and through the eye sockets |
| Sphenoid | a single photoreal 3D sphenoid bone (the butterfly-shaped skull bone with its wings and pterygoid plates), off-white bone texture with fine pores, three-quarter view |
| Muscular body | a photoreal full-body 3D model of the human muscular system, front view, standing, deep red striated muscles with white tendons |
| Skeleton | a photoreal full-body 3D human skeleton, ivory bones, relaxed three-quarter pose |
| Vascular body | a full-body 3D skeleton wrapped in red arteries, blue veins and yellow nerves, front view |
| Rib cage + lymph | a 3D rib cage and spine with green lymph vessels and a red spleen, front view |
| Neuron | an extreme close-up of a single 3D neuron, golden yellow cell body with thick branching dendrites, on grey tissue |
| Brain | a 3D human brain with the lobes in soft different colors, side view |
| Hand bones | the 27 bones of the human hand and wrist, ivory, palm view |
| Inner ear | the tiny 3D ear ossicles (malleus, incus, stapes) next to a coiled cochlea, macro view |
| Kidney | a 3D kidney cut in half showing the cortex, medulla and renal pelvis |

## 2. Animation: `gemini_omni_flash_1_2`

Settings: `mode: image-to-video`, `resolution: 1080p`, `duration: 10`, `aspect_ratio: 9:16`. The start frame's job id goes in `medias` with the role `start_image`. That's 32.5 credits a clip (22.5 at 720p).

**A1. Pinch-zoom + pencil arrow** (the 3.2M structure):
```
Handheld smartphone video looking down at an iPad lying on a wooden desk, with natural slight hand shake. A real human hand enters from the bottom right and pinch-zooms into the 3D {SUBJECT} on the screen with two fingers, and the model on the screen smoothly grows larger. Then the hand holds a white Apple Pencil, a dark rounded markup toolbar with pen tools and colored dots slides in at the top of the screen, and the pencil tip draws a thin red arrow on the glass pointing at {ONE STRUCTURE}. The ceiling-light reflection streak stays on the glass. Realistic unedited phone footage, one continuous shot, no cuts, no text overlays, no captions. Quiet room sound and soft taps on glass.
```

**A2. Pinch-zoom + tap to highlight:**
```
Handheld smartphone video looking down at an iPad lying on a wooden desk, with natural slight hand shake. A real human hand enters from the right and pinch-zooms into the 3D {SUBJECT} on the screen with two fingers, zooming toward {AREA} until it fills most of the screen. Then the index finger taps one {SMALL STRUCTURE} on the glass and that single part lights up bright yellow while the rest keeps its color. The ceiling-light reflection streak stays on the glass. Realistic unedited phone footage, one continuous shot, no cuts, no text overlays, no captions. Quiet room sound and soft taps on glass.
```

**A3. Layer toggle:**
```
... A finger taps the {BUTTON} button at the bottom of the app and the {OUTER LAYER} fades away layer by layer to reveal the {INNER LAYER} underneath, then two fingers rotate the model a little. ...
```

**B1. Turntable:**
```
Screen recording of a 3D anatomy app. The 3D {SUBJECT} rotates slowly and smoothly on the pure black background as if dragged by a finger, turning about 180 degrees around its vertical axis, then tilting a little to show its underside. The model keeps its exact shape, color and texture the whole time. The small white icons on the edge stay perfectly fixed in place. No camera movement, no hands, no cuts, no text, no captions. Silent.
```

**B2. Rotate + zoom:** the same as B1, but "turning about 90 degrees to show its side, then the view smoothly zooms in toward {AREA}".

If a clip comes back with a cut, a second hand, or a model that melts while it turns, run it again with the same frame. Don't try to fix it in the edit.

## 3. Hook bank

These are the captions the reference account used, with their views. Keep them lowercase with no full stop, the way a student types them.

| Views | Caption |
|---|---|
| 3.2M | if you have A in anatomy what is this nerve called |
| 2.7M | this bone is my biggest fear btw |
| 2.5M | If you can name this organ, then you are definitely a medical student. |
| 1.7M | my life became easier when i found this app |
| 652K | if you can name this bone you're probably a med student |
| 627K | can we all agree that learning muscles is easy? |
| 342K | if you can name this part of the heart, you are probably a med student |
| 321K | are you sure i need to know all of this??? |
| 276K | why is this muscle even needed? it's so small after all. |
| 187K | There's nothing better than knowing all of this. |

There are three hook shapes. Rotate between them:

- **Quiz (most views):** "if you have an A in anatomy what is this {nerve, artery, muscle} called", "if you can name this {bone, organ, part of the X} you're probably a med student", "only real med students know this one". People comment their answer, and that pushes the video.
- **Confession:** "this bone is my biggest fear btw", "are you sure i need to know all of this???", "i failed my exam because of this one". Pair these with a hard subject: sphenoid, temporal bone, brachial plexus, cranial nerves.
- **App line:** "my life became easier when i found this app", "studying anatomy hits different with this app", "There's nothing better than knowing all of this." Make about 1 in 4 videos this one. It's the hook that sells the app, and the comments ask for the name.
