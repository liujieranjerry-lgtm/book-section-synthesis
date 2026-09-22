# book-section-synthesis

把用户提供的教材或学术著作小节，重写成一份不照抄原文、不曲解原文、逻辑连贯的中文“脉络梳理”。

它不是摘要，不是逐句翻译，不是要点列表；它用自然段落重建这一小节的结构与推进，并明确区分原文主张、直接引用、隐含推理和外部补充。

## 硬性前提：必须提供原文

这个 skill 不会在缺少原文时凭书名、目录、模型记忆或二手介绍代写。如果没有原文，它会明确告诉用户无法做忠实梳理，并请用户提供原文。原文可以是：

- 直接粘贴的文字；
- PDF、Word、文本文件等可读取文件；
- 扫描件或页面照片（需要 OCR 或可辨认的清晰度）；
- 用户明确指认的可读取位置。

版本、译者、页码所属的版次也需要确认；不同版次的页码不能直接互推。

## 安装

### Codex

把 `book-section-synthesis/` 放进 `$CODEX_HOME/skills/`（未设置 `CODEX_HOME` 时通常是 `~/.codex/skills/`）。也可以用 skill-installer 从 GitHub 仓库安装。

### 其他支持 SKILL.md 的 agent

把整个目录复制到对应 agent 的 skills 目录即可。`agents/openai.yaml` 是 Codex 的界面元数据，其他宿主可以忽略；核心行为定义在 `SKILL.md` 和 `references/` 中。

## 使用

显式调用：

```text
$book-section-synthesis 梳理这一小节。原文如下：……
```

或者用自然语言：“使用 book-section-synthesis 梳理这一小节。原文如下：……”

或者让 agent 自动发现。skill 在开始前会确认：

1. 原文是否可得；
2. 版本和边界是否明确；
3. 你希望按什么知识基础解释（零基础 / 学过相关课程 / 本专业读者）。

如果原文缺失，它只会要求你提供原文，不会先写一段猜测。

## 三种模式

| 模式 | 用途 | 对外部知识的态度 |
|---|---|---|
| A. 忠实梳理（默认） | 重建原文结构与推进 | 不加入外部背景 |
| B. 讲解增强 | 在 A 的基础上补充背景、著作说明或思想谱系 | 外部内容必须标为“补充背景（非本小节原文）” |
| C. 文本审校 | 回答“这里是不是说错了”“前后是否矛盾” | 内部矛盾可直接判断；事实争议需要外部证据 |

## 输出约定

- 标准模式（默认）：4–8 个正文自然段。
- 紧凑模式：用户说“短一点”“不用太长”时，2–4 段。
- 详版：用户明确要求“详细/完整”，或原文包含多个必须展开的并列结构时可超过 8 段。
- 边界说明和补充说明不计入正文段落数。
- 默认使用自然段落；只有原文本身是分类或流程结构，且用户要求结构化输出时才使用少量列表。

## 质量保证

交付前必须通过以下检查：

- 没有原文时拒答并请求原文；
- 边界正确，没有混入下一小节；
- 原文主要结构推进全部进入梳理；
- 没有无来源主张，外部补充已标注；
- 隐含推理使用“可以理解为”等标记；
- 术语解释匹配用户的知识基础；
- 篇幅符合所选模式；
- 没有长段逐字复制，输出不能替代原文；
- 无法核实或无法辨认的内容单独说明。

详细规则见 [references/fidelity.md](references/fidelity.md)。

## 文本类型

这个 skill 不会把所有小节都当成论证文。它会先判断主导类型，再选择骨架：

- 论证型：问题 → 主张 → 理由 → 反驳/限定 → 结论
- 定义型：术语 → 界定 → 区分 → 例子 → 边界
- 分类型：分类目的 → 标准 → 类别 → 比较
- 过程型：目标 → 阶段 → 条件 → 结果
- 比较型：比较维度 → 异同 → 结论
- 机制型：现象 → 结构 → 机制 → 证据 → 限制
- 叙事型：背景 → 转折 → 结果 → 意义
- 描述/说明型：对象 → 特征 → 关系 → 例证

混合类型以主导类型为主；无法判断时按原文自身的标题和段落功能组织。详细规则见 [references/text-types.md](references/text-types.md)。

## 示例与评测

- 完整输入—输出示例：[references/examples/expected-output.md](references/examples/expected-output.md)
- 常见错误对照：[references/examples/anti-example.md](references/examples/anti-example.md)
- 评测用例：[evals/fixtures/cases.md](evals/fixtures/cases.md)
- 评分表：[evals/rubric.md](evals/rubric.md)

`scripts/validate.py` 只检查结构；行为需要通过前向测试验证。前向测试流程见 [evals/README.md](evals/README.md)。

## 本地开发

需要 Python 3.9+。先安装开发依赖，再运行结构校验：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py .
```

`requirements-dev.txt` 当前只声明 PyYAML；校验脚本在缺少它时会给出安装提示。

## 仓库结构

```text
book-section-synthesis/
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── text-types.md
│   ├── fidelity.md
│   └── examples/
├── evals/
│   ├── README.md
│   ├── rubric.md
│   └── fixtures/
├── scripts/
│   └── validate.py
├── requirements-dev.txt
└── .github/workflows/validate.yml
```

## 贡献

行为变更必须同时更新 `evals/fixtures/cases.md` 或新增 fixture，并说明评分影响。不要提交受版权保护的教材节选；示例使用合成材料或公共领域文本。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 版权与隐私

- 这个 skill 只做转述和结构重建，输出不能替代原文。
- 引用要简短、必要，并说明作用；不要大段逐字复制。
- 用户提供的教材、论文或未出版材料可能包含敏感信息；未经用户同意，不要上传到第三方服务。
- 开源仓库中的示例和评测材料应当是合成的或公共领域的。

## 已验证模型

发布前在这里记录实际跑过评测的模型、版本和日期：

```text
model:
version:
date:
rubric score:
notes:
```

## License

MIT，见 [LICENSE](LICENSE)。
