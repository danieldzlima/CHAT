import sys, os, math, subprocess, wave, tempfile, shutil
import numpy as np
from PIL import Image, ImageFilter

# Usage: gerar_intro.py logo.png saida.mp4 [vertical|horizontal]
logo_path, out_path = sys.argv[1], sys.argv[2]
orient = sys.argv[3] if len(sys.argv) > 3 else "vertical"
W, H = (1920, 1080) if orient == "horizontal" else (1080, 1920)
FPS, DUR = 30, 4.0
N = int(FPS * DUR)
rng = np.random.default_rng(7)
tmp = tempfile.mkdtemp(prefix="intro_frames_")


# Logo, scaled to ~85% of the frame width (55% in landscape)
logo = Image.open(logo_path).convert("RGBA")
lw = int(W * (0.55 if orient == "horizontal" else 0.85))
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
la = np.asarray(logo).astype(np.float32) / 255.0

# Background: dark navy with a blue (left) / red (right) spotlight behind the logo, LataVéias brand colors
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cy = H * 0.5
d = np.sqrt(((xx - W / 2) / max(W, H) * 1.2) ** 2 + ((yy - cy) / (max(W, H) * 0.6)) ** 2)
spot = np.clip(1 - d * 1.6, 0, 1) ** 2
bg = np.zeros((H, W, 3), np.float32)
bg += np.array([0.015, 0.025, 0.05])
# horizontal blend blue -> red (brand: #2961B3 / #B12327)
mix = np.clip((xx - W * 0.3) / (W * 0.4), 0, 1)[..., None]
BLUE, RED = np.array([0.16, 0.38, 0.70]), np.array([0.69, 0.14, 0.15])
side = BLUE * (1 - mix) + RED * mix
bg += spot[..., None] * side * 0.45
grain = rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)

IMPACT = 1.15  # seconds: logo lands

# Sparks thrown out at impact
NS = 140
sp_x = W / 2 + rng.uniform(-lw / 2, lw / 2, NS)
sp_y = cy + rng.uniform(-40, 40, NS)
ang = rng.uniform(0, 2 * math.pi, NS)
spd = rng.uniform(300, 1300, NS)
sp_vx, sp_vy = np.cos(ang) * spd, np.sin(ang) * spd - 300
sp_life = rng.uniform(0.5, 1.4, NS)

def ease_out(t):
    return 1 - (1 - t) ** 3

def paste(canvas, img_arr, x0, y0):
    h, w = img_arr.shape[:2]
    x1, y1 = max(x0, 0), max(y0, 0)
    x2, y2 = min(x0 + w, W), min(y0 + h, H)
    if x1 >= x2 or y1 >= y2:
        return
    sub = img_arr[y1 - y0:y2 - y0, x1 - x0:x2 - x0]
    a = sub[..., 3:4]
    canvas[y1:y2, x1:x2] = canvas[y1:y2, x1:x2] * (1 - a) + sub[..., :3] * a

for i in range(N):
    t = i / FPS
    frame = bg.copy()

    # Logo entrance: zoom 1.35 -> 1.0 with blur and fade, then a slow push-in
    if t < IMPACT:
        p = ease_out(max(0, (t - 0.25) / (IMPACT - 0.25)))
        scale = 1.35 - 0.35 * p
        alpha = p
        blur = (1 - p) * 18
    else:
        scale = 1.0 + 0.03 * (t - IMPACT) / (DUR - IMPACT)
        alpha, blur = 1.0, 0

    shake = 0
    if IMPACT <= t < IMPACT + 0.25:
        k = 1 - (t - IMPACT) / 0.25
        shake = int(rng.uniform(-14, 14) * k)

    if alpha > 0:
        im = Image.fromarray((la * 255).astype(np.uint8))
        sw = max(1, int(logo.width * scale))
        im = im.resize((sw, int(logo.height * scale)), Image.LANCZOS)
        if blur > 0.5:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        arr = np.asarray(im).astype(np.float32) / 255.0
        arr[..., 3] *= alpha

        # Metallic shine sweep across the letters
        ts = (t - 1.6) / 0.8
        if 0 <= ts <= 1:
            h, w = arr.shape[:2]
            gx = np.arange(w)[None, :] + np.arange(h)[:, None] * 0.5
            center = -0.2 * w + ts * 1.6 * w
            band = np.exp(-((gx - center) / (w * 0.05)) ** 2)[..., None]
            arr[..., :3] = arr[..., :3] + (1 - arr[..., :3]) * band * 0.85

        # Soft glow under the logo, blue on the left and red on the right
        glow = np.asarray(im.filter(ImageFilter.GaussianBlur(30))).astype(np.float32)[..., 3:4] / 255.0
        gm = np.clip(np.linspace(-0.4, 1.4, glow.shape[1]), 0, 1)[None, :, None]
        gcol = np.array([0.25, 0.5, 1.0]) * (1 - gm) + np.array([1.0, 0.2, 0.2]) * gm
        g = np.concatenate([np.ones_like(glow) * gcol, glow * 0.45 * alpha], axis=-1)
        x0 = (W - arr.shape[1]) // 2 + shake
        y0 = int(cy - arr.shape[0] / 2) + shake // 2
        paste(frame, g.astype(np.float32), x0, y0)
        paste(frame, arr, x0, y0)

    # Sparks
    if t >= IMPACT:
        dt = t - IMPACT
        alive = dt < sp_life
        px = sp_x + sp_vx * dt
        py = sp_y + sp_vy * dt + 0.5 * 1800 * dt ** 2
        fade = np.clip(1 - dt / sp_life, 0, 1)
        for x, y, f, a in zip(px, py, fade, alive):
            if not a:
                continue
            xi, yi = int(x), int(y)
            if 2 <= xi < W - 2 and 2 <= yi < H - 2:
                frame[yi - 2:yi + 2, xi - 2:xi + 2] = np.maximum(
                    frame[yi - 2:yi + 2, xi - 2:xi + 2], np.array([0.85, 0.92, 1.0]) * f)

    # Impact flash
    if IMPACT <= t < IMPACT + 0.2:
        frame += (1 - (t - IMPACT) / 0.2) * 0.35

    # Fade from / to black
    fade = min(1.0, t / 0.25, (DUR - t) / 0.4)
    frame = (frame + grain * 0.8) * max(fade, 0)

    Image.fromarray((np.clip(frame, 0, 1) * 255).astype(np.uint8)).save(f"{tmp}/f{i:04d}.png")

# Sound: whoosh building to a metallic boom at the impact
SR = 44100
n = int(SR * DUR)
ts = np.arange(n) / SR
audio = np.zeros(n)
noise = rng.normal(0, 1, n)
# whoosh: filtered noise swelling up to impact
env_w = np.clip((ts - 0.2) / (IMPACT - 0.2), 0, 1) ** 2 * (ts < IMPACT)
lp = np.convolve(noise, np.ones(40) / 40, mode="same")
audio += lp * env_w * 0.9
# boom: decaying low sine + metallic ring
dt = np.clip(ts - IMPACT, 0, None)
on = ts >= IMPACT
audio += on * np.sin(2 * np.pi * (55 + 40 * np.exp(-dt * 8)) * dt) * np.exp(-dt * 3.5) * 0.9
for f, a in [(523, 0.12), (1187, 0.08), (2311, 0.05)]:
    audio += on * np.sin(2 * np.pi * f * dt) * np.exp(-dt * 2.5) * a
audio += on * noise * np.exp(-dt * 25) * 0.4
audio *= np.clip((DUR - ts) / 0.4, 0, 1)
audio = audio / np.max(np.abs(audio)) * 0.8
wav = f"{tmp}/sfx.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((audio * 32767).astype(np.int16).tobytes())

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.png",
                "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_path], check=True)
print("ok", out_path)
shutil.rmtree(tmp)
