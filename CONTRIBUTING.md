# Contributing

感谢参与。这个项目的核心质量目标是**可预测**：不同模型、不同用户、不同小节，应该走出同一套可靠流程。

## 行为变更

- 修改 `SKILL.md` 中会影响输出的规则时，必须在 `evals/fixtures/cases.md` 增加或更新一个对应用例。
- 如果改变了评分标准，同步更新 `evals/rubric.md`。
- 在 Pull Request 中说明：改了什么行为、为什么旧行为不够好、用哪个模型和版本验证过。
- 不要只改措辞而不说明行为影响。评审关注行为不变量，不关注句子是否“更漂亮”。

## 内容边界

- 不要提交受版权保护的教材、论文或试卷节选。
- 示例和评测材料使用合成文本或公共领域文本，并明确标注来源与授权。
- 不要加入真实用户的私人材料、未发表手稿或敏感数据。

## 写作约定

- `SKILL.md` 保持精简；类型细节、示例和错误对照放到 `references/`。
- 默认中文写作；术语保留原文，不强行给英文对应词。
- 规则要可检查：写“4–8 个正文自然段”，不要写“篇幅适中”。
- 一个规则只在一个地方定义；引用时用链接，不要复制整段。
- 不要加入模型默认就会遵守的空泛建议。

## 本地检查

需要 Python 3.9+。先安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py .
```

这个脚本检查 frontmatter、命名和必需文件。它不能验证行为；行为验证按 [evals/README.md](evals/README.md) 进行。缺少 PyYAML 时，脚本会提示你运行上面的安装命令。

如果本机安装了 Codex skill-creator，也可以额外运行：

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Pull Request 清单

- [ ] 行为变更配有 fixture。
- [ ] 评分表已同步更新（如有需要）。
- [ ] `python scripts/validate.py .` 通过。
- [ ] 没有提交受版权保护或私密的材料。
- [ ] 记录了验证所用的模型、版本和日期。
