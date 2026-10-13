# Fermentation Gas Mass Spectrometry

A fermentation off-gas analysis toolkit with a **browser-based dry-gas calculator**, a Python calculation engine, REST endpoints, and legacy threshold-based audit workflows.

The quantitative module calculates oxygen uptake (OUR), carbon dioxide evolution (CER), and respiratory quotient (RQ). It **does not ingest raw mass-spectrometer spectra**, perform mass-to-charge peak identification, or automatically calibrate sensors.

## Run the browser calculator

The static application lives in `site/`. It uses native JavaScript modules and does not require a Python runtime or backend.

```bash
python -m http.server 8080 --directory site
```

Open **http://localhost:8080/**. Enter dry inlet gas flow in mmol/min, gas concentrations in percent, select **Calculate**, and optionally export the result as CSV. The results and download are calculated locally in your browser. No sample data are sent to a server. Modern browsers with ES module support are required.

A GitHub Pages publishing workflow is configured; availability of a public live application depends on repository Pages settings and successful deployment.

## Calculation model and assumptions

Input gas streams must be dry and on a consistent pressure/temperature molar basis. The inert gas fraction is assumed conserved between inlet and outlet.

```text
Fout = Fin * (1 - yO2,in - yCO2,in) / (1 - yO2,out - yCO2,out)
OUR  = Fin*yO2,in - Fout*yO2,out
CER  = Fout*yCO2,out - Fin*yCO2,in
RQ   = CER / OUR            (only when OUR > 0)
```

Here `F` is the gas molar flow in mmol/min and `y` is the **dimensionless mole fraction** (0–1). Calculated OUR/CER are **process-wide mmol/min**, not volumetric rates; normalize separately using a measured broth volume if needed.

The functions reject non-finite values, invalid composition fractions, zero/negative inlet flow, and streams with no inert fraction. Zero or negative net oxygen uptake yields an undefined RQ. Wet-gas corrections, nonconserved inert gases, leaks, poorly mixed streams, and sensor inaccuracies are **not** modeled.

## Python and command line

Python 3.9+ is declared in the package metadata; CI runs Python 3.10–3.12.

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m build --wheel
```

Run the domain-specific CLI:

```bash
fermentation-gas-mass-spectrometry calculate \
  --flow 100 --inlet-o2 0.21 --inlet-co2 0 \
  --outlet-o2 0.16 --outlet-co2 0.04
```

These CLI/API inputs use fractions (0–1), **not percent values**. The browser form accepts percentages and converts them internally.

Existing legacy commands remain available:

```bash
python cli.py audit --task-id DEMO-1 --target VESSEL-1 --primary 12 --secondary 4
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
fermentation-gas-mass-spectrometry audit --task-id DEMO-1
```

The legacy multi-worker audit classifiers evaluate **fixed, illustrative thresholds**, not validated clinical or bioprocess reference limits. They should not be used as safety interlocks or evidence of compliance with CAP, CLSI, ISO, or other standards.

## Local REST API

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000/** for the backend-dependent legacy audit console, or **http://127.0.0.1:8000/docs** for generated REST documentation. The new calculation endpoint is `POST /api/offgas/calculate`:

```bash
curl -s http://127.0.0.1:8000/api/offgas/calculate \
  -H 'Content-Type: application/json' \
  -d '{"inlet_flow_mmol_min":100,"inlet_o2":0.21,"inlet_co2":0,"outlet_o2":0.16,"outlet_co2":0.04}'
```

The legacy API is also available via `python -m offgas_analyzer.cli serve`. Docker deployment is supported by the provided `Dockerfile` and `docker-compose.yml`.

## Data handling and security

The standalone calculator runs in the browser without telemetry or network API requests. The local Python server processes submitted audit values and retains its audit trail **in memory only**. HMAC verification is local to that in-memory chain; it is **not** a durable, externally anchored audit record. For a stable HMAC key during server use, set `AUDIT_SECRET_KEY` to a high-entropy secret in the server environment; do not commit the key.

The legacy regular-expression identifier guard is best-effort and cannot guarantee de-identification or regulatory compliance. Do not submit patient-identifiable or otherwise sensitive production data without independent security assessment and deployment controls.

## Project layout

- `site/` — browser-only OUR/CER/RQ calculator (no Python/WASM required)
- `offgas_analyzer/calculations.py` — validated gas balance equations
- `offgas_analyzer/` — domain-specific audit API and CLI
- `agents/`, `cli.py`, `web/index.html` — preserved legacy workflow and local console
- `tests/` — unit and API regression tests
- `.github/workflows/` — CI and Pages publishing automation

## License

MIT. See [LICENSE](LICENSE).
