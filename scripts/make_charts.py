#!/usr/bin/env python3
"""生成 README 里的三张图表，并且能反过来核对它们有没有过期。

    python3 scripts/make_charts.py            # 重新生成 assets/chart-*.svg
    python3 scripts/make_charts.py --check    # 只核对，不写文件（CI 用）

为什么自己画，而不是用现成的 stats 卡片：
之前 README 底部挂着两张第三方卡片，它们是活的，但报的数字是
「Stars 3 / Commits 71 / PRs 5」和「Top Languages by Repo: Rust」。
两个都对不上：

  - 那两张卡只数**当年**、**公开**仓库的贡献。闭源主仓的提交一概不算，
    于是一个每天在写代码的人被显示成一个几乎没动过的账号。
  - 语言卡数的是「有多少个仓库以某语言为主」，而且把 fork 算了进去。
    codex 那个 fork 里有 50 MB 的 Rust，一个字不是我写的，
    却让整个账号看起来 91.3% 是 Rust。

自己画就没有这两个问题：数据怎么来的写在下面，而且 --check 会
每周去重新量一次。图里不写中文 —— SVG 当图片加载时用的是访客机器上的
字体，没装 CJK 字体就是一片豆腐块。中文说明放在 README 正文里。
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

OWNER = "wenxuanzhang1209-cyber"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

#: 语言百分比允许的漂移。每写一个新功能这些数字都会动一点，
#: 要求精确相等只会让 CI 每周都红一次而没有任何信息量。
#: 超过 2.5 个百分点才算「图该重画了」。
TOLERANCE_POINTS = 2.5

#: 语言配色沿用 GitHub linguist 自己的，读者对这几个颜色是有肌肉记忆的。
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "CSS": "#663399", "HTML": "#e34c26", "Shell": "#89e051",
    "Dockerfile": "#384d54", "Batchfile": "#C1F12E",
}
OTHER_COLOR = "#8b949e"

THEMES = {
    "light": dict(bg="#ffffff", line="#d1d9e0", ink="#1f2328",
                  muted="#59636e", grid="#eaeef2"),
    "dark":  dict(bg="#0d1117", line="#3d444d", ink="#f0f6fc",
                  muted="#9198a1", grid="#21262d"),
}
FONT = ("ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',"
        "Roboto,Helvetica,Arial,sans-serif")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def _api(path: str):
    request = urllib.request.Request(
        f"https://api.github.com/{path.lstrip('/')}",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "jkinco-profile-charts"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def measure_languages() -> tuple[list[tuple[str, int]], int, int]:
    """按字节统计**自己写的**代码的语言构成。

    两个刻意的选择：
      - `type=owner` 之后还要再滤一次 `fork` —— owner 只是说仓库归我，
        fork 来的仓库同样归我，里面的代码却不是我写的。
      - 数的是字节，不是仓库个数。一个 90% 的 Python 仓库和一个
        3 KB 的脚本仓库，按仓库数是 1:1，按字节才是真实体量。
    """
    repos = []
    page = 1
    while True:
        batch = _api(f"users/{OWNER}/repos?per_page=100&type=owner&page={page}")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r.get("fork")]
    totals: dict[str, int] = {}
    for repo in own:
        for lang, size in _api(f"repos/{OWNER}/{repo['name']}/languages").items():
            totals[lang] = totals.get(lang, 0) + size
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    return ranked, sum(totals.values()), len(own)


def top_with_other(ranked: list[tuple[str, int]], keep: int = 4):
    """前 N 个单列，剩下的并成 other —— 一条只有 3 px 宽的色块讲不出任何事。"""
    head = ranked[:keep]
    rest = sum(v for _, v in ranked[keep:])
    if rest:
        head = head + [("other", rest)]
    return head


# ── 画图 ────────────────────────────────────────────────────────
def _head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">'
            f'<rect width="{w}" height="{h}" rx="6" fill="{t["bg"]}" stroke="{t["line"]}"/>')


def _title(x, y, text, t, sub):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="13.5" font-weight="600" '
            f'fill="{t["ink"]}">{text}</text>'
            f'<text x="{x}" y="{y+18}" font-family="{FONT}" font-size="11" '
            f'fill="{t["muted"]}">{sub}</text>')


def _foot(x, y, text, t):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="9.5" '
            f'fill="{t["muted"]}">{text}</text>')


def chart_languages(t, slices, total_kb, repo_count):
    W, H = 840, 186
    s = [_head(W, H, t)]
    s.append(_title(24, 32, "Where the code actually is", t,
                    f"{repo_count} own public repos · {total_kb:,} KB · forks excluded"))
    grand = sum(v for _, v in slices)
    x, y, bw, bh = 24, 72, W - 48, 20
    cursor = float(x)
    for name, val in slices:
        w = bw * val / grand
        color = LANG_COLORS.get(name, OTHER_COLOR)
        s.append(f'<rect x="{cursor:.1f}" y="{y}" width="{max(w-2,2):.1f}" '
                 f'height="{bh}" rx="2" fill="{color}"/>')
        cursor += w
    lx, ly = x, y + bh + 28
    for name, val in slices:
        color = LANG_COLORS.get(name, OTHER_COLOR)
        s.append(f'<circle cx="{lx+4}" cy="{ly-4}" r="4" fill="{color}"/>')
        s.append(f'<text x="{lx+14}" y="{ly}" font-family="{FONT}" font-size="11.5" '
                 f'fill="{t["ink"]}">{name}</text>')
        s.append(f'<text x="{lx+14}" y="{ly+16}" font-family="{MONO}" font-size="11" '
                 f'fill="{t["muted"]}">{val/grand*100:.1f}%</text>')
        lx += 158
    s.append(_foot(24, H - 18, "Backend and frontend within a point of each other", t))
    s.append("</svg>")
    return "".join(s)


#: 测试数由 verify_profile_numbers.py 独立核对（它去读源仓库 CI 的真实日志）。
TESTS = [("JKinco Listen", 961, "counted from its CI log, not its badge"),
         ("JKinco Slides", 269, "summed across 18 packages")]


def chart_tests(t):
    W, H = 840, 200
    s = [_head(W, H, t)]
    s.append(_title(24, 32, "Tested, not asserted", t,
                    "Automated tests in the two flagship projects"))
    top = max(v for _, v, _ in TESTS)
    y = 76
    for name, val, note in TESTS:
        s.append(f'<text x="24" y="{y+13}" font-family="{FONT}" font-size="12" '
                 f'fill="{t["ink"]}">{name}</text>')
        bx, bw = 190, 510
        s.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="18" rx="3" fill="{t["grid"]}"/>')
        s.append(f'<rect x="{bx}" y="{y}" width="{bw*val/top:.1f}" height="18" rx="3" fill="#3fb950"/>')
        s.append(f'<text x="{bx+bw+16}" y="{y+13}" font-family="{MONO}" font-size="13" '
                 f'font-weight="500" fill="{t["ink"]}">{val}</text>')
        s.append(f'<text x="{bx}" y="{y+34}" font-family="{FONT}" font-size="10.5" '
                 f'fill="{t["muted"]}">{note}</text>')
        y += 54
    s.append(_foot(24, H - 18,
                   "The interesting ones cover paths that only run after something else failed", t))
    s.append("</svg>")
    return "".join(s)


def chart_benchmark(t):
    W, H = 840, 220
    s = [_head(W, H, t)]
    s.append(_title(24, 32, "Domain accuracy, measured", t,
                    "36 construction / HR / commercial terms a general model tends to mishear"))
    y = 78
    for name, val, color in (("Local ASR alone", 31, OTHER_COLOR),
                             ("+ domain correction", 36, "#3fb950")):
        s.append(f'<text x="24" y="{y+13}" font-family="{FONT}" font-size="12" '
                 f'fill="{t["ink"]}">{name}</text>')
        bx, bw = 200, 460
        s.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="18" rx="3" fill="{t["grid"]}"/>')
        s.append(f'<rect x="{bx}" y="{y}" width="{bw*val/36:.1f}" height="18" rx="3" fill="{color}"/>')
        s.append(f'<text x="{bx+bw+16}" y="{y+13}" font-family="{MONO}" font-size="13" '
                 f'font-weight="500" fill="{t["ink"]}">{val} / 36</text>')
        y += 44
    s.append(f'<text x="24" y="{y+18}" font-family="{FONT}" font-size="10.5" '
             f'fill="{t["muted"]}">Synthetic clips are cleaner than a real meeting room — '
             f'read 36/36 as an upper bound, not a promise.</text>')
    s.append(_foot(24, H - 18, "python3 scripts/benchmark_domain_accuracy.py", t))
    s.append("</svg>")
    return "".join(s)


#: 整条流水线。这张图不含任何会过期的数字 —— 它讲的是架构，不是指标。
STAGES = ["Recording", "Transcript", "Scene", "Minutes", "DOCX / PDF"]


def chart_pipeline(t):
    """本地优先这件事，一句话说不清楚，一张图可以。

    刻意画出「边界」而不是只画流程：读者真正要看到的不是有五个步骤，
    而是这五个步骤**全部在同一个框里**，框外那条线是断的。
    """
    W, H = 840, 210
    s = [_head(W, H, t)]
    s.append(_title(24, 32, "Nothing leaves the machine", t,
                    "Audio, transcript, and model all stay on your own hardware"))
    bx0, bx1, by0, by1 = 24, 700, 66, 152
    s.append(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="8" '
             f'fill="none" stroke="#3fb950" stroke-width="1.2" stroke-dasharray="5 4"/>')
    s.append(f'<text x="{bx0+16}" y="{by0+20}" font-family="{FONT}" font-size="9.5" '
             f'font-weight="600" letter-spacing="1.1" fill="#3fb950">YOUR MACHINE</text>')

    inner0, inner1 = bx0 + 16, bx1 - 16
    gap, n = 22, len(STAGES)
    bw = (inner1 - inner0 - gap * (n - 1)) / n
    y, bh = 98, 36
    x = float(inner0)
    for i, stage in enumerate(STAGES):
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="5" '
                 f'fill="{t["grid"]}" stroke="{t["line"]}" stroke-width="0.8"/>')
        s.append(f'<text x="{x+bw/2:.1f}" y="{y+22}" text-anchor="middle" '
                 f'font-family="{FONT}" font-size="10.5" fill="{t["ink"]}">{stage}</text>')
        if i < n - 1:
            s.append(f'<text x="{x+bw+gap/2:.1f}" y="{y+22}" text-anchor="middle" '
                     f'font-family="{FONT}" font-size="12" fill="{t["muted"]}">&#8594;</text>')
        x += bw + gap

    # 框外：那条本该通向云端的线，是断的。
    s.append(f'<line x1="{bx1+4}" y1="116" x2="{bx1+30}" y2="116" stroke="{t["muted"]}" '
             f'stroke-width="1" stroke-dasharray="3 3"/>')
    cx0, cy0, cw, ch = bx1 + 36, 98, 80, 36
    s.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="5" fill="none" '
             f'stroke="{t["muted"]}" stroke-width="0.8" stroke-dasharray="4 3"/>')
    s.append(f'<text x="{cx0+cw/2}" y="{cy0+22}" text-anchor="middle" font-family="{FONT}" '
             f'font-size="10.5" fill="{t["muted"]}">cloud API</text>')
    s.append(f'<line x1="{cx0+8}" y1="{cy0+ch-6}" x2="{cx0+cw-8}" y2="{cy0+6}" '
             f'stroke="#f85149" stroke-width="1.6" stroke-linecap="round"/>')

    s.append(f'<text x="24" y="176" font-family="{FONT}" font-size="10.5" fill="{t["muted"]}">'
             f'Not a promise in the README — CI fails the build if a cloud-model trace, '
             f'API key, or production hostname enters the repo.</text>')
    s.append(_foot(24, H - 16, "no API key  ·  no upload  ·  works with the WiFi off", t))
    s.append("</svg>")
    return "".join(s)


def build(slices, total_kb, repo_count) -> dict[str, str]:
    out = {}
    for theme, tokens in THEMES.items():
        out[f"chart-languages-{theme}.svg"] = chart_languages(
            tokens, slices, total_kb, repo_count)
        out[f"chart-tests-{theme}.svg"] = chart_tests(tokens)
        out[f"chart-benchmark-{theme}.svg"] = chart_benchmark(tokens)
        out[f"chart-pipeline-{theme}.svg"] = chart_pipeline(tokens)
    return out


def main() -> int:
    check = "--check" in sys.argv
    ranked, total_bytes, repo_count = measure_languages()
    slices = top_with_other(ranked)
    total_kb = round(total_bytes / 1024)
    fresh = build(slices, total_kb, repo_count)

    if not check:
        ASSETS.mkdir(exist_ok=True)
        for name, svg in fresh.items():
            (ASSETS / name).write_text(svg, encoding="utf-8")
            print(f"  ✓ assets/{name}")
        grand = sum(v for _, v in slices)
        print("\n  " + "  ".join(f"{n} {v/grand*100:.1f}%" for n, v in slices))
        return 0

    # --check：只在语言构成真的漂移了才报错。文件逐字节比对会因为
    # 一个 KB 的变化就红，那不是「图过期了」，那是噪音。
    import re
    stale = []
    committed = (ASSETS / "chart-languages-light.svg")
    if not committed.exists():
        print("  ✗ assets/chart-languages-light.svg 不存在，先跑一次不带 --check 的")
        return 1
    text = committed.read_text(encoding="utf-8")
    was = {m.group(1): float(m.group(2)) for m in
           re.finditer(r'font-size="11\.5"[^>]*>([^<]+)</text>'
                       r'<text[^>]*font-size="11"[^>]*>([\d.]+)%</text>', text)}
    grand = sum(v for _, v in slices)
    now = {n: v / grand * 100 for n, v in slices}
    if not was:
        print("  ✗ committed SVG 里读不出百分比 —— 生成格式变了？")
        return 1
    for name in sorted(set(was) | set(now)):
        before, after = was.get(name, 0.0), now.get(name, 0.0)
        drift = abs(after - before)
        mark = "✗" if drift > TOLERANCE_POINTS else "✓"
        if mark == "✗":
            stale.append(name)
        print(f"  {mark}  {name:<12} committed {before:5.1f}%   now {after:5.1f}%"
              f"   ({drift:+.1f} pt)")
    print()
    if stale:
        print(f"  {len(stale)} 项漂移超过 {TOLERANCE_POINTS} 个百分点："
              f"{', '.join(stale)}\n  重跑 python3 scripts/make_charts.py 并提交。")
        return 1
    print(f"  语言构成仍在 ±{TOLERANCE_POINTS} 个百分点内，图表不需要重画。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
