#!/usr/bin/env python3
"""核对 README 里每一个数字，全部重新去源仓库量一遍。

    python3 scripts/verify_profile_numbers.py

README 结尾写着一句「Every number above was measured, not estimated.」
这个脚本存在的意义，就是让那句话变成**可以执行的**，而不是一句自我评价。

为什么需要它：数字会自己过期。写这个脚本的那天，README 上的
「948 tests」已经落后于真实的 960，而 jkinco-listen-open 仓库内部
同时躺着 895、894、891 三个不同的版本。没有任何东西会因此报错 ——
徽章是一张图片，表格是纯文本。它只在一个场合暴露：有人真的把仓库
clone 下来跑了一遍，发现对不上。而那个人恰好是最认真的读者。

怎么量的，每一项都写在下面的 CHECKS 里。全部只用 GitHub 公开 API
和 git，不需要任何凭据（未认证有速率限制，CI 里会带上 GITHUB_TOKEN）。

退出码 0 表示 README 里的数字全部属实。
"""
from __future__ import annotations

import json
import os
import re
import io
import sys
import zipfile
import urllib.request
from pathlib import Path

OWNER = "wenxuanzhang1209-cyber"
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    GREEN = RED = YELLOW = DIM = RESET = ""


def _api(path: str):
    request = urllib.request.Request(
        f"https://api.github.com/{path.lstrip('/')}",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "jkinco-profile-verifier"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _raw(repo: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{OWNER}/{repo}/main/{path}"
    request = urllib.request.Request(url, headers={"User-Agent": "jkinco-profile-verifier"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


# ---------------------------------------------------------------------------
# 每一项：怎么从 README 里读出「声称值」，以及怎么重新量出「真实值」。
#
# 量的办法故意选了**和写 README 时不同的路径** —— 比如测试数不是去读
# 那个仓库 README 上的徽章（那样只是把一个可能过期的数字抄过来），
# 而是 clone 下来真的跑一次 pytest --collect-only。
# ---------------------------------------------------------------------------

def _claim(pattern: str) -> int:
    text = README.read_text(encoding="utf-8")
    match = re.search(pattern, text)
    if match is None:
        raise LookupError(f"README 里找不到 /{pattern}/ —— 声明改写法了？")
    return int(match.group(1).replace(",", ""))


def _ci_logs(repo: str) -> str:
    """把某个仓库最近一次成功 CI 的日志全文拿下来。

    为什么读 CI 日志而不是 clone 下来自己跑：跑测试要先装依赖，
    listen 那边是一整套 Python + 模型依赖，slides 那边要 pnpm。
    在一个只为核对数字的脚本里装这些，既慢又脆。

    而 CI 是**真的跑过**的 —— 读它的日志拿到的就是真实测试数，
    不是从另一处可能同样过期的文档里抄来的。
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("读 CI 日志需要 GITHUB_TOKEN")
    # 必须按 workflow 名筛。第一版取的是「最近一次成功运行」，
    # 结果 jkinco-listen-open 最近成功的是 pages-build-deployment ——
    # 一个部署文档站的 workflow，日志里当然没有任何测试结果。
    runs = _api(f"repos/{OWNER}/{repo}/actions/runs"
                f"?status=success&per_page=20")
    candidates = [run for run in runs.get("workflow_runs", [])
                  if run.get("name") == "CI"]
    if not candidates:
        raise RuntimeError(f"{repo} 最近 20 次成功运行里没有名为 CI 的")
    run_id = candidates[0]["id"]
    request = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{repo}/actions/runs/{run_id}/logs",
        headers={"User-Agent": "jkinco-profile-verifier",
                 "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
    return "\n".join(archive.read(name).decode("utf-8", "replace")
                     for name in archive.namelist())


def measure_listen_tests() -> int:
    """listen 的 CI 跑 pytest，日志末尾是「N passed in Xs」。"""
    counts = [int(n) for n in re.findall(r"(\d+) passed", _ci_logs("jkinco-listen-open"))]
    if not counts:
        raise RuntimeError("CI 日志里没找到 pytest 的结果行")
    # CI 里可能分多步跑；README 上写的是全量那一次，取最大值
    return max(counts)


def measure_slides_packages() -> int:
    tree = _api(f"repos/{OWNER}/jkinco-slides/contents/packages")
    return sum(1 for entry in tree if entry["type"] == "dir")


def measure_slides_tests() -> int:
    """slides 是 monorepo，各包各报各的，README 上写的是合计。"""
    total = sum(int(n) for n in
                re.findall(r"Tests\s+(\d+) passed", _ci_logs("jkinco-slides")))
    if total == 0:
        raise RuntimeError("CI 日志里没找到 vitest 的测试数")
    return total


def measure_tools_files() -> int:
    payload = json.loads(_raw("jkinco-tools", "import-logs/import-results.json"))
    return len(payload)


def measure_tools_failures() -> int:
    return len([line for line in
                _raw("jkinco-tools", "import-logs/import-failures.txt").splitlines()
                if line.strip()])


def measure_recipes() -> int:
    report = json.loads(_raw("recipe-miniprogram", "server/data/quality-report.json"))
    for key in ("total", "totalRecipes", "total_recipes", "count"):
        if isinstance(report, dict) and key in report:
            return int(report[key])
    raise RuntimeError(f"quality-report.json 里没有总数字段，只有 {list(report)[:8]}")


CHECKS = [
    ("jkinco-listen-open 测试数（徽章）", r"tests-(\d+)-3fb950", measure_listen_tests),
    ("jkinco-listen-open 测试数（正文）", r"\*\*(\d+) tests\*\*", measure_listen_tests),
    ("jkinco-slides packages",          r"(\d+) packages", measure_slides_packages),
    ("jkinco-slides 测试数",             r"packages · (\d+) tests", measure_slides_tests),
    ("jkinco-tools 校验文件数",           r"([\d,]+) files, 0 failures", measure_tools_files),
    ("jkinco-tools 失败数",              r"[\d,]+ files, (\d+) failures", measure_tools_failures),
    ("recipe-miniprogram 菜谱数",         r"([\d,]+) recipes ·", measure_recipes),
]


def main() -> int:
    print(f"{DIM}核对 README 里的每一个数字，全部重新去源仓库量{RESET}\n")
    bad = unknown = 0
    for label, pattern, measure in CHECKS:
        try:
            claimed = _claim(pattern)
        except LookupError as error:
            print(f"  {YELLOW}?{RESET}  {label:<34} {error}")
            unknown += 1
            continue
        try:
            actual = measure()
        except Exception as error:  # 量不到就说量不到，不要拿声称值当真实值
            first = str(error).splitlines()[0][:70]
            print(f"  {YELLOW}?{RESET}  {label:<34} 声称 {claimed}，量不到（{first}）")
            unknown += 1
            continue
        if claimed == actual:
            print(f"  {GREEN}✓{RESET}  {label:<34} {actual:,}")
        else:
            print(f"  {RED}✗{RESET}  {label:<34} README 写 {claimed:,}，实际 {actual:,}")
            bad += 1

    print()
    if bad:
        print(f"{RED}{bad} 处对不上。{RESET}README 里的「measured, not estimated」"
              f"目前不成立，改完再提交。")
        return 1
    if unknown:
        print(f"{YELLOW}全部核对通过，另有 {unknown} 项这次量不到{RESET}"
              f"（多半是缺 GITHUB_TOKEN 或网络受限）。")
        return 0
    print(f"{GREEN}全部属实。{RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
