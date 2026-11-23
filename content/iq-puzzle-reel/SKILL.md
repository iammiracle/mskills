---
name: iq-puzzle-reel
description: Make 9:16 IQ / brain-teaser puzzle game reels, the kind IQ apps run as ads. A real hand solves 4-5 trick puzzles on a notebook page (one wrong try with a red X, then the trick and a green check), then a "Try it yourself / Play now" end card. Everything is drawn in code (HTML + SVG + GSAP), rendered frame by frame with puppeteer, and mixed with ffmpeg. Use when asked for an IQ reel, a brain test / tricky puzzle ad, a puzzle game ad, or "videos like the IQ apps run".
---

# IQ puzzle reel

The format: a notebook page on a wooden desk. A level number and a short question on top ("Make both sides equal."). A real hand comes in, tries the obvious move, gets a red X and a buzzer, then does the trick (drags a word, flips a number, taps the UI) and gets a green check. 4-5 levels of 4-6 seconds each, hard cuts between them, then an end card with the app icon, "TRY IT YOURSELF" and a "PLAY NOW" button the hand taps.

Why it works: every level is a tiny curiosity loop. The viewer guesses the obvious answer, sees it fail, then sees the trick. That is the whole hook, every 5 seconds.

`template/` is a finished 30.6s reel with 5 levels. Copy it and change the levels.

## Steps

1. **Ask for the app.** Name, its icon (a PNG, or describe it and draw it in SVG), and the end card line. Default: "TRY IT YOURSELF" + "PLAY NOW".
2. **Pick 5 puzzles** from `puzzles.md`, or write new ones with the same shape: a question, an obvious wrong move, and a trick that breaks a rule of the page. Show the user the 5 (question, wrong try, trick) and wait for a yes.
   - Use original puzzles and your own app's look. Don't copy another game's levels, characters or logo.
3. **Copy the template:** `cp -r template ~/my-iq-reel && cd ~/my-iq-reel`.
4. **Get the sounds** into `sfx/` (see Sounds below) and a music bed at `a/music.mp3`.
5. **Build the levels** in `index.html`. Each level is a `<div class="lv" id="L1">` with a question and an inline SVG. The script at the bottom is the timeline. The helpers do the hand:
   - `level(t, '#L2', 28, '#L1')` cuts to a level and sets the LEVEL number.
   - `move(t, x, y, dur)` moves the fingertip to x,y (1080x1920 stage pixels).
   - `tap(t, x, y)` presses with a ripple and a click. `press(t)` / `release(t)` hold for a drag.
   - Drag = `press`, then tween the object and `move` the hand with the same time and duration, then `release`.
   - `wrong(t, x, y)` red X + buzzer. `right(t, x, y)` green check + chime.
   - `sfx(t, 'name', volume)` adds any sound at time t (the file is `sfx/name.mp3`).
   Drawing style: black outlines (stroke 7, round joins), flat fills, no gradients on characters, skin `#f6c69d`. Questions are short: "Plain" text in Patrick Hand, or the yellow pill in Fredoka.
6. **Check stills before the full render:**
   `NODE_PATH=<folder with puppeteer> node render.cjs stills 1,3.5,7,10,...`
   Look at every still. Check: the fingertip sits on the thing it taps, nothing is cut off, the question fits on one line, the check and X land on the subject, nothing from the last level shows in the next one.
7. **Render:** `node render.cjs full` (writes `frames/` and `cues.json`), then `python3 mix.py` (music + every sfx at its time, loudnorm -14), then
   `ffmpeg -framerate 30 -i frames/%05d.jpg -i audio.wav -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest iq-reel.mp4`
8. **Contact sheet the final** (`ffmpeg -i iq-reel.mp4 -vf "fps=1.5,scale=216:-1,tile=9x5" -frames:v 1 sheet.jpg`) and look at it before handing it over.

## The hand

`template/a/hand.png` is a real-looking hand (red nails, pointing up-left) with the forearm extended long enough that it never ends on screen, even when it taps the top bar. The fingertip sits at (230, 210) in the scaled image, and `move()` already accounts for that. To make a different hand, generate a photo of a hand pointing up-left on pure white, remove the background, and extend the forearm the same way (repeat the forearm's cross-section along its angle). Keep the fingertip offset in `applyHand()` right.

## Timing that works

- Level 1 starts with the hand already moving at 0.3s. No intro, no title.
- Wrong try at about 1s into a level, the X at about 1.7s, the trick at about 3s, the check at about 4.3s, cut at 5-6s.
- After the check the hand slides off to the bottom right, so the solved scene reads clean.
- End card at about 27.5s: the page flies up, the icon pops, then the text, then the button, which pulses until the hand taps it.

## Sounds

`mix.py` plays `sfx/<name>.mp3` for every `sfx()` and `tap()` in the timeline. The template uses: tick (tap), toggle, plop, pop2, softpop (level cut), flip (page), spin, success (check), wrong (buzzer), snore, rain, lvup1. Free sources: Mixkit (mixkit.co/free-sound-effects/, free license, no account) or generate them with the ElevenLabs API directly (key in ~/Documents/workspace/contents/.env; paid, so ask the user first). Never use Higgsfield. Example sound prompts: "short cartoon mobile game wrong answer buzzer, two quick low descending honks" (1s), "light rain falling and water pouring into a glass, cartoon style" (3s). Music: a quirky instrumental bed, 34s, instrumental, "quirky playful casual mobile puzzle game music, bouncy pizzicato strings, marimba, light ukulele, steady upbeat 120 bpm, no drops". Missing sounds are your job to add before `mix.py` runs, or it stops.

## Rules

- One idea per level. If the trick needs explaining, cut the level.
- The trick must be visible: the viewer has to see what the hand did (a word moving, a number flipping, a switch going off).
- Every level gets one wrong try first. That's where people comment "I would have done that too".
- No narration, no captions. The question on the page is the only text.
- No real game's name, levels, characters or logo, and no fake download numbers on screen.
