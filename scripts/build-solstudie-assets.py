#!/usr/bin/env python3
"""Build solstudie animation assets from PDF frames.

Converts PDFs to PNG frames and generates dashboard/data/solstudie.json.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

MONTHS = {
    "januar": (1, "januar"),
    "jan": (1, "januar"),
    "februar": (2, "februar"),
    "feb": (2, "februar"),
    "mars": (3, "mars"),
    "april": (4, "april"),
    "mai": (5, "mai"),
    "juni": (6, "juni"),
    "juli": (7, "juli"),
    "august": (8, "august"),
    "september": (9, "september"),
    "sep": (9, "september"),
    "oktober": (10, "oktober"),
    "okt": (10, "oktober"),
    "november": (11, "november"),
    "nov": (11, "november"),
    "desember": (12, "desember"),
    "des": (12, "desember"),
}

FILENAME_RE = re.compile(
    r"Sol\s*-\s*(\d{1,2})\.?\s*([A-Za-zÆØÅæøå]+)\s*-\s*Kl\.?\s*(\d{2})[_:.](\d{2})",
    re.IGNORECASE,
)


def parse_filename(stem: str) -> dict | None:
    match = FILENAME_RE.search(stem)
    if not match:
        return None

    day = int(match.group(1))
    month_raw = match.group(2).strip().lower().strip(".")
    hour = int(match.group(3))
    minute = int(match.group(4))

    month_num, month_label = MONTHS.get(month_raw, (13, month_raw))
    series_id = f"{day:02d}{month_raw}"
    date_label = f"{day}. {month_label}"
    time_label = f"{hour:02d}:{minute:02d}"

    return {
        "day": day,
        "month_num": month_num,
        "month_label": month_label,
        "series_id": series_id,
        "date_label": date_label,
        "hour": hour,
        "minute": minute,
        "time_label": time_label,
    }


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def convert_pdf(pdf_path: Path, output_path: Path, width: int | None, density: int) -> None:
    magick = shutil.which("magick")
    if magick:
        cmd = [
            magick,
            "-density",
            str(density),
            "-background",
            "white",
            "-alpha",
            "remove",
            str(pdf_path),
        ]
        if width:
            cmd += ["-resize", f"{width}x"]
        cmd.append(str(output_path))
        run_cmd(cmd)
        return

    sips = shutil.which("sips")
    if sips:
        run_cmd([sips, "-s", "format", "png", str(pdf_path), "--out", str(output_path)])
        if width:
            run_cmd([sips, "-Z", str(width), str(output_path)])
        return

    qlmanage = shutil.which("qlmanage")
    if qlmanage:
        tmp_dir = output_path.parent / ".tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        size = str(width or 2400)
        run_cmd([qlmanage, "-t", "-s", size, "-o", str(tmp_dir), str(pdf_path)])
        rendered = tmp_dir / f"{pdf_path.stem}.png"
        if rendered.exists():
            rendered.replace(output_path)
        return

    raise RuntimeError("No PDF converter found. Install ImageMagick or use macOS sips.")


def build_manifest(frames: list[dict], manifest_path: Path) -> dict:
    series_map: dict[str, dict] = {}
    for frame in frames:
        series_id = frame["series_id"]
        if series_id not in series_map:
            series_map[series_id] = {
                "id": series_id,
                "label": frame["date_label"],
                "month_num": frame["month_num"],
                "day": frame["day"],
                "frames": [],
            }
        series_map[series_id]["frames"].append(
            {
                "src": frame["src"],
                "time": frame["time_label"],
                "label": f"{frame['date_label']} kl. {frame['time_label']}",
                "source": frame["source"],
            }
        )

    series_list = sorted(
        series_map.values(),
        key=lambda item: (item["month_num"], item["day"]),
    )
    for series in series_list:
        series["frames"].sort(
            key=lambda item: (int(item["time"].split(":")[0]), int(item["time"].split(":")[1]))
        )
        series.pop("month_num", None)
        series.pop("day", None)

    manifest = {
        "title": "Solstudie Hovfaret 13",
        "updated": date.today().isoformat(),
        "series": series_list,
        "defaults": {
            "fps": 1,
            "loop": True,
        },
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build solstudie frames + manifest.")
    parser.add_argument(
        "--source",
        default="~/Downloads/hovfaret solstudiet",
        help="Directory containing PDF frames",
    )
    parser.add_argument(
        "--output",
        default="dashboard/assets/solstudie/frames",
        help="Output directory for PNG frames",
    )
    parser.add_argument(
        "--manifest",
        default="dashboard/data/solstudie.json",
        help="Manifest output path",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=2400,
        help="Output width in pixels (long edge)",
    )
    parser.add_argument(
        "--density",
        type=int,
        default=220,
        help="ImageMagick density when available",
    )
    parser.add_argument(
        "--copy-pdfs",
        action="store_true",
        help="Copy source PDFs into dashboard/assets/solstudie/pdfs",
    )
    args = parser.parse_args()

    source_dir = Path(args.source).expanduser()
    if not source_dir.exists():
        raise SystemExit(f"Source directory not found: {source_dir}")

    pdfs = sorted(source_dir.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDFs found in {source_dir}")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_copy_dir = output_dir.parent / "pdfs"
    if args.copy_pdfs:
        pdf_copy_dir.mkdir(parents=True, exist_ok=True)

    frames: list[dict] = []

    for pdf_path in pdfs:
        meta = parse_filename(pdf_path.stem)
        if not meta:
            print(f"Skipping (unrecognized name): {pdf_path.name}")
            continue

        frame_name = f"{meta['series_id']}-{meta['hour']:02d}{meta['minute']:02d}.png"
        output_path = output_dir / frame_name

        if not output_path.exists():
            print(f"Converting {pdf_path.name} -> {output_path.name}")
            convert_pdf(pdf_path, output_path, args.width, args.density)
        else:
            print(f"Frame exists, skipping: {output_path.name}")

        if args.copy_pdfs:
            shutil.copy2(pdf_path, pdf_copy_dir / pdf_path.name)

        frames.append(
            {
                **meta,
                "src": f"assets/solstudie/frames/{frame_name}",
                "source": pdf_path.name,
            }
        )

    manifest_path = Path(args.manifest)
    build_manifest(frames, manifest_path)
    print(f"Manifest written: {manifest_path}")


if __name__ == "__main__":
    main()
