# Skøyen områderegulering – vedtakspunkt 6 (dokumentpakke)

Denne mappen samler «smøla» av dokumenter om vedtakspunkt 6 for sporbarhet og gir en **oversiktsrapport** som forklarer problemstillingen uten å gå i detalj på enkeltprosjekter.

## Innhold

- `raw/` – importerte originalfiler (PDF/MD) med ryddige filnavn
- `extract/text/` – søkbar tekst per dokument (`DOC-xxx.txt`)
- `index.json` / `index.csv` – maskinlesbar dokumentindeks
- `rapport.md` / `rapport.html` / `rapport.pdf` – oversiktsrapport

## Bygg/oppdater

```bash
python3 scripts/omraderegulering/import_and_index.py
python3 scripts/omraderegulering/build_report.py
```

## Kilder
Standardkilde (kan overstyres med `--src`): `~/Downloads/områderegulering`

