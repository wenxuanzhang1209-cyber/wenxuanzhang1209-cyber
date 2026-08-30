#!/usr/bin/env python3
"""确认 README 里每一张图、每一条链接都还活着。

    python3 scripts/check_links.py

为什么需要它：这一页上大部分图片是**外链**到别的仓库的 raw 文件。
外链的好处是那边更新了这边自动跟着更新，代价是那边改个文件名，
这边就会静默地裂开一块 —— 页面照常渲染，只是多出一个碎图标。
没有任何东西会报错，而看到碎图的人恰好是第一次来的访客。

本地文件（assets/*.svg）也一起查：它们是 make_charts.py 生成的，
删掉一个不会有人发现，直到主页上少了一张图。

退出码 0 表示全部可达。
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READMES = ["README.md", "README.zh-CN.md"]

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty():
    GREEN = RED = YELLOW = DIM = RESET = ""

#: 只查图片和站内相对链接。外部 https 链接（GitHub 仓库页、PR）不查 ——
#: 它们要么是自己的仓库，要么是第三方的 PR 页，前者不会消失，
#: 后者返回 404 也不该让这个仓库的 CI 变红。
IMG = re.compile(r'(?:src|srcset)="([^"]+)"')
REL = re.compile(r'\]\((?!https?:|#)([^)]+)\)')


def collect() -> dict[str, list[str]]:
    """URL -> 出现在哪些文件里。同一张图两个 README 都用，只查一次。"""
    found: dict[str, list[str]] = {}
    for name in READMES:
        path = ROOT / name
        if not path.exists():
            print(f"  {RED}✗{RESET}  {name} 不存在")
            raise SystemExit(1)
        text = path.read_text(encoding="utf-8")
        for url in IMG.findall(text) + REL.findall(text):
            found.setdefault(url.split("#")[0], []).append(name)
    return found


def check(url: str) -> tuple[bool, str]:
    if url.startswith(("http://", "https://")):
        # img.shields.io 的徽章不查：它是动态生成的，偶发 5xx 很常见，
        # 为此把 CI 弄红没有意义。碎掉的徽章也一眼能看出来。
        if "img.shields.io" in url or "/actions/workflows/" in url:
            return True, "skipped (badge)"
        request = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "jkinco-profile-linkcheck"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status == 200, f"HTTP {response.status}"
        except urllib.error.HTTPError as error:
            return False, f"HTTP {error.code}"
        except Exception as error:  # 网络问题不等于链接坏了，但也不能当通过
            return False, f"{type(error).__name__}: {error}"
    target = (ROOT / url).resolve()
    if ROOT not in target.parents and target != ROOT:
        return False, "指到仓库外面去了"
    return target.exists(), "本地文件存在" if target.exists() else "本地文件不存在"


def main() -> int:
    found = collect()
    print(f"{DIM}核对 {', '.join(READMES)} 里的 {len(found)} 个图片与站内链接{RESET}\n")
    broken = 0
    for url in sorted(found):
        ok, note = check(url)
        shown = url if len(url) <= 78 else url[:75] + "..."
        if ok:
            mark = f"{DIM}-{RESET}" if "skipped" in note else f"{GREEN}✓{RESET}"
            print(f"  {mark}  {shown}")
        else:
            print(f"  {RED}✗{RESET}  {shown}\n       {note}  ({', '.join(found[url])})")
            broken += 1
    print()
    if broken:
        print(f"{RED}{broken} 个链接是坏的。{RESET}主页上对应的位置现在是一个碎图标。")
        return 1
    print(f"{GREEN}全部可达。{RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
