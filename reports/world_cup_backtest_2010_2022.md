# World Cup Pre-Tournament Backtest (2010–2022)

All 64 predictions for each tournament were generated from matches strictly before its opening match, then frozen before comparison with actual results. Total: 256 matches.

## Log loss by tournament

```csv
world_cup,elo,frequency,logistic,poisson
2010,0.9837,1.1113,0.972,0.9911
2014,0.978,1.0596,0.9692,0.9779
2018,0.9709,1.0923,0.967,0.9848
2022,1.0311,1.0729,1.0372,1.0168
```

## Aggregate ranking

```csv
model,mean_log_loss,mean_brier,accuracy
logistic,0.9864,0.5818,0.5547
elo,0.9909,0.5884,0.5352
poisson,0.9927,0.5897,0.5508
frequency,1.084,0.6588,0.4141
```

Lower log loss and Brier score are better. Accuracy is secondary because it ignores probability quality. The per-match audit file is `reports/world_cup_predictions_2010_2022.csv`. This is a historical backtest, not evidence that future performance is guaranteed.
