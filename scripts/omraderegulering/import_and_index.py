#!/usr/bin/env python3
"""
Import and index a local document bundle into this repo for traceability.

Default use case:
  - Source folder: ~/Downloads/områderegulering
  - Output folder: documents/omraderegulering-skoyen-vedtakspunkt6

What it does:
  1) Copies PDFs/MDs into repo (raw/)
  2) Extracts searchable text (extract/text/)
  3) Produces an index (index.json + index.csv)
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from PyPDF2 import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent.parent


NORWEGIAN_MONTHS = {
    "januar": 1,
    "februar": 2,
    "mars": 3,
    "april": 4,
    "mai": 5,
    "juni": 6,
    "juli": 7,
    "august": 8,
    "september": 9,
    "oktober": 10,
    "november": 11,
    "desember": 12,
}


GENERIC_TITLES = {
    "powerpoint-presentasjon",
    "vår ref:",
}


TOPIC_RULES: list[tuple[str, list[str]]] = [
    ("vedtakspunkt6", [r"vedtakspunkt\s*6", r"\bpunkt\s*6\b"]),
    ("utnyttelse-og-formal", [r"utnyttelse\s+og\s+formål", r"utnyttelse\s+og\s+formål"]),
    ("omraderegulering-skoyen", [r"områderegulering\s+for\s+skøyen", r"områderegulering\s+skøyen"]),
    ("kdd-innsigelse", [r"innsig", r"kommunal- og distriktsdepartementet", r"\bKDD\b", r"departementet"]),
    ("planinitiativ-stopp", [r"stopp(et)?\s+planinitiativ", r"avslag", r"avvise\s+alternative\s+plan", r"avvis(e|ning)"]),
    ("alternative-planforslag", [r"alternative?\s+plan", r"avvikende\s+plan"]),
    ("pbe", [r"\bPBE\b", r"plan- og bygningsetaten"]),
    ("byradet", [r"byrådet", r"byrådsavdeling", r"byråd"]),
    ("byutviklingsutvalget", [r"byutviklingsutvalget"]),
    ("bystyret", [r"bystyret"]),
    ("fornebubanen", [r"fornebubanen"]),
    ("trikk", [r"trikk", r"trikketras", r"trikkeløsning", r"vendesløyfe", r"vende"]),
    ("ombruk", [r"ombruk", r"sirkul", r"gjenbruk", r"bærekraftig\s+forvaltning"]),
    ("hoff-village", [r"hoff\s+village"]),
    ("hovfaret-13", [r"hovfaret\s+13", r"\bH13\b"]),
    ("engebrets-vei-3", [r"engebrets\s+vei\s+3"]),
    ("hoffsveien-13", [r"hoffsveien\s+13"]),
    ("oma-skoyen-omradeforum", [r"\bOMA\b", r"skøyen\s+grunneierforum", r"skøyen\s+områdeforum"]),
]


@dataclasses.dataclass(frozen=True)
class Quote:
    text: str
    page: int | None = None


def _slugify(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    if not text:
        return "untitled"
    # Replace Norwegian chars and other diacritics in a conservative way (best-effort).
    replacements = {
        "æ": "ae",
        "ø": "o",
        "å": "a",
        "é": "e",
        "è": "e",
        "ê": "e",
        "á": "a",
        "à": "a",
        "ä": "a",
        "ö": "o",
        "ü": "u",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return (text[:max_len] or "untitled").rstrip("-")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run_pdftotext(src_pdf: Path, out_txt: Path) -> None:
    if not _cmd_exists("pdftotext"):
        raise RuntimeError("pdftotext not found in PATH")
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    # Keep default page breaks; -layout improves legibility for some PDFs.
    subprocess.run(
        ["pdftotext", "-layout", str(src_pdf), str(out_txt)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _extract_pdf_metadata(pdf_path: Path) -> dict[str, Any]:
    try:
        reader = PdfReader(str(pdf_path))
        meta = reader.metadata or {}
        title = (meta.get("/Title") or "").strip()
        author = (meta.get("/Author") or "").strip()
        creation_raw = (meta.get("/CreationDate") or "").strip() or None
        mod_raw = (meta.get("/ModDate") or "").strip() or None
        return {
            "pages": len(reader.pages),
            "pdf_title": title or None,
            "pdf_author": author or None,
            "pdf_creation_date": _parse_pdf_metadata_date(creation_raw),
            "pdf_mod_date": _parse_pdf_metadata_date(mod_raw),
        }
    except Exception:
        return {
            "pages": None,
            "pdf_title": None,
            "pdf_author": None,
            "pdf_creation_date": None,
            "pdf_mod_date": None,
        }


def _find_first_nonempty_line(text: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Skip some boilerplate that isn't a title.
        if line.lower() in {"oslo kommune", "bystyret"}:
            continue
        return line
    return None


def _infer_title(meta_title: str | None, text: str) -> str:
    if meta_title:
        mt = meta_title.strip()
        if mt and mt.strip().lower() not in GENERIC_TITLES:
            return mt
    first = _find_first_nonempty_line(text)
    return first or (meta_title or "Ukjent tittel")


def _infer_doc_type(path: Path, meta_title: str | None, text: str) -> str:
    name = path.name.lower()
    mt = (meta_title or "").lower()
    t = text.lower()

    if path.suffix.lower() == ".md":
        return "e-post"

    if "politisk behandling av" in t or "sak utvalg møtedato" in t:
        return "politisk_sak"

    if "byrådssak" in t or "sak til bystyret" in t:
        return "byrådssak"

    if "fra:" in t and "sendt:" in t and "til:" in t:
        return "e-post"

    if "vår ref" in t and ("telefon" in t or "e-post:" in t):
        return "brev"

    if mt == "powerpoint-presentasjon" or "powerpoint" in mt or "presentasjon" in t:
        return "presentasjon"

    if "brev" in name:
        return "brev"

    return "notat"


def _parse_numeric_date(day: str, month: str, year: str) -> str | None:
    try:
        d = int(day)
        m = int(month)
        y = int(year)
        if y < 100:
            y = 2000 + y
        dt = datetime(y, m, d)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def _parse_textual_date(day: str, month_name: str, year: str) -> str | None:
    mn = month_name.strip().lower().strip(".")
    m = NORWEGIAN_MONTHS.get(mn)
    if not m:
        return None
    return _parse_numeric_date(day, str(m), year)


def _extract_date(text: str) -> str | None:
    """
    Best-effort single "document date".
    Preference order:
      1) Møtedato
      2) Vår dato / Dato / Sendt
      3) First parseable date in the text
    """
    patterns: list[tuple[str, str]] = [
        ("møtedato", r"møtedato\s+(\d{1,2})[./](\d{1,2})[./](\d{2,4})"),
        ("vår dato", r"vår\s+dato:\s*(\d{1,2})[./](\d{1,2})[./](\d{2,4})"),
        ("dato", r"dato:\s*(\d{1,2})[./](\d{1,2})[./](\d{2,4})"),
        ("sendt", r"sendt:\s*(?:\w+\s+)?(\d{1,2})\\?\.\s*(\w+)\s*(\d{4})"),
        ("sendt", r"sendt:\s*(?:\w+\s+)?(\d{1,2})[./](\d{1,2})[./](\d{2,4})"),
        ("vår dato", r"vår\s+dato:\s*(\d{1,2})\\?\.\s*(\w+)\s*(\d{4})"),
        ("dato", r"dato:\s*(\d{1,2})\\?\.\s*(\w+)\s*(\d{4})"),
    ]

    # Normalize some common Markdown/escaped punctuation to improve date extraction.
    normalized = text.replace("*", "").replace("\\.", ".")
    lower = normalized.lower()
    for _, pat in patterns:
        m = re.search(pat, lower, re.IGNORECASE)
        if not m:
            continue
        g = m.groups()
        if len(g) != 3:
            continue
        d, mo, y = g
        if mo.isdigit():
            iso = _parse_numeric_date(d, mo, y)
        else:
            iso = _parse_textual_date(d, mo, y)
        if iso:
            return iso

    # Fallback: first numeric date in text
    m = re.search(r"(\d{1,2})[./](\d{1,2})[./](\d{2,4})", lower)
    if m:
        iso = _parse_numeric_date(m.group(1), m.group(2), m.group(3))
        if iso:
            return iso

    # Fallback: first textual date in text
    m = re.search(r"(\d{1,2})\\?\.\s*([a-zæøå]+)\s*(\d{4})", lower)
    if m:
        iso = _parse_textual_date(m.group(1), m.group(2), m.group(3))
        if iso:
            return iso

    return None


def _extract_email_subject(text: str) -> str | None:
    m = re.search(r"emne:\s*(.+)", text, re.IGNORECASE)
    if not m:
        return None
    subject = m.group(1).strip()
    # Light cleanup for Markdown-ish subjects (e.g. "**Subject**", escaped dots).
    subject = subject.replace("\\.", ".")
    subject = subject.replace("*", "")
    subject = re.sub(r"\s+", " ", subject)
    return subject[:180] or None


def _collect_topics(text: str) -> list[str]:
    t = text.lower()
    topics: list[str] = []
    for topic, patterns in TOPIC_RULES:
        for pat in patterns:
            if re.search(pat, t, re.IGNORECASE):
                topics.append(topic)
                break
    # Stable order and unique
    seen = set()
    out = []
    for tp in topics:
        if tp in seen:
            continue
        seen.add(tp)
        out.append(tp)
    return out


def _summarize(doc_type: str, title: str, doc_date: str | None, topics: list[str]) -> str:
    date_part = f"{doc_date}: " if doc_date else ""
    if doc_type == "byrådssak":
        return f"{date_part}Byrådssak om oppheving av vedtakspunkt 6 i områderegulering for Skøyen."
    if doc_type == "politisk_sak":
        return f"{date_part}Politisk behandling/oversendelse til utvalg og bystyre (oppheving av vedtakspunkt 6)."
    if doc_type == "presentasjon":
        return f"{date_part}Presentasjon om områderegulering Skøyen og praktiske konsekvenser (inkl. alternative planer/vedtakspunkt 6)."
    if doc_type == "brev":
        return f"{date_part}Brev/innspill knyttet til stoppet planinitiativ og/eller tolkning av vedtakspunkt 6."
    if doc_type == "e-post":
        return f"{date_part}E-post/videresending knyttet til områderegulering Skøyen og vedtakspunkt 6."
    if "hovfaret-13" in topics:
        return f"{date_part}Notat/utdrag med Hovfaret 13 som eksempel på vedtakspunkt 6-problematikken."
    return f"{date_part}{title}"


def _extract_quotes(pdf_path: Path, doc_type: str) -> list[Quote]:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception:
        return []

    patterns = [
        r"vedtakspunkt\s*6",
        r"oppheves",
        r"stoppe\s+«?alle»?\s+plan",
        r"normalsituasjon",
        r"avvise\s+alternative\s+plan",
        r"planinitiativ",
    ]

    quotes: list[Quote] = []
    for page_idx, page in enumerate(reader.pages):
        try:
            page_text = (page.extract_text() or "").strip()
        except Exception:
            continue
        if not page_text:
            continue
        page_lower = page_text.lower()
        for pat in patterns:
            if not re.search(pat, page_lower, re.IGNORECASE):
                continue
            m = re.search(pat, page_lower, re.IGNORECASE)
            if not m:
                continue
            i = max(0, m.start() - 140)
            j = min(len(page_text), m.end() + 240)
            snippet = re.sub(r"\s+", " ", page_text[i:j]).strip()
            if len(snippet) > 240:
                snippet = snippet[:237].rstrip() + "…"
            quotes.append(Quote(text=snippet, page=page_idx + 1))
            break
        if len(quotes) >= 3:
            break

    # Special case: capture the actual vedtakspunkt 6 wording if present (often in Hovfaret/notes).
    if doc_type in {"notat", "presentasjon"} and len(quotes) < 3:
        for page_idx, page in enumerate(reader.pages):
            try:
                page_text = (page.extract_text() or "").strip()
            except Exception:
                continue
            if "Det skal tillates fremmet detaljreguleringer" in page_text:
                start = page_text.find("Det skal tillates fremmet detaljreguleringer")
                snippet = re.sub(r"\s+", " ", page_text[start : start + 420]).strip()
                if len(snippet) > 240:
                    snippet = snippet[:237].rstrip() + "…"
                quotes.insert(0, Quote(text=snippet, page=page_idx + 1))
                break

    # De-dupe by text
    seen = set()
    out: list[Quote] = []
    for q in quotes:
        if q.text in seen:
            continue
        seen.add(q.text)
        out.append(q)
    return out[:3]


def _parse_pdf_metadata_date(value: str | None) -> str | None:
    if not value:
        return None
    # Typical PDF date format: D:YYYYMMDDhhmmssZ (we only need YYYYMMDD)
    m = re.search(r"(\d{4})(\d{2})(\d{2})", value)
    if not m:
        return None
    try:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mo, d).strftime("%Y-%m-%d")
    except Exception:
        return None


def _load_existing_index(index_path: Path) -> dict[str, Any] | None:
    if not index_path.exists():
        return None
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _build_id_allocator(existing: dict[str, Any] | None) -> tuple[dict[str, str], int]:
    sha_to_id: dict[str, str] = {}
    next_num = 1
    if existing:
        docs = existing.get("documents", [])
        for doc in docs:
            sha = doc.get("sha256")
            did = doc.get("id")
            if isinstance(sha, str) and isinstance(did, str):
                sha_to_id[sha] = did
            if isinstance(did, str) and did.startswith("DOC-"):
                try:
                    n = int(did.split("-", 1)[1])
                    next_num = max(next_num, n + 1)
                except Exception:
                    pass
    return sha_to_id, next_num


def _allocate_id(sha: str, sha_to_id: dict[str, str], next_num: int) -> tuple[str, int]:
    if sha in sha_to_id:
        return sha_to_id[sha], next_num
    doc_id = f"DOC-{next_num:03d}"
    sha_to_id[sha] = doc_id
    return doc_id, next_num + 1


def _relative_to_repo(path: Path) -> str:
    try:
        return str(path.relative_to(BASE_DIR))
    except Exception:
        return str(path)


def _default_src_dir() -> Path:
    # Preferred path (as used in this project)
    direct = Path.home() / "Downloads" / "områderegulering"
    if direct.exists():
        return direct
    # Fallback: find a directory in ~/Downloads whose normalized name contains "omraderegulering"
    downloads = Path.home() / "Downloads"
    if not downloads.exists():
        return direct
    for p in downloads.iterdir():
        if not p.is_dir():
            continue
        if "omr" in p.name.lower() and "reguler" in p.name.lower():
            return p
    return direct


def _write_csv(rows: list[dict[str, Any]], out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "doc_type",
        "date",
        "title",
        "1line_summary",
        "key_topics",
        "imported_path",
        "original_path",
        "sha256",
        "pages",
    ]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "id": r.get("id"),
                    "doc_type": r.get("doc_type"),
                    "date": r.get("date"),
                    "title": r.get("title"),
                    "1line_summary": r.get("1line_summary"),
                    "key_topics": ";".join(r.get("key_topics") or []),
                    "imported_path": r.get("imported_path"),
                    "original_path": r.get("original_path"),
                    "sha256": r.get("sha256"),
                    "pages": r.get("pages"),
                }
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import and index a document bundle for traceability.")
    parser.add_argument(
        "--src",
        type=Path,
        default=_default_src_dir(),
        help="Source directory with PDFs/MDs (default: ~/Downloads/områderegulering)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=BASE_DIR / "documents" / "omraderegulering-skoyen-vedtakspunkt6",
        help="Output directory in repo",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing raw/extract outputs")
    args = parser.parse_args(argv)

    src_dir: Path = args.src
    out_dir: Path = args.out

    if not src_dir.exists():
        raise SystemExit(f"Source directory not found: {src_dir}")

    raw_dir = out_dir / "raw"
    extract_dir = out_dir / "extract" / "text"
    raw_dir.mkdir(parents=True, exist_ok=True)
    extract_dir.mkdir(parents=True, exist_ok=True)

    index_json = out_dir / "index.json"
    existing = _load_existing_index(index_json)
    sha_to_id, next_num = _build_id_allocator(existing)

    src_files = [
        p
        for p in sorted(src_dir.iterdir(), key=lambda p: p.name.lower())
        if p.is_file() and p.suffix.lower() in {".pdf", ".md"}
    ]
    if not src_files:
        raise SystemExit(f"No PDF/MD files found in: {src_dir}")

    rows: list[dict[str, Any]] = []

    for src_path in src_files:
        sha = _sha256(src_path)
        doc_id, next_num = _allocate_id(sha, sha_to_id, next_num)

        ext = src_path.suffix.lower()
        extracted_text_path = extract_dir / f"{doc_id}.txt"

        meta_title = None
        pdf_meta: dict[str, Any] = {
            "pages": None,
            "pdf_title": None,
            "pdf_author": None,
            "pdf_creation_date": None,
            "pdf_mod_date": None,
        }
        text_for_inference = ""

        if ext == ".pdf":
            pdf_meta = _extract_pdf_metadata(src_path)
            meta_title = pdf_meta.get("pdf_title")

            if args.overwrite or not extracted_text_path.exists():
                _run_pdftotext(src_path, extracted_text_path)
            text_for_inference = _read_text_file(extracted_text_path)
        else:
            text_for_inference = _read_text_file(src_path)
            if args.overwrite or not extracted_text_path.exists():
                extracted_text_path.write_text(text_for_inference, encoding="utf-8")

        title = _infer_title(meta_title, text_for_inference)
        doc_type = _infer_doc_type(src_path, meta_title, text_for_inference)

        doc_date = _extract_date(text_for_inference)
        if not doc_date and meta_title:
            doc_date = _extract_date(meta_title)
        if not doc_date:
            doc_date = _extract_date(src_path.name)

        pdf_created = pdf_meta.get("pdf_creation_date")
        if pdf_created and doc_type == "byrådssak":
            # If the text-date looks like it's a referenced attachment date, prefer PDF creation date.
            if not doc_date or (isinstance(doc_date, str) and doc_date < pdf_created):
                doc_date = pdf_created
        elif pdf_created and not doc_date:
            doc_date = pdf_created

        topics = _collect_topics(text_for_inference)

        if doc_type == "e-post":
            subj = _extract_email_subject(text_for_inference)
            if subj and subj.lower() not in title.lower():
                title = subj

        one_line = _summarize(doc_type, title, doc_date, topics)

        # Destination filename
        date_part = doc_date or "undated"
        title_slug = _slugify(title, max_len=70)
        dst_name = f"{doc_id}__{date_part}__{doc_type}__{title_slug}{ext}"
        dst_path = raw_dir / dst_name

        if args.overwrite:
            for old in raw_dir.glob(f"{doc_id}__*{ext}"):
                old.unlink(missing_ok=True)
        if not dst_path.exists():
            shutil.copy2(src_path, dst_path)

        quotes: list[Quote] = []
        if ext == ".pdf":
            quotes = _extract_quotes(src_path, doc_type)

        rows.append(
            {
                "id": doc_id,
                "original_path": str(src_path),
                "imported_path": _relative_to_repo(dst_path),
                "extract_text_path": _relative_to_repo(extracted_text_path),
                "sha256": sha,
                "bytes": src_path.stat().st_size,
                "doc_type": doc_type,
                "date": doc_date,
                "title": title,
                "1line_summary": one_line,
                "key_topics": topics,
                "pages": pdf_meta.get("pages"),
                "pdf_title": pdf_meta.get("pdf_title"),
                "pdf_author": pdf_meta.get("pdf_author"),
                "pdf_creation_date": pdf_meta.get("pdf_creation_date"),
                "pdf_mod_date": pdf_meta.get("pdf_mod_date"),
                "quotes": [dataclasses.asdict(q) for q in quotes],
            }
        )

    index = {
        "bundle": {
            "name": "områderegulering",
            "source_dir": str(src_dir),
            "imported_to": _relative_to_repo(out_dir),
            "file_count": len(src_files),
        },
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "documents": sorted(rows, key=lambda r: r["id"]),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    index_json.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_csv(index["documents"], out_dir / "index.csv")

    print(f"Imported {len(rows)} documents → {out_dir}")
    print(f"Index: {_relative_to_repo(index_json)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
