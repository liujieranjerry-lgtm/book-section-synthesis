# Contributing

感谢参与。这个项目的核心质量目标是**可预测**：不同模型、不同用户、不同章节，应该走出同一套可靠流程。

## 仓库布局

- `skill/book-section-synthesis/`：真正安装到 agent 的运行文件（`SKILL.md`、`agents/`、`references/` 及其 `examples/`）。`~/.codex/skills/` 或 `~/.dsh/skills/` 下装的就是这一个目录。
- `.claude-plugin/`：把同一个目录登记成 Claude Code 插件与自建市场，路径指向 `skill/book-section-synthesis/`。
- 根目录的 `README.md`、`QUICK_PROMPTS.md`、`AGENTS.md`、`SECURITY.md`、`evals/`、`scripts/`、`.github/`：仓库文档、评测和开发工具，不会被安装进 skill 目录。

改动的同步关系（改 A 要一起改 B）写死在 [AGENTS.md](AGENTS.md) 里，先读那张表再动手。

## 行为变更

- 修改 `skill/book-section-synthesis/SKILL.md` 中会影响输出的规则时，必须在 `evals/fixtures/cases.md` 增加或更新一个对应用例。
- 如果改变了评分标准，同步更新 `evals/rubric.md`。
- 在 Pull Request 中说明：改了什么行为、为什么旧行为不够好、用哪个模型和版本验证过。
- 不要只改措辞而不说明行为影响。评审关注行为不变量，不关注句子是否“更漂亮”。

## 内容边界

- 不要提交受版权保护的教材、论文或试卷节选。
- 示例和评测材料使用合成文本或公共领域文本，并明确标注来源与授权。
- 不要加入真实用户的私人材料、未发表手稿或敏感数据。

## 写作约定

- `skill/book-section-synthesis/SKILL.md` 保持精简；类型细节、示例和错误对照放到 `skill/book-section-synthesis/references/`。
- 默认中文写作；术语保留原文，不强行给英文对应词。
- 规则要可检查：写“每节 250–350 字、主线 250–350 字”，不要写“篇幅适中”。
- 规则只判章，不判节；需要分节处理的规则，写成由档位和原文自身结构决定。
- 一个规则只在一个地方定义；引用时用链接，不要复制整段。
- 不要加入模型默认就会遵守的空泛建议。

## 本地检查

需要 Python 3.10+，不需要安装任何依赖：

```bash
python3 scripts/validate.py .
python3 scripts/check_links.py .
```

`validate.py` 检查结构、命名、版本一致性（`SKILL.md` / `CHANGELOG.md` / `plugin.json` / README badge 四处必须相等）、README 目录与正文标题一一对应、`SKILL.md` 引用的参考文件存在、交付门编号连续。`check_links.py` 检查本地 Markdown 链接的文件与锚点。两个脚本都不验证行为；行为验证按 [evals/README.md](evals/README.md) 进行。

改了行为还要在 PR 里说明版本档位（主／次／补丁），并让 `CHANGELOG.md` 的 `[Unreleased]` 段跟上——版本号对不上时 CI 会失败。

如果本机装了这些工具，可以额外跑（CI 不跑，避免在 CI 里安装第三方包）：

```bash
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Pull Request 清单

- [ ] 行为变更配有 fixture。
- [ ] 评分表已同步更新（如有需要）。
- [ ] `python scripts/validate.py .` 通过。
- [ ] `python scripts/check_links.py .` 通过。
- [ ] 没有提交受版权保护或私密的材料。
- [ ] 记录了验证所用的模型、版本和日期。
