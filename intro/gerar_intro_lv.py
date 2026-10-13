# Intro LataVéias para YouTube (1920x1080): o "LV" do emblema bate na tela,
# vira o L e o V do letreiro, o nome se abre entre eles e encaixa na capa.
# Uso: python3 gerar_intro_lv.py  (lê e grava os arquivos desta pasta)
import os, math, subprocess, tempfile, shutil, wave
import numpy as np
import cv2
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1920, 1080, 30, 6.7
N = int(FPS * DUR)
rng = np.random.default_rng(11)


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def clamp01(t):
    return min(max(t, 0.0), 1.0)


# ---------- Emblema: recorta as letras prateadas "LV" da foto de perfil ----------
prof = cv2.imread(f"{HERE}/perfil-lv.jpg")
hsv = cv2.cvtColor(prof, cv2.COLOR_BGR2HSV)
s, v = hsv[..., 1].astype(int), hsv[..., 2].astype(int)
yy, xx = np.mgrid[0:prof.shape[0], 0:prof.shape[1]]
m = (s < 75) & (v > 40)
m &= ((xx - 1000) ** 2 + (yy - 1000) ** 2) < 860 ** 2
m &= yy < 1340
m &= ~((yy > 920) & (xx > 1290))   # moto
m &= ~((yy > 1110) & (xx < 1060))  # carro
m = m.astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
lab, n = ndi.label(m)
m = (lab == 1 + np.argmax(ndi.sum(m, lab, range(1, n + 1)))).astype(np.uint8) * 255
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((25, 25), np.uint8))
cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
poly = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 10, True)
pm = np.zeros_like(m)
cv2.fillPoly(pm, [poly], 255)
pm = cv2.GaussianBlur(pm, (5, 5), 0)
x, y, w, h = cv2.boundingRect(poly)
emb = np.dstack([prof[y:y + h, x:x + w], pm[y:y + h, x:x + w]]).astype(np.float32) / 255.0
EMB_H = 560  # altura do emblema na tela

# ---------- Letreiro: separa cada letra do PNG ----------
logo = cv2.imread(f"{HERE}/logo-lataveias.png", cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0
LH, LW = logo.shape[:2]
solid = logo[..., 3] > 40 / 255
lab, n = ndi.label(solid)
_, (iy, ix) = ndi.distance_transform_edt(lab == 0, return_indices=True)
owner = lab[iy, ix]  # cada pixel pertence à letra mais próxima
comps = []
for i, o in enumerate(ndi.find_objects(lab)):
    if (lab[o] == i + 1).sum() < 30:
        continue
    cx = (o[1].start + o[1].stop) / 2
    comps.append({"id": i + 1, "cx": cx, "cy": (o[0].start + o[0].stop) / 2, "x0": o[1].start})
L = min(comps, key=lambda c: c["x0"])
V = min((c for c in comps if c["x0"] > 250), key=lambda c: c["x0"])
middle = sorted((c for c in comps if L["x0"] < c["x0"] and c["cx"] < V["x0"]), key=lambda c: c["cx"])
trail = sorted((c for c in comps if c["cx"] > V["cx"] + 5), key=lambda c: c["cx"])
V_SHIFT = (L["x0"] + 60) - V["x0"]  # no monograma o V encosta no L, como no emblema
for c in comps:
    c["layer"] = logo * (owner == c["id"])[..., None]


def word_layer(p):
    """Letreiro em resolução do PNG; p=0 só L+V juntos, p=1 nome completo."""
    out = np.zeros_like(logo)
    e = ease_out(p)
    shift = V_SHIFT * (1 - e)
    groups = [(L, 0, 1.0), (V, shift, 1.0)]
    for k, c in enumerate(middle):
        groups.append((c, 0, clamp01((p - 0.15 - k * 0.12) / 0.35)))
    for k, c in enumerate(trail):
        groups.append((c, shift, clamp01((p - 0.25 - k * 0.09) / 0.35)))
    for c, dx, a in groups:
        if a <= 0:
            continue
        lay = c["layer"]
        sc = 0.5 + 0.5 * ease_out(a)
        M = np.float32([[sc, 0, (1 - sc) * c["cx"] + dx], [0, sc, (1 - sc) * c["cy"]]])
        lay = cv2.warpAffine(lay, M, (LW, LH), flags=cv2.INTER_LINEAR)
        lay[..., 3] *= a
        al = lay[..., 3:4]
        out[..., :3] = out[..., :3] * (1 - al) + lay[..., :3] * al
        out[..., 3:4] = out[..., 3:4] + al * (1 - out[..., 3:4])
    return out


# ---------- Fundo: a capa do canal ----------
cover = cv2.resize(cv2.imread(f"{HERE}/capa-lataveias.jpg"), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
cover_blur = cv2.GaussianBlur(cover, (0, 0), 22)
# posição do letreiro dentro da capa (achada por template matching: x=787, y=514, largura 442 em 2000px)
CS = W / 2000
FINAL_S = 442 * CS / LW
FINAL_X, FINAL_Y = 787 * CS, 514 * CS

gx = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
glow_col = (1 - gx) * np.array([1.0, 0.45, 0.15], np.float32) + gx * np.array([0.15, 0.15, 1.0], np.float32)  # BGR: azul -> vermelho
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vign = np.clip(1 - (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 1.3, 0, 1)[..., None]
grain = rng.normal(0, 0.01, (H, W, 1)).astype(np.float32)


def shine(arr, t, t0, t1):
    ts = (t - t0) / (t1 - t0)
    if not 0 <= ts <= 1:
        return arr
    h, w = arr.shape[:2]
    g = np.arange(w)[None, :] + np.arange(h)[:, None] * 0.6
    c = -0.2 * w + ts * 1.6 * w
    band = np.exp(-((g - c) / (w * 0.05)) ** 2)[..., None].astype(np.float32)
    arr = arr.copy()
    arr[..., :3] += (1 - arr[..., :3]) * band * 0.8
    return arr


def paste(canvas, arr, x0, y0, alpha=1.0):
    h, w = arr.shape[:2]
    x1, y1, x2, y2 = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if x1 >= x2 or y1 >= y2:
        return
    sub = arr[y1 - y0:y2 - y0, x1 - x0:x2 - x0]
    a = sub[..., 3:4] * alpha
    canvas[y1:y2, x1:x2, :3] = canvas[y1:y2, x1:x2, :3] * (1 - a) + sub[..., :3] * a
    canvas[y1:y2, x1:x2, 3:4] = canvas[y1:y2, x1:x2, 3:4] + a * (1 - canvas[y1:y2, x1:x2, 3:4])


def resized(arr, sw, sh):
    interp = cv2.INTER_AREA if sw < arr.shape[1] else cv2.INTER_LANCZOS4
    out = cv2.resize(arr, (max(1, sw), max(1, sh)), interpolation=interp)
    if sw > arr.shape[1] * 1.3:  # devolve um pouco de nitidez ao ampliar
        bl = cv2.GaussianBlur(out[..., :3], (0, 0), 1.5)
        out[..., :3] = np.clip(out[..., :3] * 1.6 - bl * 0.6, 0, 1)
    return np.clip(out, 0, 1)


class Sparks:
    def __init__(self, t0, cx, cy, spread, n, speed):
        self.t0 = t0
        self.x = cx + rng.uniform(-spread, spread, n)
        self.y = cy + rng.uniform(-spread * 0.3, spread * 0.3, n)
        a = rng.uniform(0, 2 * math.pi, n)
        sp = rng.uniform(speed * 0.25, speed, n)
        self.vx, self.vy = np.cos(a) * sp, np.sin(a) * sp - 250
        self.life = rng.uniform(0.4, 1.3, n)

    def draw(self, frame, t):
        dt = t - self.t0
        if dt < 0:
            return
        px = self.x + self.vx * dt
        py = self.y + self.vy * dt + 900 * dt ** 2
        f = np.clip(1 - dt / self.life, 0, 1)
        for X, Y, F in zip(px, py, f):
            if F <= 0:
                continue
            xi, yi = int(X), int(Y)
            if 2 <= xi < W - 2 and 2 <= yi < H - 2:
                col = glow_col[0, xi] * 0.6 + 0.5
                frame[yi - 2:yi + 2, xi - 2:xi + 2] = np.maximum(frame[yi - 2:yi + 2, xi - 2:xi + 2], col * F)


IMPACT, MORPH, REVEAL0, REVEAL1, SETTLE0, SETTLE1 = 1.1, 2.3, 2.55, 3.55, 4.1, 5.0
sparks = [Sparks(IMPACT, W / 2, H / 2, 330, 180, 1300), Sparks(MORPH, W / 2, H / 2, 140, 70, 800)]

tmp = tempfile.mkdtemp(prefix="intro_lv_")
emb_ar = emb.shape[1] / emb.shape[0]
for i in range(N):
    t = i / FPS
    fg = np.zeros((H, W, 4), np.float32)
    shake = 0
    if IMPACT <= t < IMPACT + 0.25:
        shake = int(rng.uniform(-16, 16) * (1 - (t - IMPACT) / 0.25))

    # 1) Emblema LV: entra com zoom e desfoque, bate, brilha, depois encolhe e some
    if t < MORPH + 0.15:
        if t < IMPACT:
            p = ease_out((t - 0.3) / (IMPACT - 0.3))
            sc, a, blur = 1.45 - 0.45 * p, p, (1 - p) * 16
        else:
            k = smooth((t - 2.1) / (MORPH + 0.15 - 2.1))
            sc, a, blur = (1 + 0.04 * (t - IMPACT)) * (1 - 0.45 * k), 1 - k, 0
        if a > 0.01:
            eh = int(EMB_H * sc)
            arr = resized(emb, int(eh * emb_ar), eh)
            if blur > 0.5:
                arr = cv2.GaussianBlur(arr, (0, 0), blur)
            arr = shine(arr, t, 1.35, 2.0)
            paste(fg, arr, (W - arr.shape[1]) // 2 + shake, (H - arr.shape[0]) // 2 + shake // 2, a)

    # 2) Letreiro: L+V viram o nome inteiro e depois encaixam na capa
    if t >= MORPH - 0.1:
        a = smooth((t - (MORPH - 0.1)) / 0.2)
        p = clamp01((t - REVEAL0) / (REVEAL1 - REVEAL0))
        S = 2.4 + (1.7 - 2.4) * smooth(p)
        pop = 1 + 0.25 * (1 - ease_out((t - (MORPH - 0.1)) / 0.4))
        S *= pop
        cx = (L["x0"] + (V["x0"] + V_SHIFT + 91)) / 2 * (1 - ease_out(p)) + (L["x0"] + LW - 7) / 2 * ease_out(p)
        ox, oy = W / 2 - cx * S, H / 2 - LH / 2 * S
        k = smooth((t - SETTLE0) / (SETTLE1 - SETTLE0))
        ox, oy, S = ox + (FINAL_X - ox) * k, oy + (FINAL_Y - oy) * k, S + (FINAL_S - S) * k
        wl = word_layer(p)
        wl = shine(wl, t, 3.55, 4.05)
        arr = resized(wl, int(LW * S), int(LH * S))
        fade = 1 - smooth((t - 5.1) / 0.35)  # some e deixa o letreiro da própria capa
        paste(fg, arr, int(round(ox)), int(round(oy)), a * fade)

    # Fundo: capa escura e desfocada que vai aparecendo nítida
    r = smooth((t - SETTLE0) / (SETTLE1 + 0.1 - SETTLE0))
    bg = cover_blur * (0.16 + 0.1 * smooth((t - IMPACT) / 0.3)) * (1 - r) + cover * r
    bg = bg * (vign * (1 - r) + r)

    # Brilho colorido atrás das letras (azul à esquerda, vermelho à direita)
    glow = cv2.GaussianBlur(fg[..., 3], (0, 0), 28)[..., None]
    frame = bg + glow_col * glow * 0.55 * (1 - r * 0.7)
    frame = frame * (1 - fg[..., 3:4]) + fg[..., :3] * fg[..., 3:4]

    for sp in sparks:
        sp.draw(frame, t)

    for t0, amp in ((IMPACT, 0.4), (MORPH, 0.3)):
        if t0 <= t < t0 + 0.2:
            frame += (1 - (t - t0) / 0.2) * amp

    fade = min(1.0, t / 0.25, (DUR - t) / 0.5)
    frame = (frame + grain) * max(fade, 0)
    cv2.imwrite(f"{tmp}/f{i:04d}.png", (np.clip(frame, 0, 1) * 255).astype(np.uint8))

# ---------- Som ----------
SR = 44100
ts = np.arange(int(SR * DUR)) / SR
noise = rng.normal(0, 1, ts.size)
lp = np.convolve(noise, np.ones(40) / 40, mode="same")
hp = noise - lp
audio = np.zeros_like(ts)


def whoosh(t0, t1, amp, src):
    env = np.clip((ts - t0) / (t1 - t0), 0, 1) ** 2 * (ts < t1)
    return src * env * amp


def after(t0):
    return np.clip(ts - t0, 0, None), ts >= t0


audio += whoosh(0.2, IMPACT, 1.0, lp)
dt, on = after(IMPACT)
audio += on * np.sin(2 * np.pi * (50 + 45 * np.exp(-dt * 8)) * dt) * np.exp(-dt * 3.5) * 1.0
for f, a in [(523, 0.12), (1187, 0.08), (2311, 0.05)]:
    audio += on * np.sin(2 * np.pi * f * dt) * np.exp(-dt * 2.5) * a
audio += on * noise * np.exp(-dt * 25) * 0.4
audio += whoosh(1.9, MORPH, 0.35, hp)
dt, on = after(MORPH)
for f, a in [(2637, 0.10), (3520, 0.08), (5274, 0.05)]:
    audio += on * np.sin(2 * np.pi * f * dt) * np.exp(-dt * 3) * a
audio += on * hp * np.exp(-dt * 18) * 0.25
audio += whoosh(REVEAL0, REVEAL1, 0.35, lp) * (ts < REVEAL1)
audio += whoosh(SETTLE0, SETTLE1, 0.5, lp)
dt, on = after(SETTLE1)
audio += on * np.sin(2 * np.pi * (45 + 20 * np.exp(-dt * 6)) * dt) * np.exp(-dt * 2.2) * 0.6
audio *= np.clip((DUR - ts) / 0.5, 0, 1)
audio = audio / np.max(np.abs(audio)) * 0.8
with wave.open(f"{tmp}/sfx.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((audio * 32767).astype(np.int16).tobytes())

out = f"{HERE}/intro-lataveias-lv-youtube.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.png",
                "-i", f"{tmp}/sfx.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
shutil.rmtree(tmp)
print("ok", out)
