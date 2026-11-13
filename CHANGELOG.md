# Changelog

本项目遵循语义化版本。

## [Unreleased]

### Changed

- `validate` workflow 只在 `main` 的 push 与 pull request 上触发：同一分支不再因为 push 与 pull_request 各跑一遍；tag 只由 `release` workflow 负责。


## [3.1.0] - 2026-11-13

### Added

- **节间衔接**：每节第一句必须先接住上一节留下的问题（入口句），末尾交代留给下一节的问题（出口句），把逐节从「互不相连的段落」变成一条链。首节的入口来自全章主线末句，末节的出口指向全章收束第一句，收束开头也规定要先接住末节缺口。
- 入口句的写法判据：只准引用上一节的结论或问题、不准重述；必须点名被承接的对象，不许用「接下来」一类空过渡；一句为限，≤30 字（简略档 ≤20 字），从本节既有预算里出，不额外加字数。
- 交付门新增第 4 项「衔接」，原第 4–10 项顺延为第 5–11 项。

### Changed

- 「每节讲三件事」改为「三件事加两个接口」，细则写在 SKILL.md 第 3 步；`references/fidelity.md` 的引用规则同步加一条「接口句只引用，不重述，不加 `*诠释*`」。
- 模式③ 不受入口句约束，它的衔接由后部关系段承担。
- 示例产出逐节重写开头以符合新规则，字数仍在标准档区间内；`README.md` 引文与 `evals/` 相关条目同步。

## [3.0.1] - 2026-11-12

规则文本没有变化，产出形状不变。这一版改的是仓库本身的可靠性：能被 `claude plugin validate` 认出来，版本号不再靠人记，脚本不再依赖第三方包。

### Added

- `.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json`：现在可以作为 Claude Code 插件安装，`/plugin marketplace add liujieranjerry-lgtm/book-section-synthesis` 后即可启用。
- `.github/workflows/release.yml`：打 `vX.Y.Z` tag 触发；先校验 tag 与 `SKILL.md` 的版本一致，再从 `CHANGELOG.md` 抽取对应小节作为 Release notes。不一致时失败，不会发出 Release。
- `scripts/release_notes.py`：本地也能用同一条命令预览某版本的 Release notes。
- `AGENTS.md`：给在本仓库工作的 agent 的「改这里必须同步改那里」对照表、验证顺序、版本三档判定与硬性禁止。
- `SECURITY.md`：威胁模型（指令注入、供应链、评测数据、用户材料外泄）与为此做的控制。

### Changed

- `scripts/validate.py` 改为纯标准库，不再依赖 PyYAML。新增检查：版本号四处一致（`SKILL.md` / `CHANGELOG.md` 最新段 / `plugin.json` / README badge）、`plugin.json` 的 `description` 与 frontmatter 逐字一致、README 目录与正文二级标题一一对应、`SKILL.md` 引用的参考文件都存在、交付门编号 1–N 连续、`SKILL.md` 正文不超过 10,000 字符、市场清单条目不得重复声明组件字段。
- `scripts/check_links.py` 增加锚点校验：带 `#片段` 的链接必须能对上目标文件里某个标题生成的锚点。
- 全部 GitHub Actions 固定到 commit SHA（不再用浮动 `@v7`），workflow 顶层 `permissions: contents: read`，`checkout` 关闭 `persist-credentials`，CI 不再安装任何依赖。

### Removed

- `requirements-dev.txt`：校验脚本不再需要第三方依赖，CI 里也就没有包安装这一步。

## [3.0.0] - 2026-11-12

范围变更：从「一个小节」改为「一整章」。旧版按小节设计的模式、骨架、篇幅表全部作废。

### Breaking

- 只做整章。只给一个小节时，按同一流程把该小节当作「章」处理，其中的自然子标题当作「节」。
- 模式改为 ① 对原文的梳理 ② 梳理＋词语阐释 ③ 精简版梳理；原 A/B/C（忠实梳理／讲解增强／文本审校）不再作为模式，文本审校降为第 5 问的可选附加。
- 篇幅主轴从「正文自然段数」改为「每节字数」；`4–8 段 / 2–4 段 / 超 8 段` 与档位表作废。
- 节层八类骨架作废，改为章层四类（论证型／综述型／史论型／导论型），只判章、不判节。
- 移除 `templates/section-note.md` 与「保真说明」节；新增「存疑项」（最多三行，没有的类别省略、不写「无」）。

### Added

- 开始前的五个问题（读者基础／模式／档位／补充背景／文本审校），一次性问完；模式③ 跳过档位问。
- 读者四档与对应解释策略；读者档位决定每条术语解释写多细，模式决定收哪些词。
- 可选的外部背景通道 `〔补充背景〕……〔/补充背景〕`，默认关闭，每章不超过 5 处。
- 章层三类新增结构：全章主线（每句带强制关系，判据是删掉全部节号后仍读得通）、全章收束（立场地图／代价对称性／未解决问题）、逐节梳理（严格按原文顺序）。
- 字数推导规则：正文 = 每节区间 × 节数 + 章级固定件；章节长短悬殊时（最长 ÷ 最短 > 1.75）按原文篇幅占比分配。
- 全章正文硬上限 12,000 字与降级顺序（术语注 → 补充背景 → 正文 → 降档）；术语注不计入上限。
- 章末附属部分按**名称**识别（Notes／Further Reading／练习／索引），不按标题层级；每类给默认处理方式。
- 图表默认从源文件裁切嵌入 `assets/`；无裁图工具时退化为一句描述并在存疑项记「图 X.X 未嵌图」。
- `*诠释*：` 标注规范（斜体只包「诠释」二字）与密度上限（每节 ≤4 处）。
- 交付门 10 项，可直接逐条检查。
- 新增 `references/examples/chapter-{synthetic-input,expected-output,anti-example}.md` 与配图 `assets/ch08-fig8-1.png`（合成材料，第 8 章 7 节）。
- `scripts/check_links.py`，检查 Markdown 本地链接。
- `.github/dependabot.yml`，每周检查 GitHub Actions 更新。

### Changed

- `README.md` 按整章重写；`QUICK_PROMPTS.md` 提示词全部重写（14 条）。
- `evals/rubric.md`、`evals/fixtures/cases.md`、`evals/README.md` 按 v3 交付门重写。
- `scripts/validate.py` 必需文件列表去掉 `templates/section-note.md`，加入三份 examples。
- CI 升级到 `actions/checkout@v7` 和 `actions/setup-python@v7`，增加链接检查步骤和并发取消。
- `agents/openai.yaml` 改为「课本整章梳理」。
- `SKILL.md` 版本改为 3.0.0，description 不再排除整章请求。

## [2.2.0] - 2026-09-22

### Changed

- 仓库重排为“根目录文档 + `skill/book-section-synthesis/` 运行文件”。
- 安装方式改为目录 URL：`$skill-installer install https://github.com/liujieranjerry-lgtm/book-section-synthesis/tree/main/skill/book-section-synthesis`。
- 官方安装器、`npx skills`、手动安装、验证/更新说明同步更新。
- `scripts/validate.py` 改为同时校验根目录文件和 `skill/` 子目录。
- `SKILL.md` 版本改为 2.2.0。

## [2.1.0] - 2026-09-22

### Added

- `requirements-dev.txt`，声明本地结构校验所需的 PyYAML。
- `scripts/validate.py` 在缺少 PyYAML 时给出明确的安装提示。
- `QUICK_PROMPTS.md`，按场景提供可直接复制的提示词。
- `templates/section-note.md`，固定边界说明、正文、术语注和保真说明的笔记骨架。
- `references/fidelity.md` 增加 Claim—Evidence—Verdict 表。
- README 增加评测覆盖与验证状态。

### Changed

- CI 改为从 `requirements-dev.txt` 安装开发依赖。
- README 与 CONTRIBUTING 增加本地开发环境说明。
- README 安装章节改为可直接执行的 `gh repo clone` / `git clone`、更新、卸载和验证命令。
- README 重写为产品化结构：快速开始、效果示例、适合与不适合、工作流、安装、FAQ、限制与路线图。
- 仓库转为 public；README 安装说明改为公开仓库版本，并补充 Python / npm / git 三种安装方式的区别；`--method git` 作为更稳定的安装方式保留。
- README 收紧到约 300 行，提示词移到 `QUICK_PROMPTS.md`，安装命令去重。
- `scripts/validate.py` 必需文件列表更新。
- `SKILL.md` 版本改为 2.1.0，并在固定结构笔记场景引用 `templates/section-note.md`。

## [2.0.0] - 2026-09-22

### Added

- 原文硬门槛：没有原文时请求用户提供原文，不再凭记忆或二手介绍代写。
- 文本类型判定与八类骨架，避免把所有小节写成论证文。
- A/B/C 三种模式：忠实梳理、讲解增强、文本审校。
- 四类陈述：原文主张、直接引用、隐含推理、外部补充。
- 读者知识基础校准：零基础、学过相关课程、本专业读者。
- 文本审校的错误分类与证据标准。
- 可执行的交付门，覆盖边界、覆盖、保真、术语、篇幅和版权。
- 评测用例、评分表与前向测试流程。
- 开源仓库治理文件：README、LICENSE、CHANGELOG、CONTRIBUTING、CI。

### Changed

- 默认篇幅改为 4–8 个正文自然段；紧凑模式为 2–4 段。
- description 重写，加入原文前提和明确的非适用场景。
- 示例从两个假设性片段扩展为完整输入—输出示例与反例对照。
- 边界处理区分“会改变主要结论的歧义”和“标题层级细微差异”。
- 术语语言规则改为保留原文术语，不再默认附英文。
