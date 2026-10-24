# Find it in π

Search the first 10,000,000 digits of pi. Static site: all searching happens in the browser, nothing is sent anywhere.

- `index.html` is the whole app (no framework, no dependencies)
- `build.py` generates the digits (Chudnovsky, ~10 s) and assembles `dist/`
- `_headers` sets caching on Cloudflare Pages

The 10 MB digits file isn't committed. It's generated on every deploy and checked against known landmarks (digits 999,991–1,000,000, the Feynman point at digit 762), so a bad build fails instead of shipping wrong digits.

## Cloudflare Pages settings

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | `pip install gmpy2 && python3 build.py` |
| Build output directory | `dist` |
| Custom domain | `pi.henryharris.co.uk` |

## Run locally

```
pip install gmpy2
python3 build.py
python3 -m http.server -d dist
```
