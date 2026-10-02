# Data source notes

- NYC Open Data dataset `erm2-nwe9`: public service request data, suitable for an operations-domain API example. API fields and available historical coverage can change; request only needed columns and check dataset terms.
- FRED series DGS10: daily Treasury constant maturity rate, suitable as an illustrative risk/economic indicator. API v1 requires a user API key; live mode falls back to the bundled synthetic fixture if `FRED_API_KEY` is unset.
- SEC EDGAR Company Facts: official XBRL facts JSON for a public filer; a descriptive `User-Agent` is required. Live mode uses Apple CIK 0000320193. SEC rate limits and fair-access policy apply; check the current SEC documentation.
- `accounts.csv`, and offline NYC/FRED/SEC files are small synthetic fixtures authored for deterministic testing. They are not official records.

Links: [NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9), [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED API observations](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), [SEC API documentation](https://www.sec.gov/edgar/sec-api-documentation).
