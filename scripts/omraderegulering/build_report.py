#!/usr/bin/env python3
"""
Build a high-level overview report (Markdown + HTML + PDF) from index.json.

Pipeline:
  1) scripts/omraderegulering/import_and_index.py
  2) scripts/omraderegulering/build_report.py

PDF generation uses:
  pandoc -> HTML
  chromium --headless --print-to-pdf -> PDF
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import date, datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _today_iso() -> str:
    return date.today().isoformat()


def _doc_ref(doc: dict[str, Any]) -> str:
    return f"{doc['id']} ({doc.get('doc_type')}{', ' + doc['date'] if doc.get('date') else ''})"


def _pick_doc(docs: list[dict[str, Any]], *, must_have_topics: list[str] | None = None, doc_type: str | None = None) -> dict[str, Any] | None:
    for d in docs:
        if doc_type and d.get("doc_type") != doc_type:
            continue
        if must_have_topics:
            topics = set(d.get("key_topics") or [])
            if not all(t in topics for t in must_have_topics):
                continue
        return d
    return None


def _find_quote(docs: list[dict[str, Any]], needle: str) -> tuple[dict[str, Any], dict[str, Any]] | None:
    n = needle.lower()
    for d in docs:
        for q in d.get("quotes") or []:
            if n in (q.get("text") or "").lower():
                return d, q
    return None


def _render_quotes_block(quotes: list[tuple[dict[str, Any], dict[str, Any]]]) -> str:
    out: list[str] = []
    for doc, q in quotes:
        p = q.get("page")
        page_part = f", s. {p}" if p else ""
        out.append(f"> {q.get('text')}\n>\n> Kilde: {_doc_ref(doc)}{page_part}\n")
    return "\n".join(out).rstrip() + "\n"


def _build_timeline_rows(docs: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for d in docs:
        if not d.get("date"):
            continue
        rows.append(
            {
                "date": d["date"],
                "event": d.get("1line_summary") or d.get("title") or d["id"],
                "source": d["id"],
            }
        )
    rows.sort(key=lambda r: (r["date"], r["source"]))
    return rows


def _build_markdown(index: dict[str, Any]) -> str:
    docs: list[dict[str, Any]] = index.get("documents") or []
    bundle = index.get("bundle") or {}

    # Key anchor documents
    byrådssak = _pick_doc(docs, doc_type="byrådssak")
    politisk = _pick_doc(docs, doc_type="politisk_sak")
    hovfaret = _pick_doc(docs, must_have_topics=["hovfaret-13"])

    quote_oppheves = _find_quote(docs, "vedtakspunkt 6") or _find_quote(docs, "oppheves")
    quote_normalsituasjon = _find_quote(docs, "normalsituasjon")
    quote_stoppe_for_start = _find_quote(docs, "stoppe s før start") or _find_quote(docs, "stoppe før start")
    quote_pbe_avvise = _find_quote(docs, "pbe kan avvise alternative planer")
    quote_vedtakspunkt6_ordlyd = _find_quote(docs, "Det skal tillates fremmet detaljreguleringer")

    quotes: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for q in [
        quote_oppheves,
        quote_normalsituasjon,
        quote_pbe_avvise,
        quote_stoppe_for_start,
        quote_vedtakspunkt6_ordlyd,
    ]:
        if q and q not in quotes:
            quotes.append(q)

    timeline = _build_timeline_rows(docs)

    md: list[str] = []
    md.append("# Skøyen områderegulering – vedtakspunkt 6")
    md.append("")
    md.append("**Oversiktsrapport (internt notat)**  ")
    md.append(f"**Dato:** {_today_iso()}  ")
    md.append(f"**Kildepakke:** {bundle.get('source_dir', 'ukjent')} (importert til repo)  ")
    md.append("")

    md.append("## Executive summary")
    md.append("- Dette dokumentsettet handler om **vedtakspunkt 6** i bystyrets vedtak om **Områderegulering for Skøyen** (27.09.2023, sak 332/23).")
    md.append("- Byrådet foreslår å **oppheve vedtakspunkt 6** (sak fremmet for politisk behandling i Byutviklingsutvalget 11.02.2026).")
    md.append("- Begrunnelsen (kort fortalt): Punktet har i praksis skapt **usikkerhet** og bidratt til at **avvikende/alternative planforslag stoppes før politisk behandling**, og byrådet ønsker en «normalsituasjon» etter plan- og bygningsloven.")
    if byrådssak:
        md.append(f"- Primærkilde: {_doc_ref(byrådssak)}.")
    if politisk:
        md.append(f"- Saksflyt/utvalgsbehandling: {_doc_ref(politisk)}.")
    md.append("")

    md.append("## 1. Hva er vedtakspunkt 6 (forenklet)?")
    md.append("Vedtakspunkt 6 er et politisk vedtak knyttet til **«Utnyttelse og formål»** i områdeplanen. Intensjonen (slik den ofte blir omtalt) har vært å åpne for at det kan fremmes **avvikende detaljreguleringer** dersom de gir bedre miljømessig/sosial bærekraft og stedstilpasset byutvikling.")
    if quote_vedtakspunkt6_ordlyd:
        md.append("")
        md.append("Utdrag av ordlyd (fra dokumentpakken):")
        md.append("")
        md.append(_render_quotes_block([quote_vedtakspunkt6_ordlyd]))
    md.append("")

    md.append("## 2. Hva er den politiske saken 11.02.2026?")
    md.append("Byrådets innstilling er å **oppheve** vedtakspunkt 6, fremfor å endre ordlyden. Begrunnelsen er at endringer kan åpne for nye tolkninger og vilkår og dermed skape ny usikkerhet.")
    if quote_oppheves or quote_normalsituasjon:
        md.append("")
        md.append("Kjerneformuleringer fra sakens sammendrag:")
        md.append("")
        md.append(_render_quotes_block([q for q in [quote_oppheves, quote_normalsituasjon] if q]))
    md.append("")

    md.append("## 3. Kjerneproblematikk: «stoppe før start» (samlet)")
    md.append("Dokumentpakken peker på et mønster der kommunal praksis/tolkning knyttet til vedtakspunkt 6 (og krav om flere planalternativer) kan gi følgende effekt:")
    md.append("- Beslutning flyttes fra politisk nivå til etatsnivå (PBE/administrasjon).")
    md.append("- Alternative planer kan avvises før politisk behandling.")
    md.append("- Kostnad og risiko blir høy fordi det kan kreves to «fullverdige» planforslag.")
    md.append("- Resultatet blir lavere investeringsvilje og lavere aktivitet på Skøyen – til tross for store offentlige investeringer (Fornebubanen).")
    if quote_pbe_avvise or quote_stoppe_for_start:
        md.append("")
        md.append("Utdrag fra presentasjoner i dokumentpakken:")
        md.append("")
        md.append(_render_quotes_block([q for q in [quote_pbe_avvise, quote_stoppe_for_start] if q]))
    md.append("")

    md.append("## 4. Tidslinje (basert på dokumentdatoer i pakken)")
    md.append("| Dato | Hendelse (kort) | Kilde |")
    md.append("|---|---|---|")
    for r in timeline:
        md.append(f"| {r['date']} | {r['event'].replace('|', '-')} | {r['source']} |")
    md.append("")

    md.append("## 5. Aktørbilde (hvem som går igjen i dokumentene)")
    md.append("- **Oslo kommune:** Bystyret, Byutviklingsutvalget, Byrådsavdeling for byutvikling, Plan- og bygningsetaten (PBE).")
    md.append("- **Stat:** Kommunal- og distriktsdepartementet (KDD) (innsigelsesbehandling/stadfesting).")
    md.append("- **Grunneiere/utbyggere/fora:** OMA / Skøyen grunneierforum/områdeforum, samt flere private aktører (i vedleggsliste og e-poster).")
    md.append("")

    md.append("## 6. Konsekvens for Hovfaret 13 (oversiktsnivå)")
    md.append("Hovfaret 13 er nevnt/vedlagt i sakens dokumentpakke (som eksempel på problemstillingen). Oppheving av vedtakspunkt 6 vil ikke i seg selv gi en automatisk tillatelse, men kan redusere en ekstra politisk/administrativ barriere ved behandling av avvikende forslag.")
    if hovfaret:
        md.append(f"- Relevante vedlegg i pakken: {_doc_ref(hovfaret)}.")
    md.append("")

    md.append("## Vedlegg A: Dokumentoversikt")
    md.append("| ID | Dato | Type | Tittel | Kort innhold | Fil |")
    md.append("|---|---|---|---|---|---|")
    for d in sorted(docs, key=lambda x: x["id"]):
        d_date = d.get("date") or ""
        d_type = d.get("doc_type") or ""
        title = (d.get("title") or "").replace("|", "-")
        summary = (d.get("1line_summary") or "").replace("|", "-")
        rel = d.get("imported_path") or ""
        md.append(f"| {d['id']} | {d_date} | {d_type} | {title} | {summary} | `{rel}` |")
    md.append("")

    md.append("## Vedlegg B: Hvordan regenerere rapporten")
    md.append("1. Importer/oppdater indeks:")
    md.append("")
    md.append("```bash")
    md.append("python3 scripts/omraderegulering/import_and_index.py")
    md.append("```")
    md.append("")
    md.append("2. Bygg rapport (MD/HTML/PDF):")
    md.append("")
    md.append("```bash")
    md.append("python3 scripts/omraderegulering/build_report.py")
    md.append("```")
    md.append("")

    return "\n".join(md).rstrip() + "\n"


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _run_pandoc(md_path: Path, html_path: Path, css_path: Path) -> None:
    if not _cmd_exists("pandoc"):
        raise RuntimeError("pandoc not found in PATH")
    cmd = [
        "pandoc",
        str(md_path),
        "--standalone",
        "--toc",
        "--toc-depth=3",
        "--metadata",
        "title=Skøyen områderegulering – vedtakspunkt 6",
        "--css",
        str(css_path.name),
        "--embed-resources",
        "--output",
        str(html_path),
    ]
    subprocess.run(cmd, check=True, cwd=str(md_path.parent))


def _run_chromium(html_path: Path, pdf_path: Path) -> None:
    chromium = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chrome")
    if not chromium:
        raise RuntimeError("chromium/google-chrome not found in PATH")
    url = html_path.resolve().as_uri()
    cmd = [
        chromium,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        url,
    ]
    subprocess.run(cmd, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build report from an index.json file.")
    parser.add_argument(
        "--out",
        type=Path,
        default=BASE_DIR / "documents" / "omraderegulering-skoyen-vedtakspunkt6",
        help="Output directory (must contain index.json)",
    )
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    args = parser.parse_args(argv)

    out_dir: Path = args.out
    index_path = out_dir / "index.json"
    css_path = out_dir / "report.css"

    if not index_path.exists():
        raise SystemExit(f"Missing index.json: {index_path}. Run import_and_index.py first.")
    if not css_path.exists():
        raise SystemExit(f"Missing report.css: {css_path}.")

    index = _read_json(index_path)
    md = _build_markdown(index)

    md_path = out_dir / "rapport.md"
    html_path = out_dir / "rapport.html"
    pdf_path = out_dir / "rapport.pdf"

    _write_text(md_path, md)
    _run_pandoc(md_path, html_path, css_path)
    if not args.no_pdf:
        _run_chromium(html_path, pdf_path)

    print(f"Report written: {md_path}")
    print(f"HTML written: {html_path}")
    if not args.no_pdf:
        print(f"PDF written:  {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
