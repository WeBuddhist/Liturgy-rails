#!/usr/bin/env python3
"""TOC + block-ID pipeline for Liturgy-rails pilot texts.

Subcommands:
  extract <file> <out.txt>          - dump indexed blocks for TOC analysis
  apply   <file> <plan.json>        - insert headings + stamp block IDs (in place)
  verify  <orig_git_path> <file>    - invariance check vs git HEAD version
"""
import json, re, subprocess, sys

ID_RE = re.compile(r'\s\^[0-9A-Za-z][0-9A-Za-z-]*$')

def split_doc(text):
    """Return (frontmatter_str, body_str). Frontmatter includes both --- lines."""
    assert text.startswith('---\n'), 'no frontmatter'
    end = text.index('\n---\n', 4) + len('\n---\n')
    return text[:end], text[end:]

def body_blocks(body):
    """Split body into blocks (runs of non-blank lines). Returns list of
    (kind, lines) where kind is 'h1', 'wrapper', or 'block', plus the
    leading/trailing blank-line structure is normalised to single blank lines
    on re-emit."""
    lines = body.split('\n')
    blocks, cur = [], []
    for ln in lines:
        if ln.strip() == '':
            if cur:
                blocks.append(cur); cur = []
        else:
            cur.append(ln)
    if cur:
        blocks.append(cur)
    out = []
    for b in blocks:
        if len(b) == 1 and b[0].startswith('# '):
            out.append(('h1', b))
        elif len(b) == 1 and re.match(r'^##+\s', b[0]):
            out.append(('wrapper', b))
        else:
            out.append(('block', b))
    return out

def content_blocks(blocks):
    return [b for b in blocks if b[0] == 'block']

def cmd_extract(path, out):
    fm, body = split_doc(open(path).read())
    blocks = body_blocks(body)
    cbs = content_blocks(blocks)
    with open(out, 'w') as f:
        for i, (_, lines) in enumerate(cbs):
            f.write(f'[[{i}]]\n')
            f.write('\n'.join(lines) + '\n\n')
    print(f'{len(cbs)} content blocks -> {out}')

def cmd_apply(path, planpath):
    plan = json.load(open(planpath))
    sections = plan['sections']
    # validate
    sections.sort(key=lambda s: (s['before_block'],))
    assert sections and sections[0]['before_block'] == 0, \
        'first section must start at block 0 (add a preamble section)'
    for s in sections:
        assert s['level'] in (2, 3, 4)
        assert s['kind'] in ('preamble', 'content', 'colophon')
        assert s['title'].strip()

    fm, body = split_doc(open(path).read())
    blocks = body_blocks(body)
    cbs = content_blocks(blocks)
    n = len(cbs)
    for s in sections:
        assert 0 <= s['before_block'] < n, f"bad before_block {s['before_block']}"
    already = [b for _, b in cbs if ID_RE.search(b[-1])]
    assert not already, (
        f'{len(already)} blocks already carry ^ids — file looks processed. '
        'git restore it to the clean baseline before re-applying.')

    # assign IDs. Stack of (level, prefix, child_counter)
    by_block = {}
    for s in sections:
        by_block.setdefault(s['before_block'], []).append(s)
    for v in by_block.values():
        v.sort(key=lambda s: s['level'])

    out_lines = []
    h1 = next(b for b in blocks if b[0] == 'h1')
    out_lines.append(h1[1][0] + ' ^0')
    out_lines.append('')

    stack = []          # list of dicts: level, prefix, counter
    top_content = 0     # numbering for ## content sections
    top_colo = 0        # letter index for colophon sections

    # Block IDs are capped at 3 segments: they are numbered against the
    # nearest enclosing ## or ### (never a ####), so deeper TOC nesting
    # does not lengthen them. Headings and blocks share their scope's
    # counter, so no block id is ever a prefix of a heading id.
    def block_scope():
        return next(e for e in reversed(stack) if e['level'] <= 3)

    def emit_heading(s):
        nonlocal top_content, top_colo
        lvl = s['level']
        while stack and stack[-1]['level'] >= lvl:
            stack.pop()
        if lvl == 2:
            assert not stack
            if s['kind'] == 'preamble':
                prefix, num = 'I', '0. '
            elif s['kind'] == 'colophon':
                prefix, num = chr(ord('a') + top_colo), ''
                top_colo += 1
            else:
                top_content += 1
                prefix, num = str(top_content), f'{top_content}. '
            title = f"{'#'*lvl} {num}{s['title']} ^{prefix}-0"
        else:
            assert stack, f"level-{lvl} heading with no parent: {s['title']}"
            parent = stack[-1]
            parent['counter'] += 1
            prefix = f"{parent['prefix']}-{parent['counter']}"
            title = f"{'#'*lvl} {s['title']} ^{prefix}-0"
        stack.append({'level': lvl, 'prefix': prefix, 'counter': 0})
        out_lines.append(title)
        out_lines.append('')

    for i, (_, lines) in enumerate(cbs):
        for s in by_block.get(i, []):
            emit_heading(s)
        assert stack, 'block before any heading'
        cur = block_scope()
        cur['counter'] += 1
        bid = f"^{cur['prefix']}-{cur['counter']}"
        assert bid.count('-') <= 2, f'block id too deep: {bid}'
        stamped = list(lines)
        stamped[-1] = stamped[-1].rstrip() + f' {bid}'
        out_lines.extend(stamped)
        out_lines.append('')

    new = fm + '\n' + '\n'.join(out_lines).rstrip('\n') + '\n'
    open(path, 'w').write(new)
    n_head = len(sections)
    print(f'applied: {n_head} headings, {n} blocks stamped')

def strip_structure(text):
    """Remove heading lines and block IDs; collapse blank runs -> canonical."""
    fm, body = split_doc(text)
    keep = []
    for _, lines in body_blocks(body):
        pass
    out_blocks = []
    for kind, lines in body_blocks(body):
        if kind in ('h1', 'wrapper'):
            continue
        clean = list(lines)
        clean[-1] = ID_RE.sub('', clean[-1])
        out_blocks.append('\n'.join(clean))
    return fm, '\n\n'.join(out_blocks)

def cmd_verify(gitpath, path):
    orig = subprocess.run(['git', 'show', f'HEAD:{gitpath}'],
                          capture_output=True, text=True, check=True,
                          cwd='.').stdout
    new = open(path).read()
    ofm, obody = strip_structure(orig)
    nfm, nbody = strip_structure(new)
    ok = True
    if ofm != nfm:
        ok = False; print('FAIL: frontmatter differs')
    if obody != nbody:
        ok = False
        print('FAIL: body differs after stripping headings+IDs')
        import difflib
        for d in list(difflib.unified_diff(obody.split('\n'), nbody.split('\n'), lineterm=''))[:40]:
            print(d)
    # every block stamped exactly once
    unstamped = []
    for kind, lines in body_blocks(split_doc(new)[1]):
        if kind == 'block' and not ID_RE.search(lines[-1]):
            unstamped.append(lines[0][:40])
    if unstamped:
        ok = False; print(f'FAIL: {len(unstamped)} unstamped blocks: {unstamped[:5]}')
    # block ids must be at most 3 segments (headings may be deeper)
    deep = []
    for kind, lines in body_blocks(split_doc(new)[1]):
        if kind != 'block':
            continue
        m = ID_RE.search(lines[-1])
        if m and m.group(0).strip().count('-') > 2:
            deep.append(m.group(0).strip())
    if deep:
        ok = False; print(f'FAIL: {len(deep)} block ids deeper than 3 segments: {deep[:5]}')
    # unique IDs
    ids = re.findall(r'\^[0-9A-Za-z][0-9A-Za-z-]*', new)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        ok = False; print(f'FAIL: duplicate ids {sorted(dupes)[:10]}')
    print('OK' if ok else 'VERIFY FAILED')
    return 0 if ok else 1

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'extract':
        cmd_extract(sys.argv[2], sys.argv[3])
    elif cmd == 'apply':
        cmd_apply(sys.argv[2], sys.argv[3])
    elif cmd == 'verify':
        sys.exit(cmd_verify(sys.argv[2], sys.argv[3]))
