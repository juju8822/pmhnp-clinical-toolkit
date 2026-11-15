# Clinical Review — PMHNP developer starter

Open `index.html` in a modern desktop browser. No install, account, API key, or server is required. On iPad, download the source to a computer or serve it with a local development server; the Files preview may not execute JavaScript.

Optional local server: `python3 -m http.server 8000 --bind 127.0.0.1` from this folder, then visit http://127.0.0.1:8000.

## What works

- Paste a visit or import a UTF-8 TXT file (up to 1 MB).
- Extract literal phrases into six original screening domains and display the sentence as evidence.
- Manually mark each domain present, absent, unknown, or conflicting; confirm presence by checkbox.
- View broad differential pathways associated with confirmed built-in domains.
- Record assessment-completeness prompts and review notes.
- Export visit text and reviewed findings as JSON.
- Import an authorized checklist JSON library (up to 5 MB) using the downloadable schema example.
- View one sourced adult sertraline/MDD medication reference, separating tablet strength from daily dose.

## What is not implemented

This is not a complete DSM-5-TR app or a validated diagnostic tool. It has no full DSM content, AI extraction, validated criteria engine, diagnosis-specific duration/exclusion rules, PDF/DOCX imports, comprehensive drug catalog, prescription generation, patient database, or HIPAA-compliance certification. No individual diagnosis is confirmed. Do not use it to direct patient care.

The extractor is a literal-phrase demonstration. It intentionally does not classify negation, historical symptoms, family history, hypothetical statements, or temporal context. Every hit is unclassified. A denied hallucination statement or a relative's symptoms can appear as a hit. Manual review is mandatory. No match means unknown, not absent. Editing a visit clears prior confirmations. The safety domain is not a risk assessment or emergency-detection system.

Imported checklists have no automatic diagnostic mapping. A full implementation must model each diagnosis's rules, rather than apply a universal symptom count. Assessment prompt checkboxes do not satisfy diagnosis-specific gates.

## Full implementation architecture

1. Authorized, versioned content: diagnostic definitions, criterion groups, thresholds, mandatory criteria, duration, frequency, impairment, exclusions, age/context rules, specifiers, source references, and license metadata.
2. Visit extraction: typed observations with patient/other subject, assertion, time, source span, confidence, and contradictions. Treat note text as untrusted data, including instructions embedded in notes. An AI service should produce a constrained schema and never write diagnoses directly.
3. Evidence validation: verify each quoted span exists in the source and attach its original offsets. Keep model suggestions separate from clinician-confirmed facts. Test negation, family history, copied notes, contradictory reports, and incomplete visits.
4. Criteria engine: deterministic diagnosis-specific rules operating on reviewed observations. Output supported, unsupported, conflicting, or missing requirements. Show possible alternatives without fabricated probability scores. Require clinician adjudication.
5. Medication content: ingredient plus exact product, formulation, route, strength, source date, indication and approval status, population, starting dose, titration interval, labeled maximum, monitoring, major warnings, contraindications, and special-population adjustments. Clinical guideline recommendations require separate sources and review; a product label alone does not establish first-line status.
6. Prescription drafting: only after clinician selects an indication, product, dose, route, frequency and patient context. Calculate tablets per administration separately from daily dose. Check release formulations, manufacturer-specific split eligibility, daily maximum, interactions, allergies and relevant clinical factors. No automatic treatment from symptom matching.
7. Patient-data infrastructure: select an approved environment and vendor agreements before identifiable visits; add authentication, role access, encryption, audit history, retention/deletion, backups, and incident procedures. GitHub holds source and synthetic fixtures only.

Suggested future stack: TypeScript UI, a typed API, relational data storage, a constrained extraction service behind a server, and a separately tested rule engine. Keep credentials server-side. Choose hosting and data services after reviewing clinical-data requirements.

## Example medication record structure

```json
{
  "ingredient": "example ingredient",
  "product_id": "source-specific identifier",
  "route": "oral",
  "formulation": "immediate-release tablet",
  "strengths_mg": [],
  "indication": "specific condition",
  "population": "adult",
  "approval_status": "review required",
  "starting_dose": null,
  "titration": null,
  "maximum_daily_dose": null,
  "source_url": "",
  "source_revision": "",
  "clinical_review_status": "pending"
}
```

Do not interpret a tablet-strength inventory as a list of recommended daily doses. Formulations and indications cannot share a single universal dosing range. The sample product lists 25, 50, 100, 150 and 200 mg tablets; other product labels can differ. Market availability requires verification beyond label inclusion.

## Privacy behavior in this starter

No network requests, remote fonts, analytics, cookies, localStorage or database. Visit data lives in the page's memory; closing/reloading clears it. Clearing the visit removes it from the app's state, but cannot erase browser/OS memory or an exported file. Exported JSON includes the complete narrative. External reference links open only when clicked. This limited design is not proof of regulatory compliance.

## Content provenance

APA DSM electronic product licensing: https://www.appi.org/Support/Customer-Information/Permissions
APA copyright policy: https://www.psychiatry.org/copyright
DailyMed sample product: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=c9e89324-0834-4434-8168-b4f2fa1e0a08

Sources checked November 13, 2026. Arrange appropriate permission for intended DSM display and machine-processing uses before incorporating that content. Owning a book is not an app content license.

## Checks

Run `node test.cjs`. Tests cover keyword boundaries, literal phrase escaping, preserving denial/family-history statements as unclassified, missing evidence, library validation, and script syntax. Browser visual/interaction testing has not been completed. Clinical validation has not been performed.

## GitHub handoff

Repository: https://github.com/juju8822/pmhnp-clinical-toolkit (private). Never upload real visit text or exported clinical reviews. Use development branches for subsequent work. Add an appropriate source-code license before redistribution.


## Reference library update — November 13, 2026

Ten supplied course PDFs (158 total PDF pages) now inform 72 paraphrased summary/update cards across the five topic tabs. Each card identifies its source file and PDF page(s). A 152-page source catalog includes title, content, exam, and reference pages; blank notes pages are omitted. Indexed pages are not a claim of exhaustive transcription. Illustrations, exact criteria lists, quizzes, and original dosing tables are not reproduced. Source files & coverage lists pages without dedicated summaries explicitly.

The Medication tab includes a name/brand index plus six selected label-checked product references, separating tablet strengths, indication/population, start, titration, dose range, example instructions, cautions, and external labels. These are selected fields, not complete monographs or patient-specific prescriptions. The remaining source-mentioned medicines do not receive invented doses. Manufacturer strengths are not a market-wide inventory.

Primary-source updates flag clonidine ER, clozapine REMS, St. John's wort, benzodiazepine tapers, RLS management, lamotrigine rash, reproductive-safety framing, pediatric sertraline, and esketamine. Other course summaries remain subject to clinical review. The original demonstration diagnostic matcher is unchanged and has no licensed full DSM criteria.

`knowledge.json` is the editable structured reference dataset. It is also embedded into `index.html` to keep the app offline and avoid network requests. Keep both in sync when editing; `node test.cjs` checks equality, provenance, and other reference-library invariants. Source hashes and exclusions are documented in `SOURCE_NOTES.md`. No patient content or original PDF files are committed.


## Diagnosis cards — November 14, 2026

The Diagnoses tab now opens a board of 30 separate assessment cards. These are original prompts, not a full or licensed DSM-5-TR criteria library. They include psychiatric diagnostic possibilities plus selected sleep conditions already discussed in the study references. Some cards share symptom prompts; overlapping matches are not competing confirmed diagnoses.

- Neutral: no positive findings or required-review items are checked.
- Yellow: some findings or review items are checked, or transcript suggestions remain unconfirmed.
- Green: at least one positive finding is clinician-confirmed, no checked transcript finding remains unconfirmed, and every required manual review task has been confirmed. Green means review-task completion, not an autonomous diagnosis or validated DSM threshold result.

Positive symptom examples are optional; not all are required for every diagnosis. Required review tasks cover the actual symptom pattern/threshold, duration/frequency/course/development/settings, impairment, exclusions/differentials, and remaining clinician assessment/testing/safety. The clinician must verify those requirements against an authorized diagnostic source. No time threshold or exclusion is inferred from a keyword hit.

Transcripts use a conservative local phrase matcher. Matches in affirmative current patient statements can be prechecked as unconfirmed suggestions. Each includes literal source text and character offsets. Denials, historical and family context, questions/provider speech, unclear assertions, and conflicting positive/negative statements are held for review. This matcher is not validated NLP: it can miss findings or misread context. Every suggested finding requires review, and required-review tasks are always manual. Editing/importing a visit or changing a checklist clears card checks and notes. Clinical data remains memory-only.

Use the card search and progress filter to focus the board. Card checks and rationale are included in JSON review export, which also supports manual review without extraction. A custom checklist cannot enable the old default diagnostic mapping by reusing the default name/version.

Validation: `npm install` then `npm test` runs the existing code/data checks plus 22 simulated-DOM card-workflow checks. `jsdom` is used only for development tests, not by the offline app. These checks are not visual browser testing or clinical validation.


## Diagnosis-specific timeframes — November 14, 2026

All 30 assessment cards now show a prominent **Timeframe & course** section with paraphrased duration, frequency, developmental-onset, and relevant course/subtype details. The previously generic course checkbox appears beside that information and is required before green. Transcript matching never confirms the timeframe automatically. Timing references are linked on each card, and the displayed requirements and confirmation state are included in JSON exports. Conditions without a fixed minimum duration say so; subtype look-back periods are distinguished from core diagnostic duration.

This adds timing reference information, not a validated duration calculator or a full licensed DSM criteria engine. The clinician must verify the complete criteria and their applicability. Validation now includes 27 simulated-DOM workflow checks plus the existing syntax/data checks; visual browser and clinical validation remain outstanding.


## Medication panels beneath reviewed diagnoses — November 14, 2026

Completing a diagnosis review automatically opens a separate medication-reference card directly beneath that diagnosis. Removing a required review/confirmation, clearing checks, or changing the visit closes it. Completion is still review progress, not an autonomous diagnosis or treatment recommendation.

The new `diagnosis-medications.json` catalog contains **19 medications and 47 diagnosis/target/age-specific references across the 30 diagnosis cards**. This is a selected catalog, not all applicable medicines. Each entry separates formulation and available product strengths from the dose regimen, and displays common adverse effects, major contraindications, key warnings, possible labs, clinical monitoring, and primary label links. Adult and pediatric references are separated; pediatric coverage is limited and each entry names its age range. Off-label indications and extrapolated dose references are explicit. Medication choices are not ranked or preselected.

Cards with no detailed regimen explain the distinction between nonmedication care, off-label specialist treatment, and missing catalog coverage. Examples include core autism features versus pediatric irritability, OSA airway treatment versus residual sleepiness, and phase-specific bipolar treatment. Missing entries do not mean no medication options exist. Complete monographs, interaction screening, a full drug database, patient-specific renal/hepatic/pregnancy adjustments, full pediatric coverage, clozapine/LAIs, and clinical validation remain outside this prototype.

The JSON catalog is also embedded in `index.html` for offline use; keep both synchronized. `npm test` includes existing code/data tests, 27 diagnosis workflow checks, and 12 medication-panel checks. These are simulated-DOM functional checks, not visual browser or clinical validation. No patient data or original source PDFs are included.
