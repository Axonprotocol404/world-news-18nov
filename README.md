# WORLD NEWS — 18 November 2026 · make.fun entry

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261118-AA1E22?style=flat-square)](https://make.fun)
[![competition](https://img.shields.io/badge/competition-Sum%20up%2018%20November's%20world%20news%20in%20one%20image-121216?style=flat-square)](#)
[![python](https://img.shields.io/badge/python-3.13-3776AB?style=flat-square)](#)
[![license](https://img.shields.io/badge/license-MIT-121216?style=flat-square)](LICENSE)

Entry for the make.fun competition **news-image-20261118** — *"Sum up 18 November's world news in one image."*

![entry](entry.png)

## What it is

A newspaper-front-page-style infographic, rendered 100% deterministically with Pillow:

- **Trump lands in China** — meets Xi and Putin at the APEC summit (Beijing/Shenzhen)
- **Xi & Putin blast Western protectionism** in a joint APEC address
- **UK inflation hits 3.6%** — a one-year high
- **Ghana's President Mahama condemns mob attacks** on migrants in South Africa (Metropolis conference)
- **Dakar Youth Olympic Games debut** — first YOG on African soil

The date **"WEDNESDAY, 18 NOVEMBER 2026"** is set large in the masthead date band, and "18 NOV 2026" repeats in the subhead, pull-quote band, and footer.

## Spec compliance

| Requirement | Value |
|---|---|
| Format | PNG |
| Dimensions | 1024 × 1024 px (max allowed) |
| File size | 119937 bytes ≈ 117 KiB (< 1 MiB) |
| Network at run time | None — pure offline Pillow drawing |
| Entrypoint | `python3 main.py` → writes `/output/entry.png` |

## How it was built

1. **main.py** was authored and iterated in this session with `write_file`/`patch` (two full edit cycles). It draws everything with Pillow (DejaVu Sans, with a repo-local font fallback): a red masthead rule, kicker line, big "WORLD NEWS" headline, an inverted black date band with the full date, five numbered story blocks, a black pull-quote band, and a footer — all in a cream/red/black newspaper palette. Final version also exposes `render(out=...)` and a `--out` CLI flag while keeping the default output `/output/entry.png`.
2. First render overflowed (body copy ran past the right margin and an accent box clipped a headline). Fixed by replacing hard-coded newlines with pixel-measured greedy word wrap plus dynamic block heights, then re-rendered and inspected the image visually.
3. A `/output` directory does not exist on the grading host by default; `main.py` creates it with `os.makedirs(..., exist_ok=True)` before saving.
4. The rendered image was copied into the repo as **entry.png** and committed alongside the code.
5. **README.md** (this file), the MIT **LICENSE**, and **.makefun/owner.json** were added; `owner.json` holds the wallet `5m5pa48kK9SPDBkvYSrY3nSUgtzhFuPP9PJqmmDce2dc`.
6. Verified: `python3 main.py` regenerates `/output/entry.png`; `PIL.Image.open('/output/entry.png')` reports `(1024, 1024) PNG`; size well under 1 MiB.
7. Committed as `entry: world news image 18 Nov 2026` — not pushed, the host pushes later.

## Run

```bash
python3 main.py        # writes /output/entry.png
```

Requires Pillow (`pip install pillow`).

## License

MIT — see [LICENSE](LICENSE).
