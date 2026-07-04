# Raw Data Refresh Procedure

This procedure updates the historical match snapshot without erasing the
provenance of a dataset previously used by MatchCast.

## Rules

- Never edit a downloaded raw CSV manually.
- Never use a moving branch URL as the final provenance identifier.
- Never replace or delete an existing provenance entry in
  `docs/data-sources.md`.
- Preserve each reviewed snapshot under a filename containing its full upstream
  commit SHA.
- Validate a new snapshot before making it the canonical development dataset.
- Commit source metadata, validation output, and code changes; do not commit the
  large raw CSV.

## Refresh Steps

1. Read the latest commit SHA from the upstream
   [`martj42/international_results`](https://github.com/martj42/international_results)
   repository.
2. Build an immutable URL in this form:

   ```text
   https://raw.githubusercontent.com/martj42/international_results/<commit-sha>/results.csv
   ```

3. Download to a new snapshot-specific path. Do not pass `--force` and do not
   reuse an existing filename:

   ```powershell
   python src/matchcast/ingestion/download_results.py `
     --output data/raw/snapshots/international_results_<commit-sha>.csv
   ```

   The downloader is pinned to the currently approved snapshot. Before using it
   for a new upstream commit, update and review `DEFAULT_COMMIT`,
   `DEFAULT_URL`, and `DEFAULT_SHA256` together, then run the downloader tests.

4. Record the new snapshot in `docs/data-sources.md` as an additional history
   entry with:

   - upstream repository and immutable file URL;
   - full commit SHA and upstream commit timestamp;
   - retrieval date;
   - local snapshot path;
   - byte size, row count, date range, and SHA-256;
   - licence and any newly observed limitations.

5. Generate a snapshot-specific validation report before promotion:

   ```powershell
   $env:PYTHONPATH = "src"
   python -c "from pathlib import Path; from matchcast.ingestion.report import write_validation_report; write_validation_report(Path('data/raw/snapshots/international_results_<commit-sha>.csv'), Path('reports/data_validation_<commit-sha>.json'))"
   ```

6. Compare the new and previous snapshots for:

   - inserted, removed, and changed historical matches;
   - schema changes;
   - newly completed fixtures and newly scheduled fixtures;
   - score, venue, neutral-flag, and team-name corrections;
   - validation failures or unexpected date ranges.

7. Promote the new snapshot to `data/raw/international_results.csv` only after
   review. Keep the commit-addressed snapshot and its metadata so the previous
   training input remains identifiable.
8. Regenerate `reports/data_validation.json`, run the full test suite, and
   commit the metadata, report, downloader pin, tests, and documentation.

## Recovery

If a refresh fails validation, leave the canonical file unchanged. Keep the
failed snapshot only while investigating it, record the reason for rejection,
and do not update the approved snapshot constants or provenance status.
