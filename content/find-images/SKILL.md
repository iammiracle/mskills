---
name: find-images
description: Find images for the user's content (Pinterest for ideas and mood boards, Openverse and Pexels for images cleared to use), download them with a record of where each came from, and check whether each one is usable — rights, size, crop and a visual check. Use when the user wants images, a mood board, Pinterest research, or asks whether an image can be used.
---

# Find images

Tool: `shared/tools/images.py`, run from `~/Documents/workspace/contents/`. Save images into the video's folder (`<name>/work/<video>/assets/images/`) or a channel mood board (`<name>/moodboard/<topic>/`).

## Sources, and what they're good for

| Source | Command | Rights | Use it for |
| --- | --- | --- | --- |
| Pinterest | `images.py pinterest "<query>" <dir> [n]` | **reference-only**, almost always | ideas, mood boards, seeing what's popular. Never in a post. |
| Openverse | `images.py openverse "<query>" <dir> [n]` | **usable** (CC0, public domain) or **attribution** (CC BY, BY-SA) | real images you can post. It's slow (~25 s) and limited to 20 searches a minute and 200 a day. |
| Pexels | `images.py pexels "<query>" <dir> [n]` | **usable** | high-res portrait photos; needs `PEXELS_API_KEY` in `contents/.env` |
| Its own | paths in `profile.yaml` → `look` | usable | always the first choice |

Every image gets `<name>.json` beside it, recording the source page, the creator, the licence and the `rights` value. Keep it with the image. A pin from a free-licence site (Unsplash, Pexels, Pixabay, Wikimedia) is marked **check-source**: open its page and confirm before using it.

## Checking usability

1. **Rights and size:** `images.py check <dir> 9:16` (or `4:5`, `1:1`). For each image it gives:
   - the rights;
   - whether it fills the frame sharply ("sharp" / "a bit soft" / "too small");
   - how much survives the crop.

   It writes `images.md` in the folder. Anything reference-only or unknown is **not usable**, whatever it looks like.
2. **By eye:** open every image that passed and note in `images.md`:
   - watermarks or logos;
   - text baked into the image;
   - recognisable people (fine under Pexels and CC0, but never imply they endorse the product, and avoid sensitive topics);
   - AI artefacts;
   - fit with `profile.yaml`'s look.
3. **Credit:** for an attribution image, put the sidecar's `attribution` text in the post caption.

## Rules

- Don't download Pinterest images in bulk or use them in posts. Pinterest grants no licence to reuse pins, and credit isn't permission.
- Never strip watermarks, crop out credits, or "edit enough to make it different". That doesn't change who owns it.
- When rights are unclear, call it not usable and say why. Suggest a licensed alternative, the channel's own photos, or making the image.
