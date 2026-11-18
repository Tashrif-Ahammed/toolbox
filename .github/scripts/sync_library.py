#!/usr/bin/env python3
"""Keeps library.json in step with the files in tools/.

 * a new tools/*.html file gets a card (name, description, icon, category read from the file)
 * a card whose file was removed is parked under "unlinked" (nothing is lost); it comes back
   with its saved details if the file returns to the same path
 * tools/<file>.meta.json or <meta name="toolbox-..."> tags in the HTML give the details
Private tools live encrypted under vault/ and are never touched here."""
import glob, html, json, os, re, time

LIB = 'library.json'
lib = json.load(open(LIB, encoding='utf-8')) if os.path.exists(LIB) else {}
lib.setdefault('v', 3)
for k in ('tools', 'archived', 'categories', 'unlinked'):
    lib.setdefault(k, [])
lib.setdefault('defaultCategory', '')

files = sorted(set(p.replace('\\', '/') for p in glob.glob('tools/**/*.htm*', recursive=True)))
exists = set(files)

def slug(s):
    return re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', s.lower())) or 'tool'

def meta_from(path):
    out = {}
    try:
        head = open(path, encoding='utf-8', errors='ignore').read(30000)
    except OSError:
        head = ''
    m = re.search(r'<title[^>]*>(.*?)</title>', head, re.I | re.S)
    if m and m.group(1).strip():
        out['name'] = html.unescape(re.sub(r'\s+', ' ', m.group(1)).strip())
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', head, re.I)
    if m:
        out['desc'] = html.unescape(m.group(1).strip())
    for key in ('name', 'desc', 'icon', 'category'):
        m = re.search(r'<meta[^>]+name=["\']toolbox-%s["\'][^>]*content=["\']([^"\']*)["\']' % key, head, re.I)
        if m:
            out[key] = html.unescape(m.group(1).strip())
    side = re.sub(r'\.html?$', '', path, flags=re.I) + '.meta.json'
    if os.path.exists(side):
        try:
            d = json.load(open(side, encoding='utf-8'))
            for key in ('name', 'desc', 'icon', 'category'):
                if isinstance(d.get(key), str):
                    out[key] = d[key]
        except Exception as e:
            print('bad sidecar', side, e)
    return out

def ensure_category(name):
    name = (name or '').strip().lower()
    if name and not any(c.get('name') == name for c in lib['categories']):
        lib['categories'].append({'name': name, 'home': False, 'defaultIcons': []})
    return name

changed = []
# 1) park cards whose file is gone
for group in ('tools', 'archived'):
    keep = []
    for t in lib[group]:
        f = t.get('file')
        if f and f.startswith('tools/') and f not in exists:
            if group == 'tools':
                lib['unlinked'].append(t)
            changed.append('parked ' + t.get('name', f))
        else:
            keep.append(t)
    lib[group] = keep
# 2) reconnect parked cards whose file is back
back = []
for u in lib['unlinked']:
    if u.get('file') in exists:
        u['visibility'] = 'public'
        lib['tools'].append(u)
        changed.append('reconnected ' + u.get('name', u['file']))
    else:
        back.append(u)
lib['unlinked'] = back
# 3) register new files; apply sidecar details to existing cards
known = {t.get('file') for t in lib['tools'] + lib['archived']}
ids = {t.get('id') for t in lib['tools'] + lib['archived'] + lib['unlinked']}
for f in files:
    if f.lower().endswith('.meta.json'):
        continue
    md = meta_from(f)
    if f in known:
        side = re.sub(r'\.html?$', '', f, flags=re.I) + '.meta.json'
        if os.path.exists(side):
            for t in lib['tools'] + lib['archived']:
                if t.get('file') == f:
                    for k in ('name', 'desc', 'icon'):
                        if k in md and t.get(k) != md[k]:
                            t[k] = md[k]; changed.append('updated ' + f)
                    if 'category' in md:
                        t['category'] = ensure_category(md['category'])
        continue
    base = os.path.basename(f)
    base = re.sub(r'\.html?$', '', base, flags=re.I)
    i, n = slug(base), 2
    uid = i
    while uid in ids:
        uid = '%s-%d' % (i, n); n += 1
    ids.add(uid)
    lib['tools'].append({
        'id': uid, 'name': md.get('name') or base, 'desc': md.get('desc', ''), 'icon': md.get('icon') or '🛠️',
        'category': ensure_category(md.get('category')) or lib.get('defaultCategory', ''),
        'file': f, 'autoDetected': True, 'reviewed': False, 'addedAt': int(time.time() * 1000), 'visibility': 'public'})
    changed.append('added ' + f)

if changed:
    lib['updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    with open(LIB, 'w', encoding='utf-8') as fh:
        json.dump(lib, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
print('\n'.join(changed) if changed else 'library already up to date')
