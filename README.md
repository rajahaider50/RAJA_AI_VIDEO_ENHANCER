# RAJA AI VIDEO ENHANCER

A Termux-friendly, open-source video processing starter project.

## What works in this release

- Interactive terminal UI.
- Single-video processing and sequential batch processing.
- FFmpeg-based denoise, mild sharpening, color/contrast adjustment and H.264/AAC export.
- Keeps original dimensions up to the configured maximum; it does not falsely claim AI super-resolution.
- Session logs and JSON reports with input/output names, file sizes, pass/fail counts and error details.
- Diagnostics for FFmpeg, FFprobe and optional AI command-line executables.

## Important AI honesty note

Version 1.0.0 does **not** include a bundled AI model or a verified Android/Mali-G57 AI inference pipeline. It detects optional `realesrgan-ncnn-vulkan` and `rife-ncnn-vulkan` executables but does not claim to run them. Real AI upscaling and frame interpolation require compatible Android binaries, model weights, and a tested frame-processing integration. Do not interpret 4K export/resizing as genuine AI detail reconstruction.

## Requirements

- Android with Termux (install Termux from a trusted current source such as F-Droid or the official Termux GitHub).
- Python 3
- FFmpeg + FFprobe
- Storage permission for shared media: `termux-setup-storage`

## Install in Termux

From the project directory:

```bash
bash termux-install.sh
```

## Run

```bash
bash run.sh
```

Or directly:

```bash
python raja_enhancer.py
```

## One-command GitHub install/run template

After pushing this repository to your own GitHub account, replace `YOUR_GITHUB_USERNAME` with your username:

```bash
pkg update -y && pkg install -y git && git clone https://github.com/YOUR_GITHUB_USERNAME/RAJA_AI_VIDEO_ENHANCER.git && cd RAJA_AI_VIDEO_ENHANCER && bash termux-install.sh && bash run.sh
```

The repository name and URL must match the repository you actually create.

## Output and reports

- Enhanced videos: `output/`
- Session logs: `data/logs/`
- JSON processing reports: `data/reports/`

A report records file names, pass/fail counts, file sizes and errors. It does not claim subjective image quality scores.

## Processing profiles

- Light: mild contrast and saturation.
- Balanced: conservative denoise, sharpening and color adjustment.
- Detail: stronger denoise and sharpening.

Strong denoising/sharpening can create artifacts. Test a short clip first and compare against the original.

## GitHub push

```bash
git init
git add .
git commit -m "Initial RAJA AI Video Enhancer"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/RAJA_AI_VIDEO_ENHANCER.git
git push -u origin main
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
