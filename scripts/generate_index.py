import os
import re
from collections import defaultdict

FOLDER = "社群貼文"
OUTPUT = "index.html"

pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})_.+?(?:_(\d+))?\.html$")

files = [f for f in os.listdir(FOLDER) if f.endswith(".html")]

groups = defaultdict(list)
for f in files:
    m = pattern.match(f)
    if not m:
        continue
    date, idx = m.groups()
    groups[date].append((int(idx) if idx else 0, f))

dates_sorted = sorted(groups.keys(), reverse=True)


def render_group(date):
    y, mth, d = date.split("-")
    posts = sorted(groups[date])
    rows = []
    if len(posts) == 1:
        _, fname = posts[0]
        rows.append(("當日貼文", fname))
    else:
        for i, (_, fname) in enumerate(posts, start=1):
            rows.append((f"第 {i} 篇", fname))
    cards = "\n".join(
        f'      <a class="card" href="{FOLDER}/{fname}" target="_blank" rel="noopener">\n'
        f'        <span class="card-title">{label}</span>\n'
        f'        <span class="card-arrow">開啟 →</span>\n'
        f'      </a>'
        for label, fname in rows
    )
    return (
        f'  <div class="date-group">\n'
        f'    <div class="date-label">{y} / {mth} / {d}</div>\n'
        f'    <div class="card-list">\n{cards}\n    </div>\n'
        f'  </div>'
    )


groups_html = "\n\n".join(render_group(d) for d in dates_sorted)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>效果升學書局・社群貼文總覽</title>
<style>
  :root {{
    --bg: #f7f6f3;
    --card-bg: #ffffff;
    --border: #e5e2db;
    --ink: #1f1d1a;
    --sub: #706a5e;
    --accent: #b8752f;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 48px 24px 80px;
    background: var(--bg);
    color: var(--ink);
    font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", -apple-system, sans-serif;
    line-height: 1.6;
  }}
  .wrap {{ max-width: 720px; margin: 0 auto; }}
  header {{ margin-bottom: 40px; }}
  h1 {{
    font-size: 26px;
    font-weight: 700;
    margin: 0 0 8px;
    letter-spacing: 0.02em;
  }}
  header p {{
    margin: 0;
    color: var(--sub);
    font-size: 14px;
  }}
  .date-group {{ margin-bottom: 32px; }}
  .date-label {{
    font-size: 13px;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.05em;
    margin-bottom: 10px;
    padding-left: 2px;
  }}
  .card-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  a.card {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    text-decoration: none;
    color: var(--ink);
    transition: border-color 0.15s ease, transform 0.15s ease;
  }}
  a.card:hover {{
    border-color: var(--accent);
    transform: translateX(2px);
  }}
  .card-title {{
    font-size: 15px;
    font-weight: 500;
  }}
  .card-arrow {{
    color: var(--sub);
    font-size: 14px;
  }}
  footer {{
    margin-top: 48px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    font-size: 12px;
    color: var(--sub);
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>效果升學書局・社群貼文總覽</h1>
    <p>依日期排序，點擊直接開啟排版好的貼文成品</p>
  </header>

{groups_html}

  <footer>
    此頁面由 GitHub Actions 自動產生，每次新增貼文會自動更新。
  </footer>
</div>
</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(TEMPLATE.format(groups_html=groups_html))
