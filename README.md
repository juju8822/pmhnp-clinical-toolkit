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

Repository: https://github.com/juju8822/pmhnp-clinical-toolkit. Never upload real visit text or exported clinical reviews. Use development branches for subsequent work. Add an appropriate source-code license before redistribution.


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

## Searchable therapy companions — November 17, 2026

The Therapies tab now includes 15 searchable modalities: CBT, DBT, ACT, IPT, behavioral activation, ERP, exposure-based CBT, CPT, prolonged exposure, EMDR, CBT-I, motivational interviewing, family psychoeducation, behavioral parent training, and CBT for psychosis. Search by therapy, abbreviation, or associated diagnosis. The modality bar appears only in Therapies; relevant links remain on individual diagnosis cards. Links from the clinical workspace open a separate page to preserve memory-only visit work.

Each standalone therapy page has four accessible tabs: Overview & diagnoses, Patient tools & print, Discussion guide, and Evidence & research. The 30 original printable resources (one patient handout and one discussion guide per modality) support shared goals and between-session practice with a therapist. They are not validated standalone treatments or reproductions of proprietary worksheets. Trauma resources focus on preparation/support; CBT-I does not provide unsupervised sleep restriction. Evidence summaries distinguish clinical guidelines, trials, and patient education, with population limits and 23 linked sources. Evidence for full therapies does not validate these companion handouts.

`therapy-catalog.json` is the canonical content dataset; its offline copy is embedded in `index.html`. Run `python3 build-therapies.py` after catalog edits to regenerate the 15 `therapy-*.html` pages, and synchronize the embedded catalog. Keep all HTML pages together when downloading the app; opening `index.html` alone without the other pages will leave therapy links unavailable. Handout notes remain in memory and print as literal text, including long notes. Browser print controls can print or save a PDF using the device's supported print dialog.

`npm test` now runs code/data checks and 51 simulated-DOM workflow checks (27 diagnosis, 12 medication, 12 therapy). Therapy tests cover directory search, diagnosis associations, direct links, all 15 pages, keyboard tabs, source completeness, print targeting, note escaping and clearing, and runtime errors. Browser spot-checks covered the directory, PTSD search, CPT page and tabs. Native print dialog/output, mobile devices and clinical validation remain unverified.

## Sidebar navigation — November 17, 2026

The five clinical topics now use a sticky left sidebar with vertical tab semantics and Up/Down keyboard navigation. The therapy modality bar and directory search live in Therapies only; the duplicated diagnosis-page therapy finder was removed. Tropical colors and 14 pt headings/12 pt body text remain. Existing code/data checks and all 51 workflow checks pass; desktop browser navigation and layout were spot-checked.

## Visual worksheet library — November 21, 2026

Therapies includes 16 separate visual cards from the user-supplied Worksheets workbook (15 exercises plus its cover), compiled by Eshaa Pitty. Every card has a page thumbnail, title, short description, standalone print preview and original single-page PDF. The complete original workbook is retained as `worksheets-source.pdf`, with original attribution and artwork. `worksheets-manifest.json` records page ordering and source hash. Handout search is independent of the modality directory. These supplied worksheets are adjunct teaching resources, not independently validated treatments. Images are scans; they do not provide a full accessible text transcription.

Keep the worksheet HTML, JPG, PDF and source PDF files beside `index.html` when downloading. Preview pages are self-contained with full-page images; PDF links retain the source page. `worksheet-test.cjs` checks all cards and assets, print handlers, source attribution, search, empty state and clearing.

## Imported U.S. strengths and forms — November 2026

The Medication tab opens an offline RxTerms browser with 8,497 product-name/presentation groups and 18,936 active unsuppressed SCD/SBD strength/form records from the official 202611 release. Search generic names, brands, aliases and formulations; filter by route/presentation and brand/generic status. Results paginate. Selecting a product displays exact forms, source product descriptions, strengths and RxCUIs. Numeric release intervals in source names are retained in the form selector. Full descriptions preserve combination ingredient/strength identity and salt distinctions.

Product strengths are distinct from treatment doses, indication-specific regimens, tablet splitting, FDA approval, interchangeability and pharmacy stock. Suppressed/retired records and packs are excluded. This is a dated imported snapshot and includes all routes, not solely psychiatric drugs. The new catalog does not supply recommended dosing for every product. Existing selected label-checked regimen references remain below it. DailyMed links open product-label search; users must choose the matching formulation, release type and manufacturer to read prescribing details. No label is silently selected or parsed into a prescription.

`rxterms-catalog.json` includes official source URL, release and source ZIP hash. It is also embedded into `index.html` for offline use. To refresh: download a current official RxTerms monthly ZIP and run `python3 import-rxterms.py /path/to/RxTermsYYYYMM.zip`. The importer rebuilds both data copies and excludes retired/suppressed entries and packs. No runtime API requests, credentials or patient data are needed. This adds about 5 MB to the HTML. Clinical validation and mobile-device performance have not been completed.

`rxterms-test.cjs` adds eight functional checks for catalog equality/accounting, search, release-form separation, route/brand filters, empty states, pagination, preservation of review state, combination descriptors and runtime errors. Existing tests and worksheet checks also pass. Browser spot-checks cover bupropion search, release-form selection and displayed descriptions.

Sources: https://lhncbc.nlm.nih.gov/MOR/RxTerms/ and https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm . RxTerms is maintained by the U.S. National Library of Medicine; U.S. availability is approximate. Refer to source documentation for scope and updates.

## Browsable mental health medication directory

The Medication page now shows 144 psychiatric and related-care medicines/combinations as collapsed clickable cards, searchable by generic/brand name and category. The four example shortcuts and auto-selected Sertraline section have been replaced. Imported strengths, formulations, DailyMed searches and study-file provenance live inside each medication. Existing selected dosing references, safety/monitoring records and indication/age-specific regimens are also linked within the appropriate medication card; none opens automatically. Missing detailed monographs and RxTerms snapshot gaps are explicit.

Coverage includes antidepressants, antipsychotics, mood/anticonvulsant references, anxiety/adjuncts, ADHD, sleep/wakefulness, addiction/reversal, cognition, movement-effect adjuncts and specialist depression treatments. Categories organize a broad directory; they do not establish an approved indication or efficacy for every item and are not an exhaustive worldwide inventory of off-label uses. Original source-mentioned medicines are retained. Strengths include single-ingredient and combination products where the ingredient appears; full descriptions preserve ingredient, salt and release distinctions.

`mental-health-medications.json` is canonical and embedded in `index.html`. It records source links, curated names/aliases, category metadata, references and matched RxTerms group names. The monthly RxTerms importer now refreshes these name-group mappings and both embedded datasets together. New `mental-health-test.cjs` covers initial collapsed cards, source-name coverage, brand/category search, inline strengths, release/salt descriptions, selected dosing and safety references, explicit gaps, and preservation of clinical review state. The existing RxTerms test was updated for the new browse prompt.

## Medication class colors and simplified cards

Medication cards now use distinct class colors with matching text tags and an optional color key. The first class determines the card color; additional class tags retain their own colors. User-facing RxCUI numbers, the formulation-choice banner, and DailyMed navigation links were removed from the medication cards and strength details. Source identifiers and source URLs remain in the underlying catalogs. Dosing/safety content and strength/form descriptions remain available in expandable cards. Existing workflow checks were updated to verify the simplified display.


### Clickable medication class key
Each color-key item is now a keyboard-accessible filter button. Selecting a class clears the name search and shows all medicines tagged with that class, including secondary classes. The category selector and pressed button stay synchronized. All classes restores the full directory.


### Compact diagnosis cards and group filters
Diagnosis cards start collapsed in a compact grid. Select a diagnosis to expand its timeframe, findings, required review and therapy references. Group colors and clickable color-key filters organize the existing seven diagnosis groups; progress remains yellow for partial review and green for complete review, with group tags retained. Expansion survives checkbox changes and filtering. A newly completed review opens the diagnosis and its medication reference panel. Group filters combine with progress filters and preserve visit findings.


### Oral strengths, concise safety bullets and monitoring
The 144 medication cards show selected usual oral product strengths while collapsed, with separate IR/ER, salt, combination-ingredient order and route labels. These are product strengths, not prescribed daily doses or an exhaustive manufacturer/stock inventory. Adderall includes 7.5 and 12.5 mg IR strengths; XR strengths remain separate. Liquids, sublingual products, nonoral medicines, supplements and historical listings are identified explicitly. Full RxTerms formulation groups remain inside each medication.

Opening a card shows up to ten selected common/reported effects, a separate uncapped list of important serious risks, a test/timing/basis table, and clinical monitoring separate from labs. A universal ranked top ten is not claimed: source populations, indications and formulations differ. Medication-specific exceptions supplement shared safety profiles. No numerical frequency ranking is invented. Clinical review remains required before patient use; these are concise adult-oriented references, not complete monographs or validated prescribing recommendations.

`medication-quick-reference.json` is the canonical curated dataset and is embedded in `index.html` for offline use. Keep them synchronized. References identify selected FDA SPL label records, dates, monitoring guidance and historical exceptions. Labels were retrieved through the official openFDA label API on 2026-11-24; melatonin uses NCCIH, Symbyax uses an FDA PDF, maprotiline a historical FDA label, and brexanolone a historical product label. No DailyMed link is added to the UI. Guideline monitoring schedules supplement U.S. labeling and are identified as guideline-based. Unspecified periodic intervals stay unspecified; risk/symptom-triggered testing is distinct from routine testing. No patient data, background API calls or credentials are introduced.

The RxTerms importer does not refresh the curated quick-reference data. Review and update both its oral strength selections and clinical summaries when labels or monitoring guidance change. `medication-quick-test.cjs` verifies all 144 summaries, the ten-item cap, combination/salt/release identity, key monitoring schedules, source presence, data equality and rendering. Functional tests and browser checks do not constitute clinical validation.


### Education reference PDF
The Education topic grid includes the supplied DSM-5-TR manual as a searchable clinician-reference card, with Open PDF and Download PDF actions. `dsm-5-tr-reference.pdf` preserves the supplied file unchanged (1,906 PDF pages; SHA-256 ab7f29bf55dedd597bb4c94fc69fe3e6293bb1923fc7628a75173c745ac762bf). Keep this PDF beside `index.html` when downloading the app. The browser PDF viewer provides search and printing; the existing on-device DSM picker in Diagnoses remains available. This resource does not change the diagnosis matcher or reproduce criteria into its assessment prompts.


### Linked Google Drive book collection
Education includes the supplied Psychology Books folder link and an offline title index of 228 book/reference files across 38 subjects (39 folder paths including the nested Essentials assessment collection). Search title/author/edition/subject, filter by subject, and expand an individual card to open the original book or source folder in Drive. Twelve cards show initially; Show more books paginates the filtered matches. `education-books.json` is the canonical catalog, embedded into `index.html`; keep them synchronized. Titles/editions are derived from source filenames observed November 24, 2026, rather than inferred from book contents. Files remain in Drive and no background Drive request or account credential is used by the app. This is a dated index; changes and access depend on the source owner. The book files are not copied into this repository.
