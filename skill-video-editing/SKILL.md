---
name: video-editing
description: Rough-cut a talking-head video (TikTok, Reels, Shorts, YouTube): joins clips, cuts silences and retakes, never cuts inside a word, transcribes. Then applies Daniel's reference style pass (workshop-vlog look, LataVéias brand colors, whip transitions, creator card). Use for "edit my video", "cut the silences", "remove my retakes", "corta os silêncios", "edita no estilo da referência".
---

# Video editing (rough cut + style pass)

Source: https://github.com/vincentventalon/claude-code-video-editing-skill (MIT). This skill's script lives in that repo. Before the first run in a session, get it:

```sh
git clone --depth 1 https://github.com/vincentventalon/claude-code-video-editing-skill video-editing-skill
```

The script is then `video-editing-skill/scripts/edit_video.py`.

## Important for Daniel's car vlogs (LataVéias)

This tool cuts silences and retakes. For driving vlogs where continuity matters (no jump cuts mid-conversation), do NOT run it on the whole video by default. Use it only when he asks for a silence/retake cut, or run it with a high `--min-sil` and `--protect` windows, and confirm with him first.

## Big files on Daniel's PC

Videos are often several GB on his Windows Desktop and cannot be brought into the cloud workspace (400 MB limit). In that case, run the script on his PC: write a `.bat` that calls `python edit_video.py ...` (or the tools in `Desktop\vlog_edicao\tools`), let him double-click it, and read the logs/outputs back. In PowerShell arrays, separate items with commas. When changing a file already on his PC, save it under a new name.

## The command

```sh
python scripts/edit_video.py clip1.MP4 clip2.MP4 -o edited.mp4 --lang pt
```

It joins the clips in order and splits the sound into islands (whatever lies between two silences). It transcribes each island and drops islands with no words and false starts: when a sentence is said several times, only the last take is kept. Then it renders `edited.mp4` and writes `edited.txt`, `edited.srt` and `edited.takes.tsv` (every island, kept or not, with its text). Always pass `--lang` (`pt` for Daniel).

## First time: install the tools yourself

| tool | check | Windows | macOS | Linux |
|---|---|---|---|---|
| ffmpeg + ffprobe | `ffmpeg -version` | `winget install Gyan.FFmpeg` or the gyan.dev essentials zip | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| whisper-cli (whisper.cpp) | `whisper-cli --help` | `whisper-bin-x64.zip` from the whisper.cpp v1.7.6 releases, add to PATH | `brew install whisper-cpp` | build from github.com/ggml-org/whisper.cpp |

The model downloads itself on first run into `~/.cache/whisper-cpp/` (from huggingface.co):

- PC with GPU / recent Mac: default `large-v3-turbo` (1.6 GB)
- little disk/RAM: `--model large-v3-turbo-q5_0` (0.57 GB)
- CPU only / too slow: `--model small` (0.49 GB)

## What to do

1. Find the clips and run the command.
2. Read the output: duration before/after, retakes cut (with quoted words), and `to check at 12.3s` lines.
3. Read the takes like an editor. Open `edited.takes.tsv` and read the `kept` lines in order. Look for sentences that were abandoned and restated in other words, or lone fragments. If you find any, re-run with `--cut A:B` and the same `-o` (this only re-renders). When in doubt, keep. Never cut something just because it is off topic, a joke or an aside.
4. If Daniel asked for the reference style, do the **style pass** below on the rough cut.
5. Hand back the video path, what was cut and why, and any `to check` times.

## Settings

| Setting | Default | When to change |
|---|---|---|
| `--min-sil` | 0.22 s | edit feels breathless → 0.35; pauses left → 0.18 |
| `--noise` | 32 dB | background noise (car, street) and nothing is cut → 25 |
| `--model` | large-v3-turbo | see above |

`--cut A:B` removes a window and `--protect A:B` keeps one (a comedic pause), in joined-footage times as in `edited.takes.tsv`. `--pad 0.08` keeps more air around each island. `--keep-retakes` keeps every take, `--keep-fillers` keeps lone "um"s, and `--no-transcript` skips whisper (silences only).

## When it fails

- `ffmpeg` or `whisper-cli` not found → install, reopen the terminal. Without whisper it still cuts silences.
- 0 s video or `concat` error → the clips have different formats; edit each alone or re-encode first.
- `nothing kept` → very quiet recording: `--noise 25`.

---

# Style pass — reference: workshop vlog (Lucas Fontana style)

Use this when Daniel asks for "o estilo da referência", "estilo oficina" or a full edit of a LataVéias video. It comes **after** the rough cut. It never replaces the LataVéias continuity rule above.

The reference is a 22-min, 16:9 Brazilian car-workshop vlog: GoPro in hand, several people talking while they work, close-ups of the process. It feels **real and live, not commercial**. It has 296 cuts (median 3 s per shot, ~3.5 s in the first 15 min, ~9 s in the closing sponsor block) and only 3 silences in 22 min.

## Daniel's videos (LataVéias)

He films **alone**, holding the camera or with it mounted in the car. There are four formats, and often several in one video. Before cutting, tell Daniel which format each part is and confirm.

| Format | Cut rhythm | What matters |
|---|---|---|
| **Driving** (showing something while he drives) | Continuity: `--min-sil 0.6`+, `--protect` on what he's saying, no jump cut mid-sentence | Engine sound, road, the car responding |
| **Part that arrived** (unboxing, explaining the part) | Fast, like the reference: default `--min-sil` | Close-ups of the part, the box, details, the brand |
| **Next upgrades** (plans) | Medium: `--min-sil 0.35` | Show the place on the car where the part goes, while he talks |
| **Result after maintenance/upgrade** (how it turned out) | Fast showing it, continuity when driving | **Before vs after** |

### Rules for each format
- **Driving**:
  - The engine is almost as important as the voice. Don't push the car sound under the voice. Lower it only where the voice gets drowned out.
  - Clean wind and road noise off the voice with the `video-cleanup` skill before the style pass.
  - Speed up (2x–4x) only stretches of road **with no talking**.
  - Never cut in the middle of a gear change or an acceleration he is showing.
- **Part that arrived**: talk → close-up of the part → back to his face. If there is no close-up B-roll, use a slow zoom (punch-in 110–120%) on the shot itself to vary it: `zoompan` or `crop` + `scale`.
- **Next upgrades**: when he names a part or a place on the car and there is footage of it, put it over the voice as B-roll, with the audio still his voice.
- **Before vs after**:
  - Look for "before" footage in the same video or in clips Daniel points to.
  - Do a side-by-side (`hstack`) or a hard cut before → after with a whip transition.
  - Text "ANTES" / "DEPOIS" in a red box (`#B12327`).
  - For a sound upgrade (exhaust, intake), put the before and after sound one after the other.

## Rhythm and structure
- **Hook in the first 3–5 s**: Daniel talking to the camera, or the best moment of the video (the result, the engine sound, the part) as a teaser.
- **Then the intro**, after the hook, never at second 0. See "Intro" below.
- In the middle, follow the format's rhythm from the table above.
- **Closing**: the result or the conclusion, a call to subscribe with the card on screen, ~10 s. No long end screen.

## Intro

Files are in the CHAT repo, folder `intro/` (on Daniel's PC, keep a copy in `Desktop\vlog_edicao\`):

| File | Use |
|---|---|
| `intro-lataveias-youtube-azul.mp4` | **default for YouTube**, Daniel's favorite (1920×1080, 4 s, logo lands with blue/red brand light) |
| `intro-lataveias-azul.mp4` | the same in vertical (1080×1920, 4 s), for Shorts/Reels |
| `intro-lataveias-lv-youtube.mp4` | alternative (6.7 s, the LV emblem turns into the logo) |
| `intro-lataveias-youtube.mp4` / `intro-lataveias.mp4` | old gold versions, don't use |

To change the intro's colors, regenerate it with `python gerar_intro.py logo-lataveias.png <out>.mp4 horizontal|vertical` (colors in the `BLUE`/`RED` variables).

Insert it after the hook (tested; the intro is scaled to the video's resolution and fps):
```sh
ffmpeg -i hook.mp4 -i intro-lataveias-youtube-azul.mp4 -i rest.mp4 -filter_complex "[1:v]scale=<W>:<H>:flags=lanczos,fps=<FPS>,setsar=1,format=yuv420p[iv];[0:v]setsar=1,format=yuv420p[v0];[2:v]setsar=1,format=yuv420p[v2];[1:a]aresample=48000,aformat=channel_layouts=stereo[ia];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[2:a]aresample=48000,aformat=channel_layouts=stereo[a2];[v0][a0][iv][ia][v2][a2]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" ...
```
Split the edited video into `hook` (first 3–5 s, cut at the end of a sentence) and `rest` with `-ss`/`-t` before this step.

## Transitions (90% hard cuts)

Transitions are seasoning. Use at most one every ~1–2 min.

**Whip / blur** (change of subject or place), tested:
```sh
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=hblur:duration=0.35:offset=<duration_of_a - 0.35>[v];[0:a][1:a]acrossfade=d=0.35[a]" -map "[v]" -map "[a]" out.mp4
```
Add a whoosh SFX on the transition if Daniel has one.

**Tilted frame + picture-in-picture** (joke / comment / meme), tested:
```sh
ffmpeg -i main.mp4 -i meme.mp4 -filter_complex "[0:v]scale=iw*0.85:-2,rotate=-6*PI/180:ow=<W>:oh=<H>:c=black[t];[1:v]scale=<W/4>:-2[p];[t][p]overlay=W-w-40:40[v]" -map "[v]" -map 0:a out.mp4
```

Never use template transitions (cube, page turn, long dissolve).

## Color grading — LataVéias brand colors

Use the colors of Daniel's LataVéias logo (`intro/perfil-lv.jpg`, `intro/logo-lataveias.png` in the CHAT repo):
- **Navy / electric blue** `#04183D` (shadows) → `#2961B3` (accent)
- **Racing red** `#B12327`
- **Brushed steel** `#B8BBC2` / `#F5F6F6` (neutral highlights)

The look: neutral, clean steel highlights (no yellow) and shadows pulled slightly toward navy. **Blue and red pop** (car paint, caps, tools), while the other colors stay a bit desaturated so the brand colors stand out. Medium-high contrast, no grain, no heavy vignette.

Tested filter (ffmpeg 6+):
```sh
-vf "eq=contrast=1.15:gamma=0.96:saturation=0.9,colorbalance=bs=0.05:bm=0.03:rh=-0.03,huesaturation=saturation=0.45:colors=b+c+m,huesaturation=saturation=0.4:colors=r,unsharp=5:5:0.5"
```
- If skin gets too red, lower the second `huesaturation` to 0.2.
- Night or driving footage with dark shadows: use `bs=0.03` so the blacks don't go blue.
- On older ffmpeg without `huesaturation`, use `eq=contrast=1.15:saturation=1.15,colorbalance=bs=0.05:rh=-0.03`.

Export one comparison frame (before | after, `hstack`), show Daniel, and only then render the whole thing.

## Overlays

- **Creator card**: `intro/card-lataveias.png` in the CHAT repo (transparent PNG, 420×520). It has the round LV avatar with a blue/red ring, the LataVéias wordmark and a red INSCREVA-SE button. It sits bottom-left at ~26% of the frame height. Tested:
  ```sh
  -i card-lataveias.png -filter_complex "[1:v][0:v]scale2ref=w=oh*mdar:h=ih*0.26[c][v];[v][c]overlay=x=W*0.025:y=H-h-H*0.03"
  ```
  Don't keep it on all the time. Show it in the first ~10 s, then for ~8 s every ~3 min, and again at the end: add `:enable='between(t,0,10)+between(t,180,188)+...'` to the `overlay`. A fade (`fade=in:st=0:d=0.3:alpha=1`) on the card stream before scaling makes it smoother.
- **No QR code and no sponsor tags** (LataVéias has neither for now). If a sponsor appears later, ask Daniel for the logo PNG.
- On-screen text: FreeSans Bold Oblique or Montserrat ExtraBold Italic, white with a dark shadow. Red `#B12327` boxes for highlights, matching the INSCREVA-SE button.
- **No running TikTok-style captions** in the horizontal version. On-screen text is only for a name or a one-off joke. If a vertical cut (Reels/Shorts) is asked for, use the `.srt` the script generates as running captions.
- Never cover a face or the main part with an overlay.

## Audio

- The voice is the star: final loudness **-14 LUFS** (`loudnorm=I=-14:TP=-1.5:LRA=11`). The reference measures -15.4 LUFS.
- Keep the workshop ambient sound (tools, welding, laughter).
- Background music low (−20 to −25 dB under the voice), rising only on whips and sped-up parts.

---

# Preview, export and extras

## Preview before the final render
Daniel's files are several GB. Before the full render on his PC, make a **fast 480p preview** with the cuts, the color and the card:
```sh
-vf "scale=-2:480,<grade>" -c:v libx264 -preset veryfast -crf 28 -c:a aac -b:a 128k preview.mp4
```
He approves it, and only then do you render the final file.

## Export
- **Keep the resolution and fps of the original footage. Never lower them.**
  - Recorded in **4K** → export in **4K** (3840×2160). On YouTube, a 4K upload gets the better codec (VP9/AV1) and a higher bitrate, so it looks sharper even for people watching at 1080p.
  - Recorded in **1080p** → export in 1080p. Upscaling to 4K only adds a little sharpness on YouTube, with a much bigger file and a slower render, so do it only if Daniel asks.
- Check the source with `ffprobe` before choosing.
- The intro and the card are 1080p. In a 4K video, scale them with `flags=lanczos` (already in the commands above).
- Settings:
  - 4K: `-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p` (or `-c:v h264_nvenc -cq 19` if the PC has an NVIDIA GPU, which is much faster).
  - 1080p: the same with `-crf 18`.
  - Audio: `-c:a aac -b:a 192k -ar 48000` + `loudnorm=I=-14:TP=-1.5:LRA=11`.
  - Always add `-movflags +faststart`.
- Always save under a **new name** (`<name>_final_4k.mp4`). Never overwrite the original.

## Deliver with the video (from the `.txt`/`.srt` the script generates)
1. **YouTube chapters** with times (`00:00 Intro`, `00:45 A peça chegou`...), already adjusted for the hook + intro.
2. **3 title suggestions** in Daniel's style (direct, curious, with the car's name).
3. **3–5 thumbnail frames**: moments with a clear expression or the part/car in focus. Export them as PNGs at full resolution.

## Short version (Shorts/Reels), when Daniel asks
- Pick 1–3 moments of 30–60 s that stand alone: the result, the engine sound, the part being opened.
- Reframe to 9:16 (`crop=ih*9/16:ih`, centered on Daniel or the part).
- Running captions from the `.srt` (white bold italic, active word in red `#B12327`).
- The vertical intro `intro-lataveias-azul.mp4` is optional. In Shorts it's better to start on the action and put the intro at the end, or leave it out.
