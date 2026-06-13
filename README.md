# OpenTax
Open-source US tax prep. 100% local, print-and-mail, no e-file, no network, no LLM for the user.

> **SKELETON / PROOF OF CONCEPT.** All numbers in `constants.py` are PLACEHOLDER
> zeros. Do **not** file anything from this. Fill real values from official IRS
> PDFs in `years/2025/federal/source_pdfs/` first. See `CLAUDE.md` for the rules.

## Run
```bash
python3 cli.py demo        # end-to-end pipeline on sample inputs
python3 -m pytest -q       # engine + form-wiring tests (6 pass)
```

## Layout
```
engine/                tax-agnostic core (never changes per year)
  money.py             Decimal, whole-dollar, half-up. fail-loud need()/Missing
  form.py              Form + Ctx (upstream line reads)
  solver.py            topo-sort by depends_on, run each form once
  registry.py          form modules register here
years/2025/federal/
  constants.py         DATA ONLY — brackets, std deduction, phaseouts (PLACEHOLDER)
  forms/               f1040, sch1, sch8812, sch_eic  (compute(inp, ctx) -> lines)
  pdf_maps/f1040.json  line_id -> pdf acroform field
  source_pdfs/         drop IRS blank + INSTRUCTION PDFs here
  tests/               engine tests + Pub-1436 case templates
ui/                    ingest -> parsers -> review -> fill_pdf  (one inputs dict in,
                       one solution dict out; parsers never feed compute directly)
cli.py                 local pipeline driver
```

## Pipeline
`ingest → parse → confirm/edit → compute → review/override → fill PDF`.
Each stage is its own module; user can stop and edit at any stage.

## Next steps (one form at a time, with its instruction PDF)
1. Drop IRS f1040 + instruction PDFs into `source_pdfs/`.
2. Fill `constants.py` numbers FROM the PDF (never from memory).
3. Fill expected values in `tests/cases/*.json` from IRS Pub 1436; tests assert exact.
4. Wire real parsers (`ui/parsers/`) and PDF stamping (`ui/fill_pdf.py` needs pypdf).
