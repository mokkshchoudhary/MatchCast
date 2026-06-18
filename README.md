# NationsAI

NationsAI is a backend-first machine learning project for probabilistic international football match prediction.

The goal is to build a technically serious football prediction engine that demonstrates data engineering, feature engineering, statistical modelling, machine learning, simulation, evaluation, and backend engineering.

## Project Goals

- Load and clean historical international football match data
- Build baseline Elo ratings for national teams
- Predict match outcomes using pre-match features
- Estimate scoreline probabilities with a Poisson model
- Simulate matches and small tournaments
- Evaluate models using proper probabilistic metrics
- Eventually expose predictions through a backend API

## Current Stage

Initial project setup.

The first milestone is to build a working baseline pipeline:

1. Data exploration
2. Data cleaning
3. Elo rating baseline
4. Poisson score model
5. Match simulation
6. Group-stage simulation
7. Basic tests

## Project Structure

```text
data/
  raw/
  interim/
  processed/
notebooks/
src/
  nations_ai/
    ingestion/
    features/
    models/
    simulation/
    evaluation/
    api/
tests/
reports/