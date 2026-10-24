# Find it in π

Search the first 50,000,000 digits of pi. Static site: all searching happens in the browser, nothing is sent anywhere.

- `index.html` is the whole app (no framework, no dependencies). It loads ten 5M-digit chunks in the background and searches whatever has arrived, re-running the search as more loads.
- `build.py` generates the digits (Chudnovsky, about 70 s) and assembles `dist/`
- `_headers` sets caching on Cloudflare Pages

The digits aren't committed. They're generated on every deploy and checked against known landmarks (digits 999,991–1,000,000, the Feynman point at digit 762, and a previously verified 10M tail), so a bad build fails instead of shipping wrong digits. They're split into chunks because Cloudflare Pages caps single files at 25 MiB.

## Cloudflare Pages settings

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | `pip install gmpy2 && python3 build.py` |
| Build output directory | `dist` |
| Python | `PYTHON_VERSION=3.12` (env var) |
| Custom domain | `pi.henryharris.co.uk` |

## Run locally

```
pip install gmpy2
python3 build.py
python3 -m http.server -d dist
```
