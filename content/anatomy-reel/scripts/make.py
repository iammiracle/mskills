#!/usr/bin/env python3
"""Turn generated anatomy clips into finished TikToks: 1080x1920, TikTok-style caption, sound.

  python3 make.py videos.json            # every video in the file
  python3 make.py videos.json heart-1    # only the ids you name
  python3 make.py videos.json --preview  # caption PNGs only (check wrapping before rendering)

videos.json (paths are relative to the json file):
{
  "out_dir": "out",
  "music": "music/lofi.mp3",          optional, one track under every video
  "music_volume": 0.5,
  "clip_audio_volume": 0.35,          the model's own sound (taps, room). 0 drops it.
  "videos": [
    {"id": "heart-1", "clip": "clips/heart.mp4",
     "caption": "if you have an A in anatomy\\nwhat is this artery called",
     "y": 0.66, "start": 0.0, "dur": 10, "grain": 0}   grain 5-8 for code-built iPad shots
  ]
}
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'assets', 'TikTokSans.ttf')
W, H, FPS = 1080, 1920, 30

# Measured from the reference (a 3.2M-view post): white SemiBold text, thin black outline,
# about 47% of the frame wide for a 24-character line, centred, lines ~1.18x the size apart.
SIZE, STROKE, LEADING, MAX_W = 47, 3, 1.18, 760


def font(size=SIZE):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name('SemiBold')
    except Exception:
        pass
    return f


def wrap(text, f, d):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split():
            test = (cur + ' ' + word).strip()
            if d.textlength(test, font=f) <= MAX_W or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def caption_png(text, y_frac, path, size=SIZE):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(size)
    lines = wrap(text, f, d)
    step = int(size * LEADING)
    top = int(H * y_frac - step * len(lines) / 2)
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, top + i * step), line, font=f, fill=(255, 255, 255, 255),
               stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
    img.save(path)
    return lines


def run(args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def has_audio(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index',
                          '-of', 'csv=p=0', path], capture_output=True, text=True).stdout
    return bool(out.strip())


def main():
    cfg_path = sys.argv[1]
    only = [a for a in sys.argv[2:] if not a.startswith('--')]
    preview = '--preview' in sys.argv
    base = os.path.dirname(os.path.abspath(cfg_path))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)  # noqa: E731
    cfg = json.load(open(cfg_path))
    out_dir = P(cfg.get('out_dir', 'out'))
    work = os.path.join(base, 'build')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(work, exist_ok=True)
    music = P(cfg['music']) if cfg.get('music') else None
    mvol = cfg.get('music_volume', 0.5)
    cvol = cfg.get('clip_audio_volume', 0.35)

    for v in cfg['videos']:
        if only and v['id'] not in only:
            continue
        cap = os.path.join(work, f"{v['id']}_cap.png")
        lines = caption_png(v['caption'], v.get('y', 0.64), cap, v.get('size', SIZE))
        print(v['id'], '|', ' / '.join(lines))
        if preview:
            continue
        clip = P(v['clip'])
        start, dur = v.get('start', 0), v.get('dur', 10)
        grain = f",noise=alls={v['grain']}:allf=t" if v.get('grain') else ''  # phone-camera grain for code-built shots
        vf = (f'[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},'
              f'fps={FPS},setsar=1{grain}[bg];[bg][1:v]overlay=0:0,format=yuv420p[v]')
        inputs = ['-ss', str(start), '-t', str(dur), '-i', clip, '-loop', '1', '-t', str(dur), '-i', cap]
        a_parts, a_labels = [], []
        if cvol > 0 and has_audio(clip):
            a_parts.append(f'[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={cvol}[ca]')
            a_labels.append('[ca]')
        if music:
            inputs += ['-i', music]
            a_parts.append(f'[2:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},'
                           f'afade=t=in:d=0.3,afade=t=out:st={max(0, dur - 1.2)}:d=1.2,volume={mvol}[mu]')
            a_labels.append('[mu]')
        if not a_labels:  # silent track so every upload path accepts it
            inputs += ['-f', 'lavfi', '-t', str(dur), '-i', 'anullsrc=r=48000:cl=stereo']
            ai = 3 if music else 2
            a_parts.append(f'[{ai}:a]anull[sil]')
            a_labels.append('[sil]')
        fc = vf + ';' + ';'.join(a_parts)
        if a_labels == ['[sil]']:
            fc += ';[sil]anull[a]'
        elif len(a_labels) == 1:
            fc += f';{a_labels[0]}loudnorm=I=-14:TP=-1.5,aresample=48000[a]'
        else:
            fc += ';' + ''.join(a_labels) + f'amix=inputs={len(a_labels)}:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=48000[a]'
        out = os.path.join(out_dir, f"{v['id']}.mp4")
        run([*inputs, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(dur),
             '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', str(FPS),
             '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
        print('  ->', out)


if __name__ == '__main__':
    main()
