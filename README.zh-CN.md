<p align="center">
  <img src="assets/banner.svg" width="100%" alt="张文轩 — AI 应用工程师" />
</p>

<h1 align="center">张文轩 · Wenxuan Zhang</h1>

<p align="center">
  <b>AI 应用工程师</b> · 上海<br/>
  给「数据不许出楼」的那类工作，做能用的工具。
</p>

<p align="center">
  <a href="README.md">English</a> · <b>简体中文</b>
</p>

<p align="center">
  <a href="https://wenxuanzhang1209-cyber.github.io/"><img src="https://img.shields.io/badge/个人站-wenxuanzhang1209--cyber.github.io-58a6ff?style=flat-square" alt="个人站" /></a>
  <img src="https://img.shields.io/badge/方向-本地优先%20AI-3fb950?style=flat-square" alt="方向" />
  <img src="https://img.shields.io/badge/许可-全部仓库%20MIT-181717?style=flat-square" alt="MIT" />
</p>

---

## 一切都是从一个约束长出来的

一场工程监理例会能录出两个小时音频。而在这个行业里，这段音频**通常不允许离开这栋楼** ——
不能传给转写服务，不能发给大模型 API，也不能落到别人机房的对象存储里。于是录音留在手机上，
当晚十一点，有人凭记忆把纪要重新敲一遍。

云端工具接不了这个活。而 Whisper 这一类模型只给到一段纯文本，真正难的那部分 ——
**到底定了什么、这件事现在归谁** —— 一个字都没碰。

所以我做的是另一种工具：整条链路跑在你自己的机器上。

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-pipeline-dark.svg" />
    <img src="assets/chart-pipeline-light.svg" width="100%" alt="整条流水线都在本机运行，通往云端 API 的那条路是断的" />
  </picture>
</p>

<sub>录音 → 转写 → 场景识别 → 纪要 → 导出，五步全部在虚线框内。框外那条通往云端 API 的线是断的
—— 而且这不是 README 里的一句承诺：只要有云模型痕迹、API key 或生产域名混进仓库，CI 会直接把构建打红。</sub>

**具体在做的三件事**：工程监理数字化 · 多模态数据平台（图文对抽取、分级校审、结构化导出）·
AI 工具开发（演示文稿软件、微信小程序、办公自动化）。

---

## 🚩 筑听 JKinco Listen

**本地优先的 AI 会议纪要工作台。** 录音 → 转写 → 场景识别 → 结构化纪要 → DOCX/PDF 导出，
全程不出本机。不需要 API key，不发生任何云端调用。

<p align="center">
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open"><img src="https://img.shields.io/badge/仓库-jkinco--listen--open-181717?style=flat-square&logo=github" alt="仓库" /></a>
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml"><img src="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/stargazers"><img src="https://img.shields.io/github/stars/wenxuanzhang1209-cyber/jkinco-listen-open?style=flat-square&label=stars" alt="Stars" /></a>
  <img src="https://img.shields.io/badge/测试-961-3fb950?style=flat-square" alt="测试数" />
  <img src="https://img.shields.io/badge/许可-MIT-blue?style=flat-square" alt="许可" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo.gif" width="88%" alt="筑听演示 —— 录音、转写、识别会议类型、导出" />
</p>

<table>
<tr>
<td width="50%" valign="top">
<img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo-workspace.png" alt="会议进行中的工作台" />
<br/><sub><b>工作台。</b>左边是实时转写，右边的结构化纪要在同步长出来。</sub>
</td>
<td width="50%" valign="top">
<img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-listen-open/main/docs/demo-minutes.png" alt="工程例会纪要成品" />
<br/><sub><b>成品。</b>一场工程进度例会，填进了场景识别自己挑中的那套模板。</sub>
</td>
</tr>
</table>

### 它凭什么不只是个套壳

- **规则的优先级高于模型。** 会议类型决定用哪套模板，而模板套错，等于让一份文件写错责任主体。
  所以先跑一道基于证据的规则门控，并且规则说了算；模型可以把一个判定**降级**，但永远不能**升级**。
- **隐私不是承诺，是被强制的。** 只要有任何云模型痕迹、API key 或生产域名进入仓库，CI 直接失败。
- **961 个测试**，而且有意思的那些覆盖的都是「别的地方已经出事之后才会走到」的路径 ——
  一个返回空的音频块、录音录到一半满了的磁盘、一个拒绝交出麦克风的浏览器。
- **领域准确率是量出来的，不是说出来的。**

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-benchmark-dark.svg" />
    <img src="assets/chart-benchmark-light.svg" width="100%" alt="纯本地 ASR 命中 36 个领域词中的 31 个，加上领域纠错后 36/36" />
  </picture>
</p>

<sub>36 个通用模型容易听错的工程 / 人事 / 商务术语：纯本地 ASR 命中 31 个，加上领域纠错后 36 个。
合成音频比真实会议室干净，所以 36/36 请当上限看，不是承诺。</sub>

写这个基准本身，反倒查出了它自己的三个问题：纠错表是凭想象写的（十三条规则一条都没被触发过）、
36 个目标词里有 17 个根本不在词表中、评分逻辑还把词中间的一个逗号算成了识别失败，一直在少报。
**一个只会告诉你「你是对的」的基准，等于什么都没测** ——
[看它怎么跑](https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open/blob/main/docs/BENCHMARK.md)。

<sub>已向 <a href="https://github.com/Hannibal046/Awesome-LLM/pull/794">Awesome-LLM 投稿（PR #794）</a>，待评审。</sub>

---

## 其余这些

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/jkinco-slides/main/docs/screenshots/editor.png" alt="JKinco Slides 编辑器" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides">JKinco Slides</a></b>
<br/><sub>AI 原生的演示文稿工作台，每个对象都还能编辑 —— 而且 PPTX 进出一轮不变形，这一步是别家普遍跳过的。</sub>
<br/><sub><code>18 个包 · 269 个测试</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab"><img src="assets/thumb-skills-lab.jpg" alt="品牌角色设定图" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab">JKinco Skills Lab</a></b>
<br/><sub>把品牌设计冻进 agent skill 里。设定图就是契约 —— 靠它，输出才不会每跑一次漂一点。</sub>
<br/><sub><code>2 个 skill + 一套参考体系</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/personal-life-hub/main/docs/screenshots/home.png" alt="NORTH 生活中枢时间线" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub">NORTH · 生活中枢</a></b>
<br/><sub>工作、生活、私人笔记放在同一条时间线上 —— 但彼此之间有边界，不会互相渗。</sub>
<br/><sub><code>只用 localStorage · 零网络请求</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/recipe-miniprogram"><img src="https://raw.githubusercontent.com/wenxuanzhang1209-cyber/recipe-miniprogram/main/docs/social-preview.png" alt="家常菜小程序" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/recipe-miniprogram">家常菜小程序</a></b>
<br/><sub>微信小程序，数据量大到搜索和排序会表现出生产环境的样子 —— 并且附了一份点名自己缺陷的质检报告。</sub>
<br/><sub><code>10,000 道菜 · 96,908 条配料关联</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/wenxuanzhang1209-cyber/video-share-site"><img src="assets/thumb-video-room.jpg" alt="单视频分享页" /></a>
<br/><b><a href="https://github.com/wenxuanzhang1209-cyber/video-share-site">Video Room</a></b>
<br/><sub>一个视频、一个页面、一条链接 —— 外面不裹平台，看的人也不用注册账号。</sub>
<br/><sub><code>96 行 JS</code></sub>
</td>
<td width="50%" valign="top">
<b><a href="https://github.com/wenxuanzhang1209-cyber/jkinco-tools">JKinco Tools</a></b>
<br/><sub>会自己校验自己成果的小脚本。镜像工具把每个文件复制完再重新算一遍哈希，跟 Git 的 SHA-1 对上
——「跑通了」因此是一个测量结果，而不是一种期望。</sub>
<br/><sub><code>6,407 个文件校验，0 失败 · 只用标准库</code></sub>
<br/><br/>
<b><a href="https://wenxuanzhang1209-cyber.github.io/">个人站</a></b>
<br/><sub>这一页的展开版。</sub>
</td>
</tr>
</table>

---

## 用数字说

下面两张图是我自己从 GitHub API 生成的，没用现成的 stats 卡片。原因很具体：那些卡片数的是
**仓库个数**而不是代码量，而且把 fork 当成自己写的算进去。这个账号里有一个 fork 装着
50 MB 我一个字都没写过的 Rust —— 足够把一个写 Python 和 TypeScript 的人显示成 Rust 开发者。

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-languages-dark.svg" />
    <img src="assets/chart-languages-light.svg" width="100%" alt="自有公开代码的语言构成：Python 40.3%、TypeScript 39.3%、JavaScript 10.1%、CSS 9.5%" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/chart-tests-dark.svg" />
    <img src="assets/chart-tests-light.svg" width="100%" alt="筑听 961 个自动化测试，JKinco Slides 269 个" />
  </picture>
</p>

<sub>上图：9 个自有公开仓库、共 2,896 KB 自己写的代码，已排除 fork。Python 与 TypeScript 相差不到一个百分点
—— 前后端体量基本对等。下图：两个主力项目的自动化测试数，取自它们 CI 的真实日志，不是抄自徽章。</sub>

这一页上的每个数字都是量出来的，还有一个[每周跑的 workflow](.github/workflows/verify-numbers.yml)
回到源仓库重新量一遍。哪个数字漂了，这份 README 就会把自己的 CI 弄红 ——
它已经抓到过一次悄悄过期的测试数。

---

## 技术栈

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
  <b>JKinco</b> —— 给数据不能出楼的那类工作，做本地优先的工具 ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-listen-open">筑听</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-slides">Slides</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/JKinco-Skills-Lab">Skills Lab</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/personal-life-hub">生活中枢</a> ·
  <a href="https://github.com/wenxuanzhang1209-cyber/jkinco-tools">Tools</a>
  </sub>
</p>

<p align="center">
  <sub>欢迎就本地优先的 AI 工具、以及工程行业的数据问题交流。</sub>
</p>
