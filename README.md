# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kreutzx/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kreutzx/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image broadsheet of Saturday 21 November 2026: 59 counted, sourced stories — 16 of them drawn — with per-story certainty tags (CONFIRMED / REPORTED / DEVELOPING / FORECAST), a UTC timeline, a markets band and a date check that lists what was left out and why. The page is rendered deterministically by a Python program: stories.py holds the story database (the renderer counts it and prints the accounting on the masthead), art.py draws every illustration in code, build.py lays out the page, and main.py validates the finished image and copies it to the output directory.

## Run it

```sh
python3 build.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=24q484pk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
