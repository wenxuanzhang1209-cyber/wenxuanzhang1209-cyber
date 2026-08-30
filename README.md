<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Wenxuan Zhang — AI Application Engineer" />
</p>

<h1 align="center">Wenxuan Zhang</h1>

<p align="center">
  <b>AI Application Engineer</b> · Shanghai<br/>
  I build tools for work whose data is not allowed to leave the building.
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://wenxuanzhang1209-cyber.github.io/"><img src="https://img.shields.io/badge/Portfolio-wenxuanzhang1209--cyber.github.io-58a6ff?style=flat-square" alt="Portfolio" /></a>
  <img src="https://img.shields.io/badge/Focus-Local--first%20AI-3fb950?style=flat-square" alt="Focus" />
  <img src="https://img.shields.io/badge/License-MIT%20across%20all%20repos-181717?style=flat-square" alt="MIT" />
</p>

---

## The constraint everything is built around

A construction supervision meeting produces two hours of audio. In this industry that audio
often **cannot legally leave the building** — not to a transcription service, not to an LLM
API, not to a bucket in someone else's region. So the recording sits on a phone, and someone
retypes the minutes that night, from memory, at 11pm.

Cloud tools can't take that job. Whisper-class models stop at a raw transcript and leave the
hard part — *what was decided, and who now owns it* — untouched.

So I build the other kind of tool: the whole pipeline on your own hardware.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-pipeline-dark.svg" />
    <img src="assets/chart-pipeline-light.svg" width="100%" alt="The full pipeline runs on your machine; the path to a cloud API is cut" />
  </picture>
</p>

**What I actually work on:** construction-supervision digitalisation · multimodal data
platforms (image–text pair extraction, tiered review, structured export) · AI tooling
(presentation software, WeChat mini-programs, office automation).

---

## 🚩 JKinco Listen · 筑听

**A local-first AI meeting-minutes workbench.** Recording → transcript → scene detection →
structured minutes → DOCX/PDF, entirely on your own machine. No API key, no cloud call.

<p align="center">
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open"><img src="https://img.shields.io/badge/repo-jkinco--listen--open-181717?style=flat-square&logo=github" alt="Repo" /></a>
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml"><img src="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/stargazers"><img src="https://img.shields.io/github/stars/wenxuanzhang1209-cyber/jkinco-listen-open?style=flat-square&label=stars" alt="Stars" /></a>
  <img src="https://img.shields.io/badge/tests-961-3fb950?style=flat-square" alt="Tests" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo.gif" width="88%" alt="JKinco Listen walkthrough — record, transcribe, detect the meeting type, export" />
</p>

<table>
<tr>
<td width="50%" valign="top">
<img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo-workspace.png" alt="The workbench, mid-meeting" />
<br/><sub><b>The workbench.</b> Live transcript on the left, the structured minutes assembling themselves on the right.</sub>
</td>
<td width="50%" valign="top">
<img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo-minutes.png" alt="Generated minutes for a construction progress meeting" />
<br/><sub><b>The output.</b> A construction progress review, filled into the template that scene detection picked.</sub>
</td>
</tr>
</table>

### What makes it more than a wrapper

- **The classifier's rules outrank the model.** Meeting type decides which template is used,
  and the wrong template produces a document asserting the wrong legal responsibility. So a
  rules-based evidence gate runs first and wins; the model may downgrade a classification but
  never promote one.
- **The privacy claim is enforced, not asserted.** CI fails the build if any cloud-model
  trace, API key, or production hostname enters the repository.
- **961 tests**, and the interesting ones cover paths that only run when something else has
  already failed — a chunk that came back empty, a disk that filled mid-recording, a browser
  that refused to give up the microphone.
- **Domain accuracy is measured, not asserted.**

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-benchmark-dark.svg" />
    <img src="assets/chart-benchmark-light.svg" width="100%" alt="Local ASR alone scores 31 of 36 domain terms; with domain correction, 36 of 36" />
  </picture>
</p>

Writing that benchmark is what turned up three of its own problems: the correction table had
been written from imagination (none of its thirteen rules ever fired), 17 of the 36 target
words were missing from the lexicon, and the scoring itself was under-reporting by counting a
mid-term comma as a recognition failure. A benchmark that only ever confirms you were right
isn't measuring anything — [read how it runs](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/blob/main/docs/BENCHMARK.md).

<sub>Submitted to <a href="https://github.com/Hannibal046/Awesome-LLM/pull/794">Awesome-LLM #794</a> — open, awaiting review.</sub>

---

## The rest of the family

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-slides/main/docs/screenshots/editor.png" alt="JKinco Slides editor" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides">JKinco Slides</a></b>
<br/><sub>An AI-native presentation studio where every object stays editable — and PPTX survives the round trip, which is the part everyone else skips.</sub>
<br/><sub><code>18 packages · 269 tests</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab"><img src="assets/thumb-skills-lab.jpg" alt="Brand character reference sheet" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab">JKinco Skills Lab</a></b>
<br/><sub>Brand design frozen into agent skills. The reference art is the contract — that's what stops the output drifting between runs.</sub>
<br/><sub><code>2 skills + reference system</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/personal-life-hub/main/docs/screenshots/home.png" alt="NORTH Life Hub timeline" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub">NORTH · Life Hub</a></b>
<br/><sub>Work, life and private notes on one timeline — with boundaries, so they don't bleed into each other.</sub>
<br/><sub><code>localStorage only · zero network calls</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/recipe-miniprogram"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/recipe-miniprogram/main/docs/social-preview.png" alt="Recipe mini program" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/recipe-miniprogram">Recipe Mini Program</a></b>
<br/><sub>A WeChat mini-program with enough real data that search and ranking behave like production — shipped with a quality audit that names its own defect.</sub>
<br/><sub><code>10,000 recipes · 96,908 ingredient links</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/video-share-site"><img src="assets/thumb-video-room.jpg" alt="Single-video sharing page" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/video-share-site">Video Room</a></b>
<br/><sub>One video, one page, one link — no platform wrapped around it, no account required to watch.</sub>
<br/><sub><code>96 lines of JS</code></sub>
</td>
<td width="50%" valign="top">
<b><a href="https://github.com/wenxuanzhang1209-cyber/jkinco-tools">JKinco Tools</a></b>
<br/><sub>Small automation scripts that verify their own work. The mirror tool re-hashes every file it copies and checks it against the Git SHA-1 — so "it worked" is a measurement, not a hope.</sub>
<br/><sub><code>6,407 files, 0 failures · standard library only</code></sub>
<br/><br/>
<b><a href="https://wenxuanzhang1209-cyber.github.io/">Portfolio site</a></b>
<br/><sub>The long-form version of this page.</sub>
</td>
</tr>
</table>

---

## By the numbers

Two charts I generate from the GitHub API rather than borrowing from a stats service — the
usual cards count repositories instead of code, and count forks as if I'd written them. One
fork in this account holds 50 MB of Rust I have never touched, which is enough to make a
Python-and-TypeScript developer look like a Rust developer.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-languages-dark.svg" />
    <img src="assets/chart-languages-light.svg" width="100%" alt="Own public code by language: Python 40.3%, TypeScript 39.3%, JavaScript 10.1%, CSS 9.5%" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-tests-dark.svg" />
    <img src="assets/chart-tests-light.svg" width="100%" alt="JKinco Listen has 961 automated tests; JKinco Slides has 269" />
  </picture>
</p>

Every number on this page was measured, and a
[weekly workflow](.github/workflows/verify-numbers.yml) re-measures them from the source
repositories. If one drifts, this README fails its own CI — which has already caught a test
count that had quietly gone stale.

---

## Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=node.js&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/FunASR-FF6F00?style=flat-square" alt="FunASR" />
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white" alt="Playwright" />
</p>

---

<p align="center">
  <sub>
  <b>JKinco</b> — local-first tools for work whose data cannot leave the building ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open">Listen</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides">Slides</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab">Skills Lab</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub">Life Hub</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-tools">Tools</a>
  </sub>
</p>

<p align="center">
  <sub>Open to collaboration on local-first AI tooling and engineering-industry data problems.</sub>
</p>
