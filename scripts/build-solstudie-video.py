#!/usr/bin/env python3
"""Build smooth solstudie videos from frames using ffmpeg interpolation."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg not found. Install ffmpeg (brew install ffmpeg) and try again.")


def build_filter(target_fps: int, grade: str) -> str:
    filters = [
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        f"minterpolate=fps={target_fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
    ]

    if grade == "cinematic":
        filters.extend(
            [
                "eq=contrast=1.08:brightness=0.02:saturation=1.08",
                "colorbalance=rs=0.015:gs=0.005:bs=-0.01:rm=0.01:gm=0.0:bm=-0.01",
                "vignette=PI/6",
            ]
        )
    elif grade == "soft":
        filters.extend(
            [
                "eq=contrast=1.04:brightness=0.01:saturation=1.04",
                "colorbalance=rs=0.01:gs=0.0:bs=-0.005:rm=0.008:gm=0.0:bm=-0.005",
                "vignette=PI/7",
            ]
        )

    filters.append("format=yuv420p")
    return ",".join(filters)


def build_video_mp4(
    series_id: str,
    frames_dir: Path,
    output_dir: Path,
    input_fps: float,
    target_fps: int,
    grade: str,
) -> Path:
    pattern = f"{series_id}-*.png"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{series_id}.mp4"

    vf = build_filter(target_fps, grade)

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(input_fps),
        "-pattern_type",
        "glob",
        "-i",
        str(frames_dir / pattern),
        "-vf",
        vf,
        "-r",
        str(target_fps),
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    run(cmd)
    return output_path


def build_video_webm(
    series_id: str,
    frames_dir: Path,
    output_dir: Path,
    input_fps: float,
    target_fps: int,
    grade: str,
) -> Path:
    pattern = f"{series_id}-*.png"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{series_id}.webm"

    vf = build_filter(target_fps, grade)

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(input_fps),
        "-pattern_type",
        "glob",
        "-i",
        str(frames_dir / pattern),
        "-vf",
        vf,
        "-r",
        str(target_fps),
        "-c:v",
        "libvpx-vp9",
        "-crf",
        "32",
        "-b:v",
        "0",
        "-deadline",
        "good",
        "-cpu-used",
        "4",
        str(output_path),
    ]

    run(cmd)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build smooth solstudie videos from frames.")
    parser.add_argument(
        "--manifest",
        default="dashboard/data/solstudie.json",
        help="Path to solstudie manifest",
    )
    parser.add_argument(
        "--frames-dir",
        default="dashboard/assets/solstudie/frames",
        help="Directory containing PNG frames",
    )
    parser.add_argument(
        "--output-dir",
        default="dashboard/assets/solstudie/video",
        help="Output directory for MP4 videos",
    )
    parser.add_argument(
        "--grade",
        choices=["cinematic", "soft", "none"],
        default="cinematic",
        help="Color grading preset (default: cinematic)",
    )
    parser.add_argument(
        "--no-webm",
        action="store_true",
        help="Skip WebM output generation",
    )
    parser.add_argument(
        "--input-fps",
        type=float,
        default=1.0,
        help="Base framerate for source frames",
    )
    parser.add_argument(
        "--target-fps",
        type=int,
        default=24,
        help="Target framerate for interpolation",
    )
    args = parser.parse_args()

    ensure_ffmpeg()

    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text())
    series_list = data.get("series", [])
    if not series_list:
        raise SystemExit("No series found in manifest. Run build-solstudie-assets.py first.")

    frames_dir = Path(args.frames_dir)
    output_dir = Path(args.output_dir)

    for series in series_list:
        series_id = series.get("id")
        if not series_id:
            continue
        print(f"Building video for {series_id}")
        output_path = build_video_mp4(
            series_id,
            frames_dir,
            output_dir,
            args.input_fps,
            args.target_fps,
            args.grade,
        )
        video_entry = {
            "mp4": f"assets/solstudie/video/{output_path.name}",
            "fps": args.target_fps,
            "interpolated": True,
            "input_fps": args.input_fps,
            "grade": args.grade,
        }
        if not args.no_webm:
            webm_path = build_video_webm(
                series_id,
                frames_dir,
                output_dir,
                args.input_fps,
                args.target_fps,
                args.grade,
            )
            video_entry["webm"] = f"assets/solstudie/video/{webm_path.name}"
        series["video"] = video_entry

    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"Updated manifest: {manifest_path}")


if __name__ == "__main__":
    main()
