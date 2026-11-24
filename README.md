[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b166-heroes-scene/rank.svg)](https://make.fun/leaderboard/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b166-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up 23 November's world news: 31 stories, 6 regions.

**The big three:** AI rout hits Asia (Kospi −3.3%, closes 4,708.54) ·
Guterres calls to regulate AI before it's too late (Bridgetown summit, 150
delegates) · US lead over China at a record low (Asia Power Index 2026:
US 78.9, China 73.6, gap 5.3).

**Also inside:** 10 more stories, a world map with 13 numbered pins, an
18-item ALSO list, and a red DATE CHECK box separating what is *not*
23 November (Democrats reach 258, Sparta II fire, El Chapo Isidro captured,
EU–Indonesia pact, Nigeria boat, ICJ Myanmar ruling) from what is still
*not yet* (Dymer search, 4 uncalled House races, COP32 venue, WHO Ebola
evacuation).

**How it is built:** `draw.py` (Pillow) renders `entry.png` (1024×1024,
≤1 MiB). `main.py` is stdlib-only: it validates the PNG header, chunk
CRCs, size and sha256, then writes the image to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Run it with
`python3 -P -s main.py`.
