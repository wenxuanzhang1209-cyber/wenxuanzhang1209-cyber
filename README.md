<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Wenxuan Zhang — AI Application Engineer" />
</p>

<h1 align="center">Wenxuan Zhang</h1>

<p align="center">
  <b>AI Application Engineer</b> · Shanghai<br/>
  I build tools that take the repetitive parts of engineering work off people's hands.<br/>
  <sub>把工程行业里重复、繁琐的工作交给工具</sub>
</p>

<p align="center">
  <a href="https://wenxuanzhang1209-cyber.github.io/"><img src="https://img.shields.io/badge/Portfolio-wenxuanzhang1209--cyber.github.io-58a6ff?style=flat-square" alt="Portfolio" /></a>
  <img src="https://img.shields.io/badge/Focus-Local--first%20AI-3fb950?style=flat-square" alt="Focus" />
  <img src="https://img.shields.io/badge/License-MIT%20across%20all%20repos-181717?style=flat-square" alt="MIT" />
</p>

---

## What I work on

**Construction supervision, digitised.** Site-process recognition, field annotation, and the
data work behind it. The constraint that shapes everything: this industry's recordings and
documents often cannot legally leave the building — so the tools have to run locally.

**Multimodal data platforms.** Image–text pair extraction and proofreading, question
generation, tiered review, structured export.

**AI tooling.** Presentation software, WeChat mini-programs, office automation.

Three things I care about in every project: **reproducible, documented, and simpler than what
it replaced.**

<sub>工程监理数字化 · 多模态数据平台 · AI 工具开发。三个坚持：可复现、有文档、把复杂流程变简单。</sub>

---

## 🚩 JKinco Listen · 筑听

**A local-first AI meeting-minutes workbench.** Recording → transcript → scene detection →
structured minutes → DOCX/PDF, entirely on your own machine. No API key, no cloud call.

[![Repo](https://img.shields.io/badge/repo-jkinco--listen--open-181717?style=flat-square&logo=github)](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open)
[![CI](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml/badge.svg)](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml)
[![Stars](https://img.shields.io/github/stars/wenxuanzhang1209-cyber/jkinco-listen-open?style=flat-square&label=stars)](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/stargazers)
![Tests](https://img.shields.io/badge/tests-924-3fb950?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

<p align="center">
  <img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo.gif" width="88%" alt="JKinco Listen walkthrough" />
</p>

Most meeting tools force a trade: cloud services want your audio uploaded, and Whisper-class
models stop at a raw transcript. For a construction review, an interview, or a client visit,
neither is acceptable — so people type the notes by hand.

What makes it more than a wrapper:

- **The classifier's rules outrank the model.** Meeting type decides which template is used,
  and the wrong template produces a document asserting the wrong legal responsibility. So a
  rules-based evidence gate runs first and wins; the model may downgrade a classification but
  never promote one.
- **The privacy claim is enforced, not asserted.** CI fails the build if any cloud-model
  trace, API key, or production hostname enters the repository.
- **924 tests**, and the interesting ones cover paths that only run when something else has
  already failed.

<sub>本地优先的 AI 会议纪要工作台。录音 → 转写 → 场景识别 → 结构化纪要 → 导出，全程不出本机。
场景判定用规则证据门控，模型只能降级不能升级——套错模板等于让文件写错责任主体。</sub>

<sub>Submitted to <a href="https://github.com/Hannibal046/Awesome-LLM/pull/794">Awesome-LLM #794</a> — open, awaiting review.
已向 Awesome-LLM 投稿（PR #794），待评审。</sub>

---

## The rest of the family

| Project | What it is | Scale |
| --- | --- | --- |
| [**JKinco Slides**](https://github.com/wenxuanzhang1209-cyber/jkinco-slides) | AI-native presentation studio — every object stays editable, PPTX survives the round trip | 18 packages · 269 tests |
| [**JKinco Skills Lab**](https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab) | Brand design frozen into agent skills, so the output stops drifting between runs | 2 skills + reference system |
| [**NORTH · Life Hub**](https://github.com/wenxuanzhang1209-cyber/personal-life-hub) | Work, life, and private notes on one timeline with space boundaries | `localStorage` only |
| [**JKinco Tools**](https://github.com/wenxuanzhang1209-cyber/jkinco-tools) | Mirrors a repo tree, verifying every blob against its Git SHA-1 | 6,407 files, 0 failures |
| [**Recipe Mini Program**](https://github.com/wenxuanzhang1209-cyber/recipe-miniprogram) | WeChat mini-program — enough real data that search and ranking behave like production | 10,000 recipes · 96,908 ingredient links |
| [**Video Room**](https://github.com/wenxuanzhang1209-cyber/video-share-site) | One video, one page, one link — no platform wrapped around it | 96 lines of JS |

All MIT. Every number above was measured, not estimated.

<sub>以上数字全部是实测的，不是估计的。</sub>

---

## Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=node.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" />
</p>

<p align="center">
  <img height="160em" src="https://github-stats.vercel.app/api?username=wenxuanzhang1209-cyber&show_icons=true&count_private=true&hide_border=true&theme=github_dark" alt="GitHub stats" />
  <img height="160em" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=wenxuanzhang1209-cyber&theme=github_dark" alt="Languages" />
</p>

---

<sub>
<b>JKinco</b> — local-first tools for work whose data cannot leave the building ·
<a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open">Listen</a> ·
<a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides">Slides</a> ·
<a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab">Skills Lab</a> ·
<a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub">Life Hub</a> ·
<a href="https://github.com/wenxuanzhang1209-cyber/jkinco-tools">Tools</a>
</sub>

<p align="center">
  <sub>Open to collaboration on local-first AI tooling and engineering-industry data problems.<br/>
  欢迎就本地优先的 AI 工具与工程行业数据问题交流。</sub>
</p>
