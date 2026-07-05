# MatchCast Model Card

## Intended use

Estimate probabilities for senior international football outcomes and support educational tournament simulations. It is not suitable for betting, selection, safety-critical, or financial decisions.

## Training and evaluation

Data is the documented Mart Jürisoo international-results dataset processed chronologically. The production candidate is regularized logistic regression using leakage-safe Elo/form/context features. On identical 2014/2018/2022 World Cup folds (192 matches), its pooled log loss was 0.982 versus Elo 0.993 and Poisson 0.998. Poisson remains the scoreline model.

## Limitations

The evaluation sample is small. Data may contain historical coverage and naming bias. The system lacks player availability, line-ups, injuries, travel, and live match information. Probabilities are estimates, not guarantees, and performance may drift.

## Ethics and maintenance

Outputs must identify model/data versions and limitations. Monitor calibration and data drift before releases. Do not infer player characteristics or use the model to target individuals.
