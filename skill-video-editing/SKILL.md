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

Use this only when Daniel asks for "o estilo da referência", "estilo oficina" or similar. It comes **after** the rough cut. It never replaces the LataVéias continuity rule above.

The reference is a 22-min, 16:9 Brazilian car-workshop vlog: GoPro in hand, several people talking while they work, close-ups of the process. It feels **real and live, not commercial**. It has 296 cuts (median 3 s per shot, ~3.5 s in the first 15 min, ~9 s in the closing sponsor block) and only 3 silences in 22 min.

## Where the fast rhythm applies (LataVéias)

- **Workshop / explanation / build segments**: fast rhythm is OK (rough cut with default `--min-sil`).
- **Driving / conversation in the car**: keep continuity. Use `--min-sil 0.6` or more, `--protect` on the conversation, and no jump cuts mid-sentence.
- Before running, show Daniel which segments you will treat as workshop and which as driving, and confirm.

## Rhythm and structure

- **Hook in the first 3–5 s**: someone talking straight to the camera and promising what will happen. No long intro.
- In the middle, cycle **talk → close-up of the detail → reaction**.
- Repetitive manual work (sanding, welding, taking things apart) → speed up 2x–4x: `setpts=PTS/3`, plus `atempo=2,atempo=1.5` for the audio or mute it.
- **Closing block**: a wider, steadier shot, longer takes (~9 s): the result of the day, a call to subscribe, the card on screen.
- Short ending, no long end screen.

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
