# Builds audio.wav from cues.json (sfx times from the page) + the music bed.
import json, subprocess
cues = json.load(open('cues.json')); DUR = 30.6
inp = ['-i', 'a/music.mp3']; f = []
for i, c in enumerate(cues, 1):
    inp += ['-i', f"sfx/{c['f']}.mp3"]
    f.append(f"[{i}]volume={c['v']},adelay={int(c['t']*1000)}|{int(c['t']*1000)}[s{i}]")
f.insert(0, f"[0]volume=0.42,afade=t=out:st={DUR-1.2}:d=1.2[m]")
f.append('[m]' + ''.join(f'[s{i}]' for i in range(1, len(cues)+1)) + f"amix=inputs={len(cues)+1}:normalize=0,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[out]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(f), '-map', '[out]', '-ar', '44100', 'audio.wav'], check=True)
