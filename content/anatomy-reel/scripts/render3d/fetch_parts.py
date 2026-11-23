#!/usr/bin/env python3
"""Find and download real anatomy meshes (BodyParts3D, 934 parts) for a scene, then write a
render-ready copy of the scene.

  python3 fetch_parts.py scene.json            -> downloads the meshes, writes scene.resolved.json
  python3 fetch_parts.py --find "sphenoid|palmaris"   -> lists matching part names, downloads nothing

In scene.json, each entry in "parts" names what to load with a regex over the English part names:
  {"match": "^sphenoid bone$", "id": "sphenoid", "look": "bone"}
  {"match": "^(frontal bone|mandible|(left|right) parietal bone)$"}        look is guessed if left out
One entry can load many meshes. "id" only works when the regex matches exactly one part.

Meshes are cached in ~/.cache/bodyparts3d. Credit line for anything you post:
  BodyParts3D, (c) The Database Center for Life Science, licensed under CC BY-SA 2.1 Japan
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = 'https://raw.githubusercontent.com/Kevin-Mattheus-Moerman/BodyParts3D/main/assets/BodyParts3D_data'
TREE = 'https://api.github.com/repos/Kevin-Mattheus-Moerman/BodyParts3D/git/trees/main?recursive=1'
CACHE = os.path.expanduser('~/.cache/bodyparts3d')
STL = os.path.join(CACHE, 'stl')

LOOKS = [  # first match wins
    ('tendon', r'retinaculum|membrane|ligament|aponeurosis|tendon|cartilage|intervertebral disk|linea alba|meniscus'),
    ('bone', r'\b(bone|humerus|radius|ulna|femur|tibia|fibula|patella|scapula|clavicle|rib|sternum|manubrium|vertebra|sacrum|coccyx|'
             r'mandible|maxilla|ethmoid|vomer|scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate|'
             r'phalanx|talus|calcaneus|cuboid|cuneiform|navicular|atlas|axis|concha)\b'),
    ('tooth', r'tooth'),
    ('artery', r'arter|aorta|arterial|coronary'),
    ('vein', r'vein|vena cava|venous|sinus'),
    ('nerve', r'nerve|plexus|optic tract|spinal cord'),
    ('heart', r'wall of heart|papillary|valve'),
    ('brain', r'gyrus|gyri|lobe of (left|right) cerebral|thalamus|cerebell|hippocamp|amygdala|putamen|nucleus|corpus callosum|'
              r'midbrain|medulla|pons|colliculus|fornix|insula|pallidus|hypothalamus|commissure|brain'),
    ('organ', r'lung|liver|kidney|stomach|colon|spleen|pancreas|duodenum|jejunum|ileum|esophagus|trachea|bronchus|gland|'
              r'bladder|eyeball|ear|testis|epididymis|appendix|gallbladder|thymus|ureter|diaphragm'),
]


def get(url, path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path + '.part')
        os.replace(path + '.part', path)
    return path


def catalogue():
    names = {}
    for line in open(get(f'{REPO}/parts_list_e.txt', os.path.join(CACHE, 'parts_list_e.txt')), encoding='utf-8').read().splitlines()[1:]:
        if '\t' in line:
            k, v = line.split('\t', 1)
            names[k] = v
    idx = os.path.join(CACHE, 'stl_index.json')
    if not os.path.exists(idx):
        tree = json.load(urllib.request.urlopen(TREE))['tree']
        json.dump([x['path'].split('/')[-1][:-4] for x in tree if x['path'].endswith('.stl')], open(idx, 'w'))
    have = set(json.load(open(idx)))
    return {k: v for k, v in names.items() if k in have}


def guess(name):
    for look, pat in LOOKS:
        if re.search(pat, name):
            return look
    return 'muscle'


def main():
    cat = catalogue()
    if sys.argv[1] == '--find':
        for k, v in sorted(cat.items(), key=lambda x: x[1]):
            if re.search(sys.argv[2], v):
                print(k, v, f'[{guess(v)}]')
        return
    path = sys.argv[1]
    scene = json.load(open(path))
    if 'parts' not in scene:
        sys.exit('this scene has no parts (an iPad scene uses the screen scene\'s meshes): run fetch_parts.py on that one')
    base = os.path.dirname(os.path.abspath(path))
    out, todo = [], []
    for p in scene['parts']:
        if 'file' in p:
            out.append(p)
            continue
        hits = [(k, v) for k, v in cat.items() if re.search(p['match'], v)]
        if not hits:
            sys.exit(f"no part matches {p['match']!r}. Try: fetch_parts.py --find '<word>'")
        if p.get('id') and len(hits) > 1:
            sys.exit(f"{p['match']!r} matches {len(hits)} parts but has an id: {[v for _, v in hits][:6]}")
        for k, v in hits:
            out.append({'file': f'stl/{k}.stl', 'look': p.get('look') or guess(v), 'id': p.get('id') or k, 'name': v})
            todo.append(k)
    with ThreadPoolExecutor(12) as ex:
        list(ex.map(lambda k: get(f'{REPO}/stl/{k}.stl', os.path.join(STL, f'{k}.stl')), set(todo)))
    link = os.path.join(base, 'stl')
    if not os.path.exists(link):
        os.symlink(STL, link)
    scene['parts'] = out
    dst = path.replace('.json', '.resolved.json')
    json.dump(scene, open(dst, 'w'), indent=1)
    print(f'{len(out)} meshes ready -> {dst}')


if __name__ == '__main__':
    main()
