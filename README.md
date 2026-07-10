# MatchCast

Probabilistic prediction of international football matches, built and audited around the
2026 FIFA World Cup. Independent portfolio project — not affiliated with FIFA or any
tournament organizer, and not suitable for betting.

## What We Built

An end-to-end, leakage-safe prediction pipeline:

- **Data**: the Mart Jürisoo international-results dataset (49k+ matches since 1872),
  cleaned and processed chronologically.
- **Ratings**: an Elo rating system computed match-by-match, so every prediction uses
  only information available before kickoff.
- **Features**: Elo differences, rolling form (goals, points, form vs expectation over
  3/5/10 matches), rest days, activity, tournament type, and World Cup stage flags.
- **Models**: Elo baseline, Poisson scoreline model, and a sweep of ML classifiers
  (regularized logistic regression, random forest, extra trees, gradient boosting,
  XGBoost, MLPs, and ensembles).
- **Evaluation**: strictly chronological, pre-tournament frozen backtests scored on
  log loss, Brier score, and accuracy.
- **Serving**: seeded tournament simulation, a typed API/persistence prototype, and
  container/CI/MLOps packaging. See `docs/` for architecture, API, model card, and
  reproduction guides.

**Selected model: recency- and importance-weighted L2 logistic regression** for outcome
probabilities (home/draw/away), with Poisson retained for scorelines.

## How the Model Was Validated

Every audit freezes the model before the tournament starts: it trains only on matches
played before kickoff of the tournament being tested, then predictions are compared
with actual results.

1. **World Cup backtest** (`notebooks/09`, `12`): all 256 matches of the 2010–2022
   World Cups. Weighted logistic won with 148/256 (57.8%) and the best log loss.
2. **Wider major-tournament backtest** (`notebooks/16`): the World Cup sample alone is
   too small — a few matches of accuracy difference between models is pure noise
   (±3.1% standard error). So the frozen protocol was extended to **27 tournament
   editions since 2010** (4 World Cups, 4 Euros, 6 Copa Américas, 9 AFCONs, 4 Asian
   Cups) — **1,141 test matches**, shrinking the error margin to ±1.5%.

Results on the full 1,141-match set:

| Model | Log loss | Brier | Accuracy | Correct |
| --- | --- | --- | --- | --- |
| **Weighted logistic (L2) — selected** | **0.967** | **0.576** | 55.0% | 628 |
| Ensemble (logistic + boosting + MLP) | 0.970 | 0.579 | 55.2% | 630 |
| Weighted logistic (L1) | 0.969 | 0.577 | 54.1% | 617 |
| XGBoost (regularized) | 0.972 | 0.581 | 53.6% | 612 |
| Hist gradient boosting | 0.979 | 0.585 | 53.5% | 610 |
| Elo baseline | 0.982 | 0.586 | 52.8% | 602 |
| MLP (deep) | 0.996 | 0.593 | 53.4% | 609 |
| Random forest | 0.996 | 0.598 | 48.7% | 556 |
| Extra trees | 1.024 | 0.617 | 46.3% | 528 |

## Findings

1. **The weighted logistic model is the confirmed winner.** Best log loss and Brier
   score; its accuracy is statistically tied with the best ensemble (628 vs 630 correct,
   a 0.18% gap against a ~2.9% noise threshold). The extra complexity of ensembles and
   boosting buys nothing.
2. **Fancier algorithms are a dead end on these features.** Random forests, extra trees,
   and neural networks lose by 2–9 percentage points on 1,141 matches — a real deficit,
   not bad luck. Earlier "XGBoost is one match better" results on the 256-match sample
   were noise.
3. **The feature layer beats raw Elo everywhere**: roughly +2.3% accuracy and −0.015
   log loss across all five tournament families, not just World Cups.
4. **Draws are the main weakness.** The argmax pick almost never selects a draw even
   though ~25% of matches end drawn. In the live 2026 audit below, 24 of the 37 misses
   are draws the model called for one side.
5. **AFCON is the hardest tournament.** Every model scores below 50% accuracy there,
   versus ~58% at World Cups and ~63% at Asian Cups — the clearest target for
   region-specific improvement (likely Elo coverage of African teams).
6. **Experiments that did not help** (kept in the repo as negative results):
   upset-risk features (`notebooks/14`, −2.3%), Wikipedia squad/manager data
   (`notebooks/15`, −6.8%), and rich-feature model sweeps (`notebooks/10`, `12`).
7. **What could still move accuracy** (not yet implemented): a tuned draw decision
   rule, historical betting odds, and squad market values — the strongest known
   predictors the dataset currently lacks.

## 2026 World Cup: Live Audit

Predictions for all 96 matches played through 2026-07-08. For each match date, the
selected weighted logistic model is trained only on matches before that date, then its
pick is compared with the actual result.

**Overall record: 59/96 correct (61.5%)** — above the 55% historical backtest level.

| Stage | Record | Accuracy |
| --- | --- | --- |
| Group stage | 43/72 | 59.7% |
| Round of 32 | 12/16 | 75.0% |
| Round of 16 | 4/8 | 50.0% |

Of the 37 misses, 24 were draws — the model always picked a winner.

<details>
<summary><strong>Group stage — 43/72 correct</strong> (click to expand)</summary>

| Date | Match | Score | Model pick | Actual | Result |
| --- | --- | --- | --- | --- | :---: |
| 2026-06-11 | Mexico vs South Africa | 2-0 | Mexico | Mexico | ✅ |
| 2026-06-11 | South Korea vs Czech Republic | 2-1 | South Korea | South Korea | ✅ |
| 2026-06-12 | Canada vs Bosnia and Herzegovina | 1-1 | Canada | Draw | ❌ |
| 2026-06-12 | United States vs Paraguay | 4-1 | Paraguay | United States | ❌ |
| 2026-06-13 | Qatar vs Switzerland | 1-1 | Switzerland | Draw | ❌ |
| 2026-06-13 | Brazil vs Morocco | 1-1 | Brazil | Draw | ❌ |
| 2026-06-13 | Haiti vs Scotland | 0-1 | Scotland | Scotland | ✅ |
| 2026-06-13 | Australia vs Turkey | 2-0 | Turkey | Australia | ❌ |
| 2026-06-14 | Germany vs Curaçao | 7-1 | Germany | Germany | ✅ |
| 2026-06-14 | Ivory Coast vs Ecuador | 1-0 | Ecuador | Ivory Coast | ❌ |
| 2026-06-14 | Netherlands vs Japan | 2-2 | Japan | Draw | ❌ |
| 2026-06-14 | Sweden vs Tunisia | 5-1 | Tunisia | Sweden | ❌ |
| 2026-06-15 | Belgium vs Egypt | 1-1 | Belgium | Draw | ❌ |
| 2026-06-15 | Iran vs New Zealand | 2-2 | Iran | Draw | ❌ |
| 2026-06-15 | Spain vs Cape Verde | 0-0 | Spain | Draw | ❌ |
| 2026-06-15 | Saudi Arabia vs Uruguay | 1-1 | Uruguay | Draw | ❌ |
| 2026-06-16 | France vs Senegal | 3-1 | France | France | ✅ |
| 2026-06-16 | Iraq vs Norway | 1-4 | Norway | Norway | ✅ |
| 2026-06-16 | Argentina vs Algeria | 3-0 | Argentina | Argentina | ✅ |
| 2026-06-16 | Austria vs Jordan | 3-1 | Austria | Austria | ✅ |
| 2026-06-17 | Portugal vs DR Congo | 1-1 | Portugal | Draw | ❌ |
| 2026-06-17 | Uzbekistan vs Colombia | 1-3 | Colombia | Colombia | ✅ |
| 2026-06-17 | England vs Croatia | 4-2 | England | England | ✅ |
| 2026-06-17 | Ghana vs Panama | 1-0 | Panama | Ghana | ❌ |
| 2026-06-18 | Czech Republic vs South Africa | 1-1 | Czech Republic | Draw | ❌ |
| 2026-06-18 | Mexico vs South Korea | 1-0 | Mexico | Mexico | ✅ |
| 2026-06-18 | Switzerland vs Bosnia and Herzegovina | 4-1 | Switzerland | Switzerland | ✅ |
| 2026-06-18 | Canada vs Qatar | 6-0 | Canada | Canada | ✅ |
| 2026-06-19 | Scotland vs Morocco | 0-1 | Morocco | Morocco | ✅ |
| 2026-06-19 | Brazil vs Haiti | 3-0 | Brazil | Brazil | ✅ |
| 2026-06-19 | United States vs Australia | 2-0 | United States | United States | ✅ |
| 2026-06-19 | Turkey vs Paraguay | 0-1 | Turkey | Paraguay | ❌ |
| 2026-06-20 | Germany vs Ivory Coast | 2-1 | Germany | Germany | ✅ |
| 2026-06-20 | Ecuador vs Curaçao | 0-0 | Ecuador | Draw | ❌ |
| 2026-06-20 | Netherlands vs Sweden | 5-1 | Netherlands | Netherlands | ✅ |
| 2026-06-20 | Tunisia vs Japan | 0-4 | Japan | Japan | ✅ |
| 2026-06-21 | Belgium vs Iran | 0-0 | Belgium | Draw | ❌ |
| 2026-06-21 | New Zealand vs Egypt | 1-3 | Egypt | Egypt | ✅ |
| 2026-06-21 | Spain vs Saudi Arabia | 4-0 | Spain | Spain | ✅ |
| 2026-06-21 | Uruguay vs Cape Verde | 2-2 | Uruguay | Draw | ❌ |
| 2026-06-22 | France vs Iraq | 3-0 | France | France | ✅ |
| 2026-06-22 | Norway vs Senegal | 3-2 | Norway | Norway | ✅ |
| 2026-06-22 | Argentina vs Austria | 2-0 | Argentina | Argentina | ✅ |
| 2026-06-22 | Jordan vs Algeria | 1-2 | Algeria | Algeria | ✅ |
| 2026-06-23 | Portugal vs Uzbekistan | 5-0 | Portugal | Portugal | ✅ |
| 2026-06-23 | Colombia vs DR Congo | 1-0 | Colombia | Colombia | ✅ |
| 2026-06-23 | England vs Ghana | 0-0 | England | Draw | ❌ |
| 2026-06-23 | Panama vs Croatia | 0-1 | Croatia | Croatia | ✅ |
| 2026-06-24 | Mexico vs Czech Republic | 3-0 | Mexico | Mexico | ✅ |
| 2026-06-24 | South Africa vs South Korea | 1-0 | South Korea | South Africa | ❌ |
| 2026-06-24 | Canada vs Switzerland | 1-2 | Canada | Switzerland | ❌ |
| 2026-06-24 | Bosnia and Herzegovina vs Qatar | 3-1 | Bosnia and Herzegovina | Bosnia and Herzegovina | ✅ |
| 2026-06-24 | Scotland vs Brazil | 0-3 | Brazil | Brazil | ✅ |
| 2026-06-24 | Morocco vs Haiti | 4-2 | Morocco | Morocco | ✅ |
| 2026-06-25 | United States vs Turkey | 2-3 | United States | Turkey | ❌ |
| 2026-06-25 | Paraguay vs Australia | 0-0 | Paraguay | Draw | ❌ |
| 2026-06-25 | Curaçao vs Ivory Coast | 0-2 | Ivory Coast | Ivory Coast | ✅ |
| 2026-06-25 | Ecuador vs Germany | 2-1 | Ecuador | Ecuador | ✅ |
| 2026-06-25 | Japan vs Sweden | 1-1 | Japan | Draw | ❌ |
| 2026-06-25 | Tunisia vs Netherlands | 1-3 | Netherlands | Netherlands | ✅ |
| 2026-06-26 | Egypt vs Iran | 1-1 | Egypt | Draw | ❌ |
| 2026-06-26 | New Zealand vs Belgium | 1-5 | Belgium | Belgium | ✅ |
| 2026-06-26 | Cape Verde vs Saudi Arabia | 0-0 | Cape Verde | Draw | ❌ |
| 2026-06-26 | Uruguay vs Spain | 0-1 | Spain | Spain | ✅ |
| 2026-06-26 | Norway vs France | 1-4 | France | France | ✅ |
| 2026-06-26 | Senegal vs Iraq | 5-0 | Senegal | Senegal | ✅ |
| 2026-06-27 | Algeria vs Austria | 3-3 | Algeria | Draw | ❌ |
| 2026-06-27 | Jordan vs Argentina | 1-3 | Argentina | Argentina | ✅ |
| 2026-06-27 | Colombia vs Portugal | 0-0 | Colombia | Draw | ❌ |
| 2026-06-27 | DR Congo vs Uzbekistan | 3-1 | DR Congo | DR Congo | ✅ |
| 2026-06-27 | Panama vs England | 0-2 | England | England | ✅ |
| 2026-06-27 | Croatia vs Ghana | 2-1 | Croatia | Croatia | ✅ |

</details>

<details>
<summary><strong>Round of 32 — 12/16 correct</strong> (click to expand)</summary>

| Date | Match | Score | Model pick | Actual | Result |
| --- | --- | --- | --- | --- | :---: |
| 2026-06-28 | South Africa vs Canada | 0-1 | Canada | Canada | ✅ |
| 2026-06-29 | Brazil vs Japan | 2-1 | Brazil | Brazil | ✅ |
| 2026-06-29 | Germany vs Paraguay | 1-1 | Germany | Draw | ❌ |
| 2026-06-29 | Netherlands vs Morocco | 1-1 | Netherlands | Draw | ❌ |
| 2026-06-30 | Ivory Coast vs Norway | 1-2 | Ivory Coast | Norway | ❌ |
| 2026-06-30 | France vs Sweden | 3-0 | France | France | ✅ |
| 2026-06-30 | Mexico vs Ecuador | 2-0 | Mexico | Mexico | ✅ |
| 2026-07-01 | England vs DR Congo | 2-1 | England | England | ✅ |
| 2026-07-01 | Belgium vs Senegal | 3-2 | Belgium | Belgium | ✅ |
| 2026-07-01 | United States vs Bosnia and Herzegovina | 2-0 | United States | United States | ✅ |
| 2026-07-02 | Spain vs Austria | 3-0 | Spain | Spain | ✅ |
| 2026-07-02 | Portugal vs Croatia | 2-1 | Portugal | Portugal | ✅ |
| 2026-07-02 | Switzerland vs Algeria | 2-0 | Switzerland | Switzerland | ✅ |
| 2026-07-03 | Australia vs Egypt | 1-1 | Australia | Draw | ❌ |
| 2026-07-03 | Argentina vs Cape Verde | 3-2 | Argentina | Argentina | ✅ |
| 2026-07-03 | Colombia vs Ghana | 1-0 | Colombia | Colombia | ✅ |

</details>

<details open>
<summary><strong>Round of 16 — 4/8 correct</strong></summary>

| Date | Match | Score | Model pick | Actual | Result |
| --- | --- | --- | --- | --- | :---: |
| 2026-07-04 | Canada vs Morocco | 0-3 | Canada | Morocco | ❌ |
| 2026-07-04 | France vs Paraguay | 1-0 | France | France | ✅ |
| 2026-07-05 | Brazil vs Norway | 1-2 | Brazil | Norway | ❌ |
| 2026-07-05 | Mexico vs England | 2-3 | Mexico | England | ❌ |
| 2026-07-06 | Spain vs Portugal | 1-0 | Spain | Spain | ✅ |
| 2026-07-06 | United States vs Belgium | 1-4 | Belgium | Belgium | ✅ |
| 2026-07-07 | Argentina vs Egypt | 3-2 | Argentina | Argentina | ✅ |
| 2026-07-07 | Switzerland vs Colombia | 0-0 | Colombia | Draw; Switzerland advanced on penalties | ❌ |

</details>

### Quarter-finals — predictions locked, results pending

Predictions from `notebooks/17`: the selected model trained on all matches through
2026-07-07 (every round-of-16 result included, nothing after), frozen before the
first quarter-final kicked off.

| Date | Match | Venue | Model pick | P(win) | P(draw) | P(loss) | Actual | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | :---: |
| 2026-07-09 | France vs Morocco | Boston | France | 55% | 23% | 22% | — | ⏳ |
| 2026-07-10 | Spain vs Belgium | Los Angeles | Spain | 54% | 25% | 21% | — | ⏳ |
| 2026-07-11 | Norway vs England | Miami | England | 48% | 23% | 29% | — | ⏳ |
| 2026-07-11 | Argentina vs Switzerland | Kansas City | Argentina | 67% | 22% | 11% | — | ⏳ |

P(win)/P(loss) are from the picked team's perspective. Argentina over Switzerland is
the model's most confident knockout pick of the tournament so far (67%); Norway vs
England is the closest call (England 48% vs Norway 29%).

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

Notebooks `01`–`17` walk through the project in order: data preparation, Elo and
Poisson baselines, simulation, evaluation, ML model sweeps, the frozen backtests, the
2026 audits, and the live quarter-final predictions. Full guides live in `docs/reproduction.md`, `docs/api.md`,
`docs/model-card.md`, and `docs/architecture.md`.

## Licence

See [LICENSE](LICENSE).
