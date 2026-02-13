#!/usr/bin/env python3
"""
Import batch: hovfaret13mailgreier. 13.02

Pipeline:
1) Build file inventory + mapping report.
2) Upsert all batch files into data/documents.json.
3) Derive/merge meetings from ICS (+ invitation EML context) into data/meetings.json.
4) Enrich data/themes/nabomerknader.json with source traceability for this batch.
5) Append relevant evidence refs into data/themes/nabomerknad-svar.json.
6) Keep data/config.json metrics in sync (meetings/documents + last_updated).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Any
from zipfile import ZipFile

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    PdfReader = None


BATCH_ID = "mailgreier_2026-02-13"
BATCH_FOLDER_NAME = "hovfaret13mailgreier. 13.02"
SOURCE_FOLDER_LABEL = BATCH_FOLDER_NAME
TODAY = "2026-02-13"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode_header_value(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def parse_email_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        return dt.date().isoformat()
    except Exception:
        return None


def normalize_text(value: str) -> str:
    value = value.strip().lower()
    # Normalize Scandinavian letters before ASCII cleanup.
    value = (
        value.replace("æ", "ae")
        .replace("ø", "o")
        .replace("å", "a")
    )
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.replace("&", " og ")
    value = re.sub(r"[_\-–—]+", " ", value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slugify(value: str) -> str:
    n = normalize_text(value)
    return re.sub(r"\s+", "_", n)[:72] or "untitled"


def split_address_list(value: str | None) -> list[dict[str, str]]:
    if not value:
        return []
    result = []
    for name, addr in getaddresses([value]):
        clean_name = decode_header_value(name).strip()
        clean_addr = addr.strip()
        if not clean_name and not clean_addr:
            continue
        result.append({"name": clean_name, "email": clean_addr})
    return result


def maybe_domain_org(email_addr: str | None) -> str | None:
    if not email_addr or "@" not in email_addr:
        return None
    domain = email_addr.split("@", 1)[1].lower()
    mapping = {
        "naturalstate.no": "Natural State AS",
        "urbania.no": "Urbania Eiendom AS",
        "r21.no": "R21 Arkitekter",
        "bsrg.no": "Byggesaksrådgivning AS",
        "uio.no": "UiO",
    }
    return mapping.get(domain)


def classify_document(name: str, ext: str, subject: str = "", body: str = "") -> tuple[str, str]:
    hay = " ".join([name, subject, body]).lower()

    def has(*terms: str) -> bool:
        return any(t in hay for t in terms)

    if ext == "ics":
        return "meetings", "calendar_invitation"

    if ext == "eml":
        if has("invitation", "informasjonsmøtet", "dialogmøte", "ekstra møte", " @ "):
            return "meetings", "meeting_invitation_email"
        if has("nabomerknad", "nabovarsel", "merknad", "uttalelser"):
            return "stakeholder_engagement", "neighbor_remarks_email"
        if has("dispensasjon", "rammesøknad", "byggesaksrådgivning", "følgebrev"):
            return "regulatory", "regulatory_correspondence"
        return "communications", "email_correspondence"

    if ext in {"pdf", "docx", "doc"}:
        if has("nabomerknad", "nabovarsel", "merknad", "uttalels"):
            return "stakeholder_engagement", "neighbor_remarks_document"
        if has(
            "dispensasjon",
            "byggesaksrådgivning",
            "følgebrev",
            "beskrivelse",
            "fremdrift",
            "høydeberegning",
            "rekkverk",
            "saksnr",
            "rammesøknad",
        ):
            return "regulatory", "regulatory_document"
        return "communications", "supporting_document"

    return "other", "unknown"


def extract_docx_preview(path: Path) -> dict[str, Any]:
    preview: dict[str, Any] = {"title": None, "headings": [], "excerpt": None}
    try:
        with ZipFile(path) as zf:
            xml = zf.read("word/document.xml")
    except Exception:
        return preview

    try:
        root = ET.fromstring(xml)
    except Exception:
        return preview

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: list[str] = []
    headings: list[str] = []
    for p in root.findall(".//w:p", ns):
        texts = [t.text or "" for t in p.findall(".//w:t", ns)]
        line = "".join(texts).strip()
        if not line:
            continue
        paragraphs.append(line)
        style_el = p.find(".//w:pStyle", ns)
        style_val = style_el.attrib.get(f"{{{ns['w']}}}val", "") if style_el is not None else ""
        if style_val.lower().startswith("heading"):
            headings.append(line)

    if paragraphs:
        preview["title"] = paragraphs[0][:240]
        preview["excerpt"] = " ".join(paragraphs[:6])[:1200]
    preview["headings"] = headings[:20]
    return preview


def extract_pdf_preview(path: Path) -> dict[str, Any]:
    preview: dict[str, Any] = {"title": None, "page_count": None, "excerpt": None}
    if PdfReader is None:
        return preview
    try:
        reader = PdfReader(str(path))
        preview["page_count"] = len(reader.pages)
        if reader.metadata and getattr(reader.metadata, "title", None):
            title = str(reader.metadata.title or "").strip()
            if title:
                preview["title"] = title[:240]
        text_parts = []
        for page in reader.pages[:2]:
            try:
                text_parts.append((page.extract_text() or "").strip())
            except Exception:
                continue
        excerpt = " ".join(part for part in text_parts if part).strip()
        if excerpt:
            preview["excerpt"] = re.sub(r"\s+", " ", excerpt)[:1200]
    except Exception:
        return preview
    return preview


def parse_ics_content(raw: str) -> dict[str, Any]:
    lines = []
    for line in raw.replace("\r\n", "\n").split("\n"):
        if not line:
            continue
        if line.startswith((" ", "\t")) and lines:
            lines[-1] += line[1:]
        else:
            lines.append(line)

    # Only parse the first VEVENT block to avoid timezone DTSTART fallthrough.
    event_lines: list[str] = []
    in_event = False
    for line in lines:
        if line == "BEGIN:VEVENT":
            in_event = True
            continue
        if line == "END:VEVENT":
            in_event = False
            break
        if in_event:
            event_lines.append(line)

    if not event_lines:
        event_lines = lines

    def get(prefix: str) -> str | None:
        for line in event_lines:
            if line.startswith(prefix):
                return line.split(":", 1)[1] if ":" in line else None
        return None

    def get_key(prefix: str) -> str | None:
        for line in event_lines:
            if line.startswith(prefix):
                return line
        return None

    summary = get("SUMMARY") or ""
    location = get("LOCATION") or ""
    uid = get("UID") or ""
    desc = get("DESCRIPTION") or ""

    dtstart_line = get_key("DTSTART")
    dtend_line = get_key("DTEND")
    start_date = None
    start_time = None
    end_time = None

    def parse_dt(line: str | None) -> tuple[str | None, str | None]:
        if not line or ":" not in line:
            return None, None
        raw_val = line.split(":", 1)[1].replace("Z", "")
        m = re.match(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})", raw_val)
        if m:
            y, mo, d, hh, mm = m.groups()
            return f"{y}-{mo}-{d}", f"{hh}:{mm}"
        m2 = re.match(r"(\d{4})(\d{2})(\d{2})", raw_val)
        if m2:
            y, mo, d = m2.groups()
            return f"{y}-{mo}-{d}", None
        return None, None

    start_date, start_time = parse_dt(dtstart_line)
    _, end_time = parse_dt(dtend_line)

    attendees = []
    for line in event_lines:
        if line.startswith("ATTENDEE"):
            addr = line.split(":", 1)[1] if ":" in line else ""
            email_addr = addr.replace("mailto:", "").strip()
            cn_match = re.search(r"CN=([^;:]+)", line)
            name = cn_match.group(1).strip() if cn_match else ""
            attendees.append({"name": name, "email": email_addr})

    organizer_line = get_key("ORGANIZER")
    organizer = {"name": "", "email": ""}
    if organizer_line:
        cn_match = re.search(r"CN=([^;:]+)", organizer_line)
        organizer["name"] = cn_match.group(1).strip() if cn_match else ""
        if ":" in organizer_line:
            organizer["email"] = organizer_line.split(":", 1)[1].replace("mailto:", "").strip()

    description = desc.replace("\\n", "\n").replace("\\,", ",").strip()
    description_lines = [ln.strip(" -•\t") for ln in description.split("\n") if ln.strip()]

    return {
        "uid": uid,
        "summary": summary.strip(),
        "location": location.strip(),
        "date": start_date,
        "start_time": start_time,
        "end_time": end_time,
        "organizer": organizer,
        "attendees": attendees,
        "description": description,
        "description_lines": description_lines,
    }


@dataclass
class ParsedFile:
    file_name: str
    path: Path
    ext: str
    size_bytes: int
    checksum_sha256: str
    category: str
    document_type: str
    derived_from: str
    parsed: dict[str, Any]


def parse_batch_file(path: Path) -> ParsedFile:
    file_name = path.name
    ext = path.suffix.lower().lstrip(".")
    checksum = sha256_file(path)
    parsed: dict[str, Any] = {}
    subject = ""
    body_preview = ""

    if ext == "eml":
        with path.open("rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
        subject = decode_header_value(msg.get("Subject"))
        from_raw = decode_header_value(msg.get("From"))
        to_raw = decode_header_value(msg.get("To"))
        cc_raw = decode_header_value(msg.get("Cc"))
        date_raw = decode_header_value(msg.get("Date"))
        message_id = decode_header_value(msg.get("Message-ID"))
        in_reply_to = decode_header_value(msg.get("In-Reply-To"))

        text_plain = ""
        text_html = ""
        has_calendar = False
        calendar_parts: list[dict[str, Any]] = []
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain" and not text_plain:
                try:
                    text_plain = part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True) or b""
                    text_plain = payload.decode(errors="replace")
            elif ctype == "text/html" and not text_html:
                try:
                    text_html = part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True) or b""
                    text_html = payload.decode(errors="replace")
            elif ctype in {"text/calendar", "application/ics"}:
                has_calendar = True
                raw = part.get_payload(decode=True) or b""
                try:
                    ics_text = raw.decode("utf-8", errors="replace")
                except Exception:
                    ics_text = ""
                if ics_text:
                    calendar_parts.append(parse_ics_content(ics_text))

        from_list = split_address_list(from_raw)
        to_list = split_address_list(to_raw)
        cc_list = split_address_list(cc_raw)
        date_norm = parse_email_date(date_raw)
        body_preview = re.sub(r"\s+", " ", (text_plain or text_html or "").strip())[:1200]

        parsed = {
            "subject": subject,
            "from": from_list,
            "to": to_list,
            "cc": cc_list,
            "date_raw": date_raw,
            "date": date_norm,
            "message_id": message_id,
            "in_reply_to": in_reply_to,
            "body_preview": body_preview,
            "has_calendar": has_calendar,
            "calendar_parts": calendar_parts,
        }

    elif ext == "ics":
        raw = path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_ics_content(raw)
        subject = parsed.get("summary") or ""
        body_preview = parsed.get("description", "")[:1200]

    elif ext in {"docx", "doc"}:
        parsed = extract_docx_preview(path)
        subject = parsed.get("title") or ""
        body_preview = parsed.get("excerpt") or ""

    elif ext == "pdf":
        parsed = extract_pdf_preview(path)
        subject = parsed.get("title") or ""
        body_preview = parsed.get("excerpt") or ""

    category, document_type = classify_document(file_name, ext, subject=subject, body=body_preview)
    return ParsedFile(
        file_name=file_name,
        path=path,
        ext=ext,
        size_bytes=path.stat().st_size,
        checksum_sha256=checksum,
        category=category,
        document_type=document_type,
        derived_from=ext or "unknown",
        parsed=parsed,
    )


def build_doc_record(parsed: ParsedFile) -> dict[str, Any]:
    doc_id = f"doc_mail_{parsed.checksum_sha256[:16]}"
    record: dict[str, Any] = {
        "id": doc_id,
        "file_name": parsed.file_name,
        "file_type": parsed.ext or "unknown",
        "document_type": parsed.document_type,
        "category": parsed.category,
        "source_folder": SOURCE_FOLDER_LABEL,
        "source_batch": BATCH_ID,
        "extraction_date": now_iso(),
        "has_error": False,
        "checksum_sha256": parsed.checksum_sha256,
        "derived_from": parsed.derived_from,
        "size_bytes": parsed.size_bytes,
    }
    if parsed.ext == "eml":
        record["email_subject"] = parsed.parsed.get("subject")
        record["email_date"] = parsed.parsed.get("date")
        record["email_from"] = parsed.parsed.get("from", [])
        record["email_to"] = parsed.parsed.get("to", [])
        if parsed.parsed.get("cc"):
            record["email_cc"] = parsed.parsed["cc"]
    elif parsed.ext == "ics":
        record["event_summary"] = parsed.parsed.get("summary")
        record["event_date"] = parsed.parsed.get("date")
        if parsed.parsed.get("uid"):
            record["event_uid"] = parsed.parsed.get("uid")
    elif parsed.ext in {"docx", "doc"}:
        if parsed.parsed.get("title"):
            record["title"] = parsed.parsed.get("title")
        if parsed.parsed.get("headings"):
            record["headings"] = parsed.parsed.get("headings")
    elif parsed.ext == "pdf":
        if parsed.parsed.get("title"):
            record["title"] = parsed.parsed.get("title")
        if parsed.parsed.get("page_count") is not None:
            record["page_count"] = parsed.parsed.get("page_count")
    return record


def duplicate_canonical_key(doc: dict[str, Any]) -> str:
    name = doc.get("file_name", "")
    base = re.sub(r"\.[^.]+$", "", name.strip(), flags=re.IGNORECASE)
    base = base.lower()
    prefixes = [
        "natural state as mail - ",
        "fwd_ ",
        "svar_ ",
        "videresend_ ",
        "updated invitation_ ",
        "invitation_ ",
    ]
    for p in prefixes:
        if base.startswith(p):
            base = base[len(p) :]
    return normalize_text(base)


def assign_duplicate_groups(batch_docs: list[dict[str, Any]]) -> None:
    groups: dict[str, list[dict[str, Any]]] = {}
    for doc in batch_docs:
        key = duplicate_canonical_key(doc)
        if key:
            groups.setdefault(key, []).append(doc)

    group_idx = 1
    priority = {"eml": 0, "docx": 1, "pdf": 2, "ics": 3}

    for _, docs in sorted(groups.items(), key=lambda x: x[0]):
        if len(docs) < 2:
            continue
        group_id = f"mg_dup_{group_idx:03d}"
        group_idx += 1
        docs_sorted = sorted(
            docs,
            key=lambda d: (
                priority.get(str(d.get("derived_from", "")), 9),
                len(str(d.get("file_name", ""))),
                str(d.get("file_name", "")),
            ),
        )
        primary = docs_sorted[0]
        primary_id = primary["id"]
        for doc in docs_sorted:
            doc["duplicate_group"] = group_id
            if doc["id"] != primary_id:
                doc["variant_of_doc_id"] = primary_id
            elif "variant_of_doc_id" in doc:
                del doc["variant_of_doc_id"]


def has_meeting_signal_eml(parsed: ParsedFile) -> bool:
    if parsed.ext != "eml":
        return False
    p = parsed.parsed
    subject = (p.get("subject") or "").lower()
    body = (p.get("body_preview") or "").lower()
    if p.get("has_calendar"):
        return True
    terms = [
        "invitation",
        "informasjonsmøtet",
        "dialogmøte",
        "ekstra møte",
        " @ ",
        "møte",
    ]
    return any(t in subject for t in terms) or any(t in body for t in terms[:4])


def candidate_from_ics_event(event: dict[str, Any], source_file: str) -> dict[str, Any] | None:
    date = event.get("date")
    summary = (event.get("summary") or "").strip()
    if not date or not summary:
        return None

    event_slug = slugify(summary)[:48]
    meeting_id = f"m_{date}_{event_slug}"
    start = event.get("start_time")
    end = event.get("end_time")
    time_range = f"{start}-{end}" if start and end else (start or None)
    attendees = event.get("attendees", [])

    participants = []
    seen = set()
    organizer = event.get("organizer", {})
    for person in [organizer] + attendees:
        name = (person.get("name") or "").strip()
        email_addr = (person.get("email") or "").strip()
        key = (name.lower(), email_addr.lower())
        if key in seen:
            continue
        seen.add(key)
        if not name and email_addr:
            name = email_addr.split("@", 1)[0]
        participants.append(
            {
                "name": name or "Ukjent",
                "organization": maybe_domain_org(email_addr),
                "email": email_addr or None,
            }
        )

    topics = []
    for line in event.get("description_lines", []):
        clean = re.sub(r"^\d+\.\s*", "", line).strip()
        if clean:
            topics.append(clean)
    topics = topics[:8]

    summary_text = (
        f"Avledet fra kalenderinvitasjon: {summary}. "
        f"Opprettet via {BATCH_ID} med {len(participants)} registrerte deltakere."
    )

    candidate: dict[str, Any] = {
        "id": meeting_id,
        "date": date,
        "title": summary,
        "organizer": organizer.get("email") or None,
        "location": event.get("location") or None,
        "participant_count": len(participants),
        "participants": participants,
        "topics_discussed": topics,
        "decisions": [],
        "action_items": [],
        "summary": summary_text,
        "outcomes": [summary_text],
        "type": "Møteinvitasjon",
        "source_file": source_file,
        "source_files": [source_file],
        "source_batch": BATCH_ID,
        "ingest_confidence": "high",
        "report": {
            "summary": summary_text,
            "discussion": [],
            "context": "Maskinavledet fra ICS-invitasjon. Krever manuell verifisering ved behov.",
            "metadata": {
                "source": "ics_import",
                "source_files": [source_file],
                "consolidated_date": TODAY,
            },
        },
    }
    if time_range:
        candidate["time"] = time_range
    if event.get("uid"):
        candidate["calendar_uid"] = event.get("uid")
    return candidate


def token_set(text: str) -> set[str]:
    return set(normalize_text(text).split())


def meeting_similarity(a: str, b: str) -> float:
    ta = token_set(a)
    tb = token_set(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return inter / max(len(ta), len(tb))


def merge_participants(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = []
    seen = set()
    for p in existing + incoming:
        name = (p.get("name") or "").strip()
        email_addr = (p.get("email") or "").strip().lower()
        key = (name.lower(), email_addr)
        if key in seen:
            continue
        seen.add(key)
        merged.append(
            {
                "name": name or "Ukjent",
                "organization": p.get("organization"),
                "email": p.get("email"),
            }
        )
    return merged


def find_matching_meeting(existing_meetings: list[dict[str, Any]], candidate: dict[str, Any]) -> dict[str, Any] | None:
    c_date = candidate.get("date")
    c_title = candidate.get("title", "")
    for meeting in existing_meetings:
        if meeting.get("id") == candidate.get("id"):
            return meeting
    for meeting in existing_meetings:
        if meeting.get("date") != c_date:
            continue
        sim = meeting_similarity(meeting.get("title", ""), c_title)
        if sim >= 0.45:
            return meeting
        m_title_norm = normalize_text(meeting.get("title", ""))
        c_title_norm = normalize_text(c_title)
        if (
            "hovfaret 13" in m_title_norm
            and "hovfaret 13" in c_title_norm
            and (
                ("dialogmote" in m_title_norm and "nabolag" in c_title_norm)
                or ("dialogmote" in c_title_norm and "nabolag" in m_title_norm)
            )
        ):
            return meeting
    return None


def merge_meeting(existing: dict[str, Any], candidate: dict[str, Any]) -> None:
    incoming_sources = candidate.get("source_files", []) or []
    existing_sources = existing.get("source_files", [])
    if isinstance(existing_sources, list):
        existing["source_files"] = sorted(set(existing_sources + incoming_sources))
    else:
        existing["source_files"] = sorted(set(incoming_sources))

    if not existing.get("source_file") and candidate.get("source_file"):
        existing["source_file"] = candidate["source_file"]
    if not existing.get("source_batch"):
        existing["source_batch"] = BATCH_ID
    if not existing.get("ingest_confidence"):
        existing["ingest_confidence"] = candidate.get("ingest_confidence", "medium")
    if not existing.get("time") and candidate.get("time"):
        existing["time"] = candidate["time"]
    if not existing.get("location") and candidate.get("location"):
        existing["location"] = candidate["location"]
    if not existing.get("organizer") and candidate.get("organizer"):
        existing["organizer"] = candidate["organizer"]

    existing_participants = existing.get("participants", []) or []
    incoming_participants = candidate.get("participants", []) or []
    merged_participants = merge_participants(existing_participants, incoming_participants)
    existing["participants"] = merged_participants
    existing["participant_count"] = len(merged_participants)

    if "report" in existing and isinstance(existing["report"], dict):
        md = existing["report"].setdefault("metadata", {})
        source_files = md.get("source_files", [])
        if not isinstance(source_files, list):
            source_files = []
        md["source_files"] = sorted(set(source_files + incoming_sources))
        if not md.get("consolidated_date"):
            md["consolidated_date"] = TODAY


def parse_batch(folder: Path) -> list[ParsedFile]:
    parsed_files = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file() or path.name.startswith("."):
            continue
        parsed_files.append(parse_batch_file(path))
    return parsed_files


def ensure_stat_bucket(stats: dict[str, Any], key: str) -> dict[str, int]:
    value = stats.get(key)
    if not isinstance(value, dict):
        value = {}
        stats[key] = value
    return value


def recalc_nabomerknad_stats(nm: dict[str, Any]) -> None:
    remarks = nm.get("remarks", [])
    stats = nm.setdefault("statistics", {})
    stats["total_submissions"] = len(remarks)
    stats["unique_submitters"] = len({r.get("submitter") for r in remarks if r.get("submitter")})

    by_type = {}
    by_channel = {}
    theme_frequency = {}
    dates = []
    for r in remarks:
        t = r.get("type")
        c = r.get("channel")
        if t:
            by_type[t] = by_type.get(t, 0) + 1
        if c:
            by_channel[c] = by_channel.get(c, 0) + 1
        for theme in r.get("themes", []):
            theme_frequency[theme] = theme_frequency.get(theme, 0) + 1
        if r.get("date"):
            dates.append(r["date"])

    stats["by_type"] = by_type
    stats["by_channel"] = by_channel
    stats["theme_frequency"] = dict(sorted(theme_frequency.items(), key=lambda kv: (-kv[1], kv[0])))
    if dates:
        stats["date_range"] = {"earliest": min(dates), "latest": max(dates)}


def build_inventory(parsed_files: list[ParsedFile]) -> dict[str, Any]:
    by_ext: dict[str, int] = {}
    by_category: dict[str, int] = {}
    files = []
    for p in parsed_files:
        by_ext[p.ext] = by_ext.get(p.ext, 0) + 1
        by_category[p.category] = by_category.get(p.category, 0) + 1
        files.append(
            {
                "file_name": p.file_name,
                "extension": p.ext,
                "size_bytes": p.size_bytes,
                "checksum_sha256": p.checksum_sha256,
                "category": p.category,
                "document_type": p.document_type,
                "derived_from": p.derived_from,
            }
        )
    return {
        # Keep inventory deterministic across reruns on the same batch/day.
        "generated_at": TODAY,
        "batch_id": BATCH_ID,
        "source_folder": SOURCE_FOLDER_LABEL,
        "summary": {
            "total_files": len(parsed_files),
            "by_extension": by_ext,
            "by_category": by_category,
        },
        "files": files,
    }


def build_mapping_report(
    parsed_files: list[ParsedFile],
    new_doc_records: list[dict[str, Any]],
    meetings_added: list[str],
    meetings_merged: list[str],
) -> str:
    lines = []
    lines.append("# Mailgreier Batch Mapping Report (2026-02-13)")
    lines.append("")
    lines.append(f"- Batch ID: `{BATCH_ID}`")
    lines.append(f"- Source folder: `{SOURCE_FOLDER_LABEL}`")
    lines.append(f"- Total files parsed: **{len(parsed_files)}**")
    lines.append(f"- Documents upserted: **{len(new_doc_records)}**")
    lines.append(f"- Meetings added: **{len(meetings_added)}**")
    lines.append(f"- Meetings merged: **{len(meetings_merged)}**")
    lines.append("")
    lines.append("## Files by category")
    category_counts = {}
    for p in parsed_files:
        category_counts[p.category] = category_counts.get(p.category, 0) + 1
    for k, v in sorted(category_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Meeting updates")
    if meetings_added:
        lines.append("- Added:")
        for item in meetings_added:
            lines.append(f"  - {item}")
    if meetings_merged:
        lines.append("- Merged into existing:")
        for item in meetings_merged:
            lines.append(f"  - {item}")
    if not meetings_added and not meetings_merged:
        lines.append("- No meeting changes.")
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- Duplicate handling is non-destructive: grouped via `duplicate_group` with `variant_of_doc_id`."
    )
    lines.append("- `source_batch` and `checksum_sha256` added for traceability.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Import mailgreier batch into project database")
    parser.add_argument(
        "--batch-folder",
        default=BATCH_FOLDER_NAME,
        help="Folder containing batch files",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    batch_folder = (root / args.batch_folder).resolve()
    if not batch_folder.exists():
        raise SystemExit(f"Batch folder not found: {batch_folder}")

    documents_path = root / "data" / "documents.json"
    meetings_path = root / "data" / "meetings.json"
    nabomerknader_path = root / "data" / "themes" / "nabomerknader.json"
    nabosvar_path = root / "data" / "themes" / "nabomerknad-svar.json"
    config_path = root / "data" / "config.json"
    inventory_path = root / "analysis" / "2026-02-13_mailgreier_inventory.json"
    mapping_report_path = root / "analysis" / "2026-02-13_mailgreier_mapping_report.md"

    parsed_files = parse_batch(batch_folder)

    # 1) Documents upsert
    documents = load_json(documents_path)
    docs_list: list[dict[str, Any]] = documents.get("documents", [])
    existing_by_checksum = {d.get("checksum_sha256"): d for d in docs_list if d.get("checksum_sha256")}
    existing_by_name = {d.get("file_name"): d for d in docs_list if d.get("file_name")}

    batch_records: list[dict[str, Any]] = []
    upserted_records: list[dict[str, Any]] = []
    for parsed in parsed_files:
        record = build_doc_record(parsed)
        batch_records.append(record)

        match = existing_by_checksum.get(record["checksum_sha256"]) or existing_by_name.get(record["file_name"])
        if match:
            # Non-destructive update for traceability fields only.
            for k, v in record.items():
                if k in {
                    "source_batch",
                    "checksum_sha256",
                    "derived_from",
                    "size_bytes",
                    "document_type",
                    "category",
                    "source_folder",
                    "email_subject",
                    "email_date",
                    "email_from",
                    "email_to",
                    "email_cc",
                    "event_summary",
                    "event_date",
                    "event_uid",
                    "title",
                    "headings",
                    "page_count",
                }:
                    match[k] = v
            upserted_records.append(match)
        else:
            docs_list.append(record)
            existing_by_checksum[record["checksum_sha256"]] = record
            existing_by_name[record["file_name"]] = record
            upserted_records.append(record)

    batch_docs_live = [
        d
        for d in docs_list
        if d.get("source_batch") == BATCH_ID and d.get("source_folder") == SOURCE_FOLDER_LABEL
    ]
    assign_duplicate_groups(batch_docs_live)

    documents["documents"] = docs_list
    metadata = documents.setdefault("metadata", {})
    metadata["last_updated"] = TODAY
    metadata["total"] = len(docs_list)
    metadata["total_documents"] = len(docs_list)
    by_cat = {}
    for d in docs_list:
        cat = d.get("category") or "other"
        by_cat[cat] = by_cat.get(cat, 0) + 1
    metadata["by_category"] = dict(sorted(by_cat.items(), key=lambda kv: kv[0]))
    write_json(documents_path, documents)

    # 2) Meetings upsert from ICS (+ EML calendars)
    meetings = load_json(meetings_path)
    meetings_list: list[dict[str, Any]] = meetings.get("meetings", [])
    # Idempotency: regenerate all batch-imported invitation meetings from scratch.
    meetings_list = [
        m
        for m in meetings_list
        if not (m.get("source_batch") == BATCH_ID and m.get("type") == "Møteinvitasjon")
    ]

    meeting_candidates: list[dict[str, Any]] = []
    for parsed in parsed_files:
        if parsed.ext == "ics":
            c = candidate_from_ics_event(parsed.parsed, parsed.file_name)
            if c:
                meeting_candidates.append(c)
        elif parsed.ext == "eml" and has_meeting_signal_eml(parsed):
            for idx, event in enumerate(parsed.parsed.get("calendar_parts", [])):
                c = candidate_from_ics_event(event, parsed.file_name)
                if c:
                    c["ingest_confidence"] = "medium"
                    # Keep deterministic id if multiple calendar parts in same email.
                    if idx > 0:
                        c["id"] = f"{c['id']}_{idx+1}"
                    meeting_candidates.append(c)

    # Consolidate duplicates among candidates first.
    consolidated_candidates: list[dict[str, Any]] = []
    for candidate in meeting_candidates:
        existing = find_matching_meeting(consolidated_candidates, candidate)
        if existing:
            merge_meeting(existing, candidate)
        else:
            consolidated_candidates.append(candidate)

    meetings_added: list[str] = []
    meetings_merged: list[str] = []
    for candidate in consolidated_candidates:
        existing = find_matching_meeting(meetings_list, candidate)
        label = f"{candidate.get('date')} | {candidate.get('title')}"
        if existing:
            merge_meeting(existing, candidate)
            meetings_merged.append(label)
        else:
            meetings_list.append(candidate)
            meetings_added.append(label)

    meetings_list.sort(key=lambda m: (m.get("date") or "0000-00-00", m.get("title") or ""))
    meetings["meetings"] = meetings_list
    mmeta = meetings.setdefault("metadata", {})
    mmeta["last_updated"] = TODAY
    mmeta["total_meetings"] = len(meetings_list)
    write_json(meetings_path, meetings)

    # 3) Nabomerknader traceability enrichment
    nabomerknader = load_json(nabomerknader_path)
    remarks: list[dict[str, Any]] = nabomerknader.get("remarks", [])

    # Build fast index for batch docs by normalized name.
    batch_docs_by_norm = {}
    for doc in batch_docs_live:
        n = normalize_text(str(doc.get("file_name", "")))
        if n:
            batch_docs_by_norm[n] = doc

    source_index: list[dict[str, Any]] = []
    for remark in remarks:
        source_file = remark.get("source_file") or ""
        source_norm = normalize_text(source_file)
        linked_docs: list[str] = []
        linked_doc_ids: list[str] = []

        if source_norm and source_norm in batch_docs_by_norm:
            doc = batch_docs_by_norm[source_norm]
            linked_docs.append(doc["file_name"])
            linked_doc_ids.append(doc["id"])
            dup_group = doc.get("duplicate_group")
            if dup_group:
                variants = [d for d in batch_docs_live if d.get("duplicate_group") == dup_group]
                for v in variants:
                    if v["file_name"] not in linked_docs:
                        linked_docs.append(v["file_name"])
                        linked_doc_ids.append(v["id"])

        if linked_docs:
            remark["source_documents"] = sorted(set(linked_docs))
            remark["source_doc_ids"] = sorted(set(linked_doc_ids))
            remark["source_batch"] = BATCH_ID

        source_index.append(
            {
                "remark_id": remark.get("id"),
                "source_file": source_file,
                "source_documents": remark.get("source_documents", []),
                "source_doc_ids": remark.get("source_doc_ids", []),
            }
        )

    nmeta = nabomerknader.setdefault("metadata", {})
    nmeta["last_updated"] = TODAY
    batches = nmeta.get("source_batches", [])
    if not isinstance(batches, list):
        batches = []
    if not any(b.get("id") == BATCH_ID for b in batches if isinstance(b, dict)):
        batches.append(
            {
                "id": BATCH_ID,
                "source_folder": SOURCE_FOLDER_LABEL,
                "ingested_date": TODAY,
                "files_total": len(parsed_files),
                "files_linked_to_remarks": len(
                    {
                        d
                        for r in remarks
                        for d in r.get("source_documents", [])
                        if isinstance(r.get("source_documents"), list)
                    }
                ),
            }
        )
    nmeta["source_batches"] = batches
    nabomerknader["source_index"] = source_index
    recalc_nabomerknad_stats(nabomerknader)
    write_json(nabomerknader_path, nabomerknader)

    # 4) Nabomerknad-svar evidence updates
    nabosvar = load_json(nabosvar_path)
    smeta = nabosvar.setdefault("metadata", {})
    smeta["last_updated"] = TODAY
    sbatches = smeta.get("source_batches", [])
    if not isinstance(sbatches, list):
        sbatches = []
    if BATCH_ID not in sbatches:
        sbatches.append(BATCH_ID)
    smeta["source_batches"] = sbatches

    extra_refs_by_theme = {
        "DISP": [
            f"{SOURCE_FOLDER_LABEL}/Oppsummering fra meknader i saksnr 202521699.docx",
            f"{SOURCE_FOLDER_LABEL}/Svar_ Ved. Hovfaret - nabomerknader uttalelser.eml",
        ],
        "DOK": [
            f"{SOURCE_FOLDER_LABEL}/Oppsummering av merknadene fra Engebretsvei 2 og 6.docx",
            f"{SOURCE_FOLDER_LABEL}/Svar_ Hovfaret 13 - Nabomerknader.eml",
        ],
        "SOL": [
            f"{SOURCE_FOLDER_LABEL}/Merknad-til-nabovarsel-1-20251230-BORETTSLAGET-HOFFSBYEN-HAGEBY.pdf",
        ],
        "VASSDRAG": [
            f"{SOURCE_FOLDER_LABEL}/Henvendelse om fagvurdering_ Sjøørret og skyggeeffekt ved Hovfaret 13.eml",
        ],
    }
    for theme in nabosvar.get("themes", []):
        code = theme.get("theme_code")
        extras = extra_refs_by_theme.get(code, [])
        if not extras:
            continue
        refs = theme.get("evidence_refs")
        if not isinstance(refs, list):
            refs = []
        for ref in extras:
            if ref not in refs:
                refs.append(ref)
        theme["evidence_refs"] = refs
    write_json(nabosvar_path, nabosvar)

    # 5) Config metrics sync
    config = load_json(config_path)
    config.setdefault("metadata", {})["last_updated"] = TODAY
    metrics = config.setdefault("metrics", {})
    metrics["documents_total"] = len(docs_list)
    metrics["meetings_total"] = len(meetings_list)
    write_json(config_path, config)

    # 6) Analysis outputs
    inventory = build_inventory(parsed_files)
    write_json(inventory_path, inventory)
    mapping = build_mapping_report(
        parsed_files=parsed_files,
        new_doc_records=batch_docs_live,
        meetings_added=meetings_added,
        meetings_merged=meetings_merged,
    )
    mapping_report_path.write_text(mapping, encoding="utf-8")

    print("=== Mailgreier import complete ===")
    print(f"Batch folder: {batch_folder}")
    print(f"Parsed files: {len(parsed_files)}")
    print(f"Documents total: {len(docs_list)}")
    print(f"Meetings total: {len(meetings_list)}")
    print(f"Meetings added: {len(meetings_added)}")
    print(f"Meetings merged: {len(meetings_merged)}")
    print(f"Nabomerknader remarks: {len(remarks)}")
    print(f"Inventory: {inventory_path.relative_to(root)}")
    print(f"Mapping report: {mapping_report_path.relative_to(root)}")


if __name__ == "__main__":
    main()
