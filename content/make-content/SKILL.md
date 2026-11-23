---
name: make-content
description: Make short-form videos (Reels, TikTok, Shorts) for any of the user's apps or channels, from idea to rendered MP4 and caption, using the shared tools in ~/Documents/workspace/contents. Use when the user asks for content, a reel, an explainer, video ideas, a script or a caption for a channel, asks what's in progress, or wants to research what's working in a niche.
---

# Make content

A one-person content setup made of files, scripts and this skill. No dashboard, no database. All content lives in `~/Documents/workspace/contents/`; product code lives in `~/Documents/workspace/olympus/` and never holds content.

```
contents/
  .env                    every API key, once
  <name>/                 one folder per app or channel (anything with a profile.yaml)
    profile.yaml          facts tools read: voice, look, engine, formats, product path
    profile.md            nuance: audience, tone, claims, why
    ideas.md              backlog and log
    <date>/<slug>/        one finished post, and nothing else: the video or slides, the cover, caption.txt
    work/<date>-<slug>/   everything used to make it: status, script.md, research.md, narration.txt, assets/, code
    generator/            optional: the channel's own engine
  shared/                 what the user built for every channel
    formats/<format>.md   recipes: beats, rules, checklist (engine-agnostic)
    library/              breakdowns of reels that worked
    tools/                profiles.py, new.sh, status.sh, tts.sh, social.py, images.py, loudness.sh
    skills/               this skill, social-data, find-images
    template/             profile.md + profile.yaml to copy for a new channel
  muses/                  projects and skills found online to learn from or copy, listed in SOURCES.md
```

Tools live in `contents/shared/tools/`; run them from `contents/`. Every one takes a folder name and reads `<name>/profile.yaml`, so nothing specific to one app or channel is ever passed by hand.

## Work loop

Stages, kept in each piece's `work/<date>-<slug>/status` file: idea → scripted → approved → voiced → rendered → posted. Move between them with `status.sh <name>/<date>-<slug> <stage>`.

**Keep the finished folder clean.** The user opens `<name>/<date>/<slug>/` to post, so it holds only the files that get posted (video or slides, cover) and `caption.txt`. Scripts, research, REVIEW.md, audio, build files and tries stay in `work/`. Renders write straight into the finished folder; a bad try never lands there.

1. **Orient.** `status.sh` shows what's in progress across all channels. Read the channel's `profile.yaml` and `profile.md`. New channel: copy `shared/template/` to `channels/<name>/`, fill it in from the product's folder, and ask the user only for what can't be found.
2. **Idea.** Use `ideas.md`, or research with the `social-data` skill: `social.py accounts <name> --refs` for the channel's accounts and references, or `social.py <platform> top <handle>` and `transcript <url>`. Lead with a belief people hold, not a topic. Save strong references to `shared/library/`.
3. **Start.** `new.sh <name> <format> <slug>` creates both folders. Follow the format's recipe it names.
4. **Research.** Read primary sources (the paper's methods, not press coverage) and record quotes and pages in `research.md`. Never put a number on screen that the source doesn't give.
5. **Script, then stop.** Fill in `script.md` and `narration.txt`, set the stage to `scripted`, and **wait for the user's approval**. Set `approved` only when they say so.
6. **Voice.**
   - For `voice.provider: cartesia`: `tts.sh <name> <name>/work/<video>/narration.txt <name>/work/<video>/assets`, then `npx hyperframes transcribe assets/voiceover.mp3 --model small.en --language en` inside the work folder. Check the words match the script. Set `voiced`.
   - For other providers: use the channel's engine.
7. **Render** with the channel's `engine`:
   - `hyperframes`: load the `hyperframes` skill and follow it. Run `npx hyperframes init` in the work folder (or a subfolder), write `SPEC.md` from `profile.yaml`'s look, build one scene per beat timed to the transcript, then `check`, `snapshot --review` and fix. Copy fonts and images from the paths in `profile.yaml`.
   - `generator`: run `<name>/generator` as its README says, with `--out-dir` in the work folder; copy the finished mp4 to `<name>/<date>/<slug>/`. Load keys first with `set -a; source .env; set +a`.
   - Images that aren't the app's or channel's own go through the `find-images` skill. Only images it marks usable go into a video.
   - Render to `<name>/<date>/<slug>/<name>-<slug>.mp4`. Run `loudness.sh` on it (target −16 to −14 LUFS), write `REVIEW.md` in the work folder and `caption.txt` next to the video. Set `rendered`.
8. **Log.** Add the video under "Made" in `ideas.md`. The user posts it and moves it to `posted`.

## Adding to the setup

- **A new format:** write `shared/formats/<format>.md` (beats, rules, checklist), then add it to the channels it suits in their `profile.yaml`.
- **A new engine:** keep it in that folder (like `phrase5/generator/`) until a second app or channel needs it, then move it to `shared/engines/`.
- **A project or skill from GitHub:** read it before running it, and check the licence ("non-commercial" rules it out). Clone it into `muses/<name>/` with its own venv, record it in `muses/SOURCES.md` as `trying`, and keep `contents/.env` away from it until it's been read. When kept, mark it `kept` and point the channel at it (`engine: ../muses/<name>`); when dropped, delete the folder and note why.

## Rules

- The user decides when to commit and when to post. Never post or publish anything.
- Keys stay in `contents/.env`; never print them or write them anywhere else.
- Look, voice and claims come from the profile files, never from defaults.
