# MatchCast API

Start locally:

```powershell
Copy-Item .env.example .env
# Replace POSTGRES_PASSWORD in .env
docker compose up --build
```

OpenAPI is at `http://localhost:8000/docs`.

Endpoints:

- `GET /health`, `GET /teams`, `GET /metrics`
- `POST /predict-match`
- `POST /simulate-tournament`
- `GET /simulation/{simulation_id}`
- `GET /models/leaderboard`

Examples:

```bash
curl -X POST http://localhost:8000/predict-match -H "Content-Type: application/json" -d "{\"home_team\":\"Argentina\",\"away_team\":\"England\",\"neutral\":true}"
curl -X POST http://localhost:8000/simulate-tournament -H "Content-Type: application/json" -d "{\"teams\":[\"Argentina\",\"England\",\"France\",\"Spain\"],\"runs\":1000,\"seed\":7,\"qualifiers\":2}"
```

Errors use `{"error":{"code":"request_error","message":"..."}}`. Team names must be known and distinct. Round robin is the only supported format; teams must be unique; run counts are bounded by `MATCHCAST_MAX_SIMULATIONS`.
