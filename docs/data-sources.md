# MatchCast Data Sources

## Selected Initial Dataset

MatchCast uses
[`martj42/international_results`](https://github.com/martj42/international_results)
as its initial historical international-match dataset.

### Snapshot Provenance

| Field | Value |
| --- | --- |
| Source file | `results.csv` |
| Repository commit | [`25e30198bc6b2e51b3cfe2efaed2d9323b37174d`](https://github.com/martj42/international_results/commit/25e30198bc6b2e51b3cfe2efaed2d9323b37174d) |
| Immutable source URL | `https://raw.githubusercontent.com/martj42/international_results/25e30198bc6b2e51b3cfe2efaed2d9323b37174d/results.csv` |
| Retrieval method | HTTPS download from GitHub Raw Content |
| Retrieval date | 2026-07-04 |
| Local raw path | `data/raw/international_results.csv` |
| File size | 3,726,085 bytes |
| SHA-256 | `bcf26ebc26bd911fd8e68009c8606aa2cca09a52bde4cf739bdbddfadb014f49` |
| Data rows | 49,501 |
| Observed date range | 1872-11-30 through 2026-07-06 |
| Licence | [CC0 1.0 Universal](https://github.com/martj42/international_results/blob/master/LICENSE) |

The raw file is deliberately ignored by Git. Its checksum and immutable source
URL identify the exact snapshot used for development.

### Selection Rationale

- Its nine columns exactly match MatchCast's minimum raw schema.
- It covers a long history of men's senior international matches.
- The repository, source file, and public-domain licence are directly
  accessible without an account or API key.
- The snapshot includes completed 2026 World Cup matches and scheduled
  knockout fixtures available at retrieval time.
- Separate shootout data is available from the same upstream project for later
  knockout-result enrichment.

### Known Limitations

- Scores include extra time but exclude penalty-shootout scores.
- Scheduled fixtures appear in the same file as completed matches, with `NA`
  score values; training data must exclude rows without final scores.
- Team and country names use current names rather than names at match time.
- The dataset is limited to men's full internationals and excludes Olympic
  matches and games involving B teams, under-23 teams, or league selections.
- Upstream corrections can change historical rows, so every refresh requires a
  new commit identifier, checksum, and validation report.
- A GitHub repository is not a guaranteed live-results service; current
  tournament rows must be checked for freshness before publishing predictions.
- Venue and neutral-site fields require validation, especially for host teams
  during the 2026 tournament.

## Live Tournament Supplement

[OpenFootball World Cup](https://github.com/openfootball/worldcup) remains the
preferred fallback and cross-check source for 2026 fixtures and results. It is
also CC0-licensed, but its Football.TXT/JSON structure requires a separate
adapter and is not part of the initial raw match snapshot.

See [the source comparison](data-source-evaluation.md) for the full evaluation.
Follow [the raw data refresh procedure](data-refresh.md) for future snapshots.
