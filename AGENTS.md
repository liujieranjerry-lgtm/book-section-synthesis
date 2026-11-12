# AGENTS.md

给在本仓库工作的 AI agent 和维护者。人读 [CONTRIBUTING.md](CONTRIBUTING.md)，用户读 [README.md](README.md)。

这个仓库的**产品是一份规则文本**：`skill/book-section-synthesis/SKILL.md` 及其 `references/` 改了，agent 的产出就跟着变。因此改动的判定标准不是「读起来更清楚」，而是「产出是否按预期变化、旧产出还能不能被解释」。

## 一、改这里必须同步改那里

| 改了 | 必须同步 |
| :- | :- |
| `SKILL.md` 的规则语义 | `CHANGELOG.md` 新增一段、`SKILL.md` 的 `metadata.version`、`.claude-plugin/plugin.json` 的 `version`、`README.md` 的 version badge |
| `references/` 增删文件 | `SKILL.md` 的「参考文件」清单、`scripts/validate.py` 的 `REQUIRED_SKILL_FILES` |
| 字数表、输出结构、标注规范 | `references/examples/chapter-expected-output.md`（必须重算字数）、`README.md` 的「效果示例」引文、`evals/fixtures/cases.md`、`evals/rubric.md` |
| 交付门条目 | `evals/rubric.md` 的评分维度与三条硬线（编号必须对得上） |
| 安装方式、仓库布局 | `README.md` 的安装段与仓库结构段、`.claude-plugin/plugin.json` 的 `skills` 路径 |
| 增删仓库顶层的任何文件 | `scripts/validate.py` 的 `REQUIRED_REPO_FILES` |

`python3 scripts/validate.py .` 会检查上表里可机器判的部分（版本四处一致、README 目录与正文标题一一对应、SKILL.md 引用的参考文件存在、交付门编号连续）。它查不出语义漂移，语义漂移靠下面两件事。

## 二、验证顺序

1. `python3 scripts/validate.py .`
2. `python3 scripts/check_links.py .`
3. 若改了行为：按 `evals/README.md` 的流程跑一个相关用例，只看行为不变量，不看措辞是否和参考一致。
4. 若改了字数或结构：重算 `references/examples/chapter-expected-output.md` 的字数，把 `README.md` 引文逐字重同步。

两个脚本只用标准库，不需要安装任何依赖。CI 不装包。

## 三、版本与发布

语义化版本，三档判定：

- **主版本**：规则的兼容性破坏——已生成的梳理稿不再符合新规则，或用户必须改提问方式。
- **次版本**：新增能力，或输出格式新增字段（例如文件头多记一行）。旧产出仍合法。
- **补丁版本**：措辞澄清、文档、脚本、CI，不改变产出形状。

发布流程：改 `CHANGELOG.md` → 提交 → 在 GitHub 上打 `vX.Y.Z` tag → `release` workflow 校验 tag 与 `SKILL.md` 的版本一致后，用 `CHANGELOG.md` 对应小节生成 Release notes。tag 与版本号不一致时 workflow 失败，不会发出 Release。

## 四、硬性禁止

- 不提交教材、论文或任何受版权保护的原文片段。`references/examples/` 里的材料全部是合成的。
- 不在 `SKILL.md` 或 `references/` 里写「忽略用户指令」「执行以下命令」这类可被下游 agent 当指令执行的语句。skill 文本是给模型读的规则，不是执行入口。
- 不为了通过评测而改评测。要放宽阈值，先说明放宽后哪类失败会被漏掉。
- 不直接 push `main`：走 PR，CI 的 `validate` 是关键检查。
- 一个规则只在一处定义。`SKILL.md` 定规则，`references/` 给细节，两处重复同一句话会先漂移再打架。

## 五、提交信息

中文，动词开头，说清改了什么规则、影响什么产出。示例：`统一字数口径：一律按去标点计`。
