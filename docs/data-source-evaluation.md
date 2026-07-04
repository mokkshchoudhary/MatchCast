# Match Data Source Evaluation

This evaluation compares candidate sources for MatchCast's historical training
data and live 2026 World Cup updates. It was reviewed on 4 July 2026.

## Evaluation Criteria

- Coverage of senior men's international matches
- Coverage of the minimum MatchCast schema
- Freshness and suitability for 2026 tournament updates
- Clear provenance and licence
- Stable, scriptable access
- Amount of transformation required

## Candidate Comparison

| Candidate | Coverage and format | Minimum schema | Freshness | Licence | Access | Assessment |
| --- | --- | --- | --- | --- | --- | --- |
| [martj42/international_results](https://github.com/martj42/international_results) | Men's full internationals from 1872; `results.csv` plus separate shootout and goalscorer files | Exact nine required columns | Strong historical coverage, but repository documentation currently describes results only through 2024 | CC0-1.0 in the repository | Stable raw GitHub URL; no account or API key | Best historical baseline because its schema directly matches MatchCast and its provenance is clear; not sufficient alone for live 2026 updates |
| [OpenFootball World Cup](https://github.com/openfootball/worldcup) and [generated JSON](https://github.com/openfootball/worldcup.json) | World Cup tournaments and qualifiers, including a 2026 tournament file; Football.TXT upstream with generated JSON | Contains core fixture/result fields, but requires mapping and does not use the MatchCast CSV schema directly | Maintained for the current tournament and suitable for refreshing fixtures/results | CC0-1.0 | Stable GitHub files; no account or API key | Best live-tournament supplement; too narrow to train a general international model by itself |
| [Kaggle historical mirror](https://www.kaggle.com/datasets/brunokonzen/football-results-national-teams-18722025) | A 48,673-row mirror derived from the martj42 dataset, covering 1872–2025 | Exact nine required columns | Newer snapshot than the documented GitHub dataset, but not a live feed | CC0-1.0 stated on the data card | Kaggle download workflow may require an account, credentials, or CLI setup | Usable fallback snapshot, but adds an intermediary and less convenient automation without improving provenance |
| [DataBazaar 1872–2026 snapshot](https://databazaar.io/datasets/e9f0cefb-7269-4468-a779-f9cb047fc75c) | 49,215 matches through March 2026 with 20 derived columns | Includes the required concepts, but documented score types need validation and extra columns require normalization | One-time snapshot; excludes the live tournament | Licence is not clearly established on the public description | Downloadable CSV | Useful comparison data, but unclear licensing and one-time update frequency make it unsuitable as the primary source |

## Findings

1. No evaluated source combines a long international history with dependable
   live 2026 World Cup updates.
2. The martj42 dataset has the cleanest fit for model training because its
   documented fields exactly match the MatchCast raw schema.
3. OpenFootball is the strongest complement for current World Cup fixtures and
   results because it is public-domain, scriptable, and tournament-specific.
4. The Kaggle mirror is a fallback if a newer historical snapshot is needed,
   but it introduces credentials and another distribution layer.
5. DataBazaar should not be used until its licence and score data types are
   confirmed.

## Proposed Source Strategy

- Use the martj42 `results.csv` as the historical baseline candidate.
- Use OpenFootball's 2026 World Cup data as a separately versioned live
  tournament supplement.
- Preserve source-specific raw files and provenance metadata before combining
  them into a normalized processed table.
- Validate overlapping matches before merging, with explicit duplicate and
  conflict handling added during the cleaning phase.

The source-selection task must formally accept or reject this proposal before
download automation is implemented.
