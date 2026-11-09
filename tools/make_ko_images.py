"""영문 UI 이미지 → 한국어 이미지 (중문판 대조로 글자 영역 검출, 배경 복원, 본명조로 재작성)
사용: python3 tools/make_ko_images.py [필터접두어...]"""
import json, sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = os.path.join(ROOT, 'translation/images/x'); OUT = os.path.join(ROOT, 'translation/images/ko'); os.makedirs(OUT, exist_ok=True)
FD = os.path.join(ROOT, 'workshop/font')
FONT = {'b': FD + '/NotoSerifKR-Bold.otf', 'sb': FD + '/NotoSerifKR-SemiBold.otf', 'blk': FD + '/NotoSerifKR-Black.otf', 'm': FD + '/NotoSerifKR-Medium.otf'}
L = json.load(open(os.path.join(ROOT, 'translation/images/labels.json'), encoding='utf-8'))
meta = json.load(open(X + '/images_2.json', encoding='utf-8')); cmeta = {(m['id'], m['sn']): m for m in json.load(open(X + '/images_0.json', encoding='utf-8'))}
filt = sys.argv[1:]

def load(p):
    return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)

def render(job, en, ch):
    H, W = en.shape[:2]
    if ch.shape != en.shape:
        c2 = np.zeros_like(en); h, w = min(H, ch.shape[0]), min(W, ch.shape[1]); c2[:h, :w] = ch[:h, :w]; ch = c2
    reg = job.get('region')  # 처리 영역 제한 [x0,y0,x1,y1]
    diff = np.abs(en - ch)[..., :4].max(2) > job.get('thr', 28)
    if reg:
        m = np.zeros_like(diff); m[reg[1]:reg[3], reg[0]:reg[2]] = True; diff &= m
    k = job.get('dil', 3)
    mask = cv2.dilate(diff.astype(np.uint8) * 255, np.ones((2 * k + 1, 2 * k + 1), np.uint8))
    # 배경 합성: 영문 글자 자리는 중문판 배경으로, 둘 다 글자인 곳만 inpaint
    def score(img):
        lum = img[..., :3].mean(2)
        return (lum if job.get('tl', 'light') == 'light' else 255 - lum) * img[..., 3] / 255
    se, sc = score(en), score(ch)
    kk = np.ones((2 * k + 1, 2 * k + 1), np.uint8)
    E = cv2.dilate((diff & (se >= sc)).astype(np.uint8), kk) > 0
    C = cv2.dilate((diff & (sc > se)).astype(np.uint8), kk) > 0
    comp = en.copy(); use_c = E & ~C; comp[use_c] = ch[use_c]
    if job.get('mode') != 'comp': hole = mask; comp = en
    else: hole = ((E & C).astype(np.uint8) * 255)
    rgb = np.clip(comp[..., :3], 0, 255).astype(np.uint8); a = np.clip(comp[..., 3], 0, 255).astype(np.uint8)
    bg_rgb = cv2.inpaint(rgb, hole, 5, cv2.INPAINT_TELEA); bg_a = cv2.inpaint(a, hole, 5, cv2.INPAINT_TELEA)
    if job.get('bg_alpha0'): bg_a[mask > 0] = 0
    bg = np.dstack([bg_rgb, bg_a]).astype(np.float32)
    if job.get('bgmed') is not None: bg = job['bgmed']
    if job.get('bgfile'):
        fn, ox, oy = job['bgfile']; src = load(X + '/en/' + fn); bg = src[oy:oy + H, ox:ox + W].copy()
    if job.get('bgclear'): bg = np.zeros_like(en)
    if job.get('fillsrc') and reg:
        sx0, sx1 = job['fillsrc']; n = sx1 - sx0; bg = en.copy()
        for i, x in enumerate(range(reg[0], reg[2])):
            q, r = divmod(i, n); c = sx0 + (r if q % 2 == 0 else n - 1 - r)
            bg[reg[1]:reg[3], x] = en[reg[1]:reg[3], c]
    # 글자 영역(영문·중문) 측정
    def bbox(img):
        tm = (np.abs(img - bg)[..., :4].max(2) > 40) & (mask > 0)
        ys, xs = np.nonzero(tm)
        return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None
    eb, cb = bbox(en), bbox(ch)
    if not eb and not cb: return Image.fromarray(np.clip(en, 0, 255).astype(np.uint8))
    eb = eb or cb; cb = cb or eb
    ux0, ux1 = min(eb[0], cb[0]), max(eb[2], cb[2]); uy0, uy1 = min(eb[1], cb[1]), max(eb[3], cb[3])
    fill = tuple(job.get('fill', [240, 230, 210])) + (255,)
    stroke = job.get('stroke', 0); scol = tuple(job.get('scol', [20, 15, 10])) + (255,)
    text = job['text']; fp = FONT[job.get('font', 'b')]
    tx0, ty0, tx1, ty1 = job.get('box', [int(eb[0]), int(eb[1]), int(eb[2]), int(eb[3])])
    bw = tx1 - tx0; bh = int(cb[3] - cb[1])
    size = int(job.get('size', bh * job.get('hfac', 1.0)))
    maxw = job.get('maxw', max(bw, 10) * job.get('wfac', 1.0))
    lines = text.split('\n')
    while size > 6:
        f = ImageFont.truetype(fp, size)
        ws = [f.getbbox(t, stroke_width=stroke) for t in lines]
        tw = max(b[2] - b[0] for b in ws); th = sum(b[3] - b[1] for b in ws) + (len(lines) - 1) * size * 0.1
        if tw <= maxw: break
        size -= 1
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    align = job.get('align', 'center')
    cy = (ty0 + ty1) / 2 + job.get('dy', 0); y = cy - th / 2
    for t, b in zip(lines, ws):
        lw = b[2] - b[0]
        x = {'center': (tx0 + tx1) / 2 - lw / 2, 'left': tx0, 'right': tx1 - lw}[align] - b[0] + job.get('dx', 0)
        d.text((x, y - b[1]), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=scol)
        y += b[3] - b[1] + size * 0.1
    base = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), 'RGBA')
    glow = job.get('glow')
    if glow:
        g = layer.split()[3].filter(ImageFilter.GaussianBlur(glow['r']))
        g = g.point(lambda v: min(255, int(v * glow.get('k', 1.6))))
        gl = Image.new('RGBA', (W, H), tuple(glow['c']) + (0,)); gl.putalpha(g)
        base = Image.alpha_composite(base, gl)
    sh = job.get('shadow')
    if sh:
        s = layer.split()[3].filter(ImageFilter.GaussianBlur(sh.get('r', 1.5)))
        sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sl.putalpha(s.point(lambda v: int(v * sh.get('a', 0.8))))
        base = Image.alpha_composite(base, sl.transform(sl.size, Image.AFFINE, (1, 0, -sh.get('o', 2), 0, 1, -sh.get('o', 2))))
    return Image.alpha_composite(base, layer)

done = []; MED = {}
for m in meta:
    key = m['out'].split('__')[0]
    if key not in L: continue
    if filt and not any(key.startswith(p) for p in filt): continue
    job = L[key]
    if isinstance(job, str): job = {'text': job}
    for k2, v in L.get('_group', {}).items():
        if key.startswith(k2): job = {**v, **job}
    if job.get('med'):
        g = key.split('_')[0]
        if g not in MED:
            import glob
            st = []
            if job.get('med') == 3:  # 영문판만, 어두운 글자 마스크(내부 영역)
                y0, y1, x0_, x1_ = job.get('inner', [8, 50, 12, 192])
                for f in glob.glob(X + '/en/' + g + '_*.png'):
                    a = load(f); lum = a[..., :3].mean(2)
                    t = np.zeros(lum.shape, bool); t[y0:y1, x0_:x1_] = lum[y0:y1, x0_:x1_] < 130
                    dm = cv2.dilate(t.astype(np.uint8), np.ones((11, 11), np.uint8)) > 0
                    a = a.copy(); a[dm] = np.nan; st.append(a)
            for f in ([] if job.get('med') == 3 else glob.glob(X + '/en/' + g + '_*.png')):
                a = load(f); b = load(X + '/cht/' + os.path.basename(f))
                dm = cv2.dilate((np.abs(a - b).max(2) > 12).astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
                for im in (a, b):
                    im = im.copy(); im[dm] = np.nan; st.append(im)
            md = np.nanmedian(np.stack(st), 0)
            hole = np.isnan(md).any(2)
            md = np.nan_to_num(md)
            if hole.any() and job.get('med') in (2, 3):  # 거울 타일로 질감 메우기
                xs = np.nonzero(hole.any(0))[0]; x0, x1 = xs.min(), xs.max() + 1
                sw = job.get('strip', 30); s0 = max(0, x0 - sw); strip = md[:, s0:x0].copy(); n = strip.shape[1]
                for i, x in enumerate(range(x0, x1)):
                    q, r = divmod(i, n); md[:, x] = strip[:, n - 1 - r] if q % 2 == 0 else strip[:, r]
                hole[:] = False
            if hole.any():
                h8 = hole.astype(np.uint8) * 255
                md = np.dstack([cv2.inpaint(np.clip(md[..., :3], 0, 255).astype(np.uint8), h8, 5, cv2.INPAINT_TELEA),
                                cv2.inpaint(np.clip(md[..., 3], 0, 255).astype(np.uint8), h8, 5, cv2.INPAINT_TELEA)]).astype(np.float32)
            print(g, 'hole px', int(hole.sum()))
            MED[g] = md
        job['bgmed'] = MED[g]
    en = load(X + '/en/' + m['out']); ch = load(X + '/cht/' + cmeta[(m['id'], m['sn'])]['out'])
    if 'items' in job:
        cur = en
        for it in job['items']:
            sub = {**{k: v for k, v in job.items() if k != 'items'}, **it}
            cur = np.asarray(render(sub, cur, ch)).astype(np.float32)
        im = Image.fromarray(np.clip(cur, 0, 255).astype(np.uint8), 'RGBA')
    else:
        im = render(job, en, ch)
    if Image.open(X + '/en/' + m['out']).mode == 'RGB': im = im.convert('RGB')
    im.save(os.path.join(OUT, m['out'])); done.append(m['out'])
print(len(done))
