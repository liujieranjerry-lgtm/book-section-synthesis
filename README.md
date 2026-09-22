# book-section-synthesis

> 把教材或学术著作中的指定小节，重写成一份忠于原文、逻辑连贯、可以直接放进笔记的中文“脉络梳理”。

![version](https://img.shields.io/badge/version-2.2.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-10a37f)
![language](https://img.shields.io/badge/language-中文-red)

它不是摘要，不是逐句翻译，不是要点列表，也不是整章总结。它用自然段落重建这一小节的结构与推进，并把原文主张、直接引用、隐含推理和外部补充分开。

**硬性要求：必须提供原文。** 没有原文时，它会先要求你提供原文，不会凭书名、目录或模型记忆代写。

## 目录

- [30 秒开始](#30-秒开始)
- [它解决什么问题](#它解决什么问题)
- [效果示例](#效果示例)
- [适合与不适合](#适合与不适合)
- [怎么用](#怎么用)
- [它会产出什么](#它会产出什么)
- [它怎么工作](#它怎么工作)
- [和普通摘要的区别](#和普通摘要的区别)
- [安装](#安装)
- [仓库结构](#仓库结构)
- [评测覆盖](#评测覆盖)
- [FAQ](#faq)
- [限制与路线图](#限制与路线图)
- [开发与贡献](#开发与贡献)
- [License](#license)

---

## 30 秒开始

### 1. 安装

Codex 里直接把目录链接交给 `skill-installer`：

```text
$skill-installer install https://github.com/liujieranjerry-lgtm/book-section-synthesis/tree/main/skill/book-section-synthesis
```

也可以直接运行安装脚本：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo liujieranjerry-lgtm/book-section-synthesis \
  --path skill/book-section-synthesis \
  --name book-section-synthesis \
  --method git
```

安装后重启 Codex。

### 2. 使用

```text
$book-section-synthesis 梳理 3.4 这一节，不要照本宣科。原文如下：
<粘贴原文>
```

它会先确认原文、版本/边界，以及你的知识基础（零基础 / 学过相关课程 / 本专业读者）。没有原文时，它不会先写猜测。

---

## 它解决什么问题

普通 AI 摘要常见三个问题：

- **压缩成要点，丢掉论证**：信息还在，但“为什么这样推进”没了。
- **没有原文也敢写**：看起来像在梳理，实际在凭记忆复述。
- **把作者的主张和模型的解释混在一起**：读者分不清哪句来自原文，哪句是推断。

这个 skill 的约束正好相反：没有原文不写；先判类型再选骨架；原文主张、引用、推断、外部补充分开；默认 4–8 个自然段。

---

## 效果示例

> 示例是合成材料，不是任何真实教材的节选。完整输入和输出见 [skill/book-section-synthesis/references/examples/expected-output.md](skill/book-section-synthesis/references/examples/expected-output.md)。

### 输入（节选）

<details>
<summary>3.4 度量为什么会改变被度量的对象</summary>

> 很多人把度量想成一面镜子：只要方法正确，它就能如实反映对象。但在组织环境中，度量往往会反过来改变对象。原因不在于测量仪器有误差，而在于人会根据度量调整行为。
>
> 假设一家医院用“急诊等待时间”考核科室。等待时间定义为患者从挂号到见到医生的时长。这个指标看起来直接对应“患者是否及时得到救治”。但科室很快发现，只要让患者在救护车里等待，就不计入统计；于是等待时间下降了，患者实际获得救治的时间却没有改善。

</details>

### 输出（节选）

> 这一节要回答的问题是：为什么度量会反过来改变被度量的对象。常见的想法是把度量看成一面看似中立的镜子，只要方法正确，数字就能如实反映对象；作者要反驳的正是这种想法。他的主张不是“测量有误差”，而是：在组织环境中，人会根据度量调整行为，因此度量会进入被度量的系统，改变它原本想反映的东西。
>
> 这个主张的关键在于区分“指标”与“指标想代表的目标”。指标是一个可计算的代理量，目标才是组织真正关心的事情；当两者被混为一谈时，人们就可能去优化代理量，而不是目标本身。

[查看完整输出 →](skill/book-section-synthesis/references/examples/expected-output.md)

---

## 适合与不适合

**适合**：

- 正在读教材、教科书或学术著作，需要把某一节讲清楚；
- 需要把阅读内容整理成笔记、讲义或知识库条目；
- 需要区分“作者原话”和“我的理解”；
- 需要解释术语、引用、图表、公式或隐含推理。

**不适合**：

- 只想要摘要或要点列表；
- 想做整章/整本书总结、文献综述、论文写作或逐句翻译；
- 没有原文，想让模型凭记忆复述；
- 想让模型在没有外部证据时判定作者事实错误。

---

## 怎么用

标准梳理：

```text
$book-section-synthesis 梳理 3.4 这一节，不要照本宣科。原文如下：
<粘贴原文>
```

短版：

```text
$book-section-synthesis 梳理这一节，短一点，2–4 段。原文如下：
<粘贴原文>
```

更多场景提示词见 [QUICK_PROMPTS.md](QUICK_PROMPTS.md)。

---

## 它会产出什么

默认输出：

1. **边界说明**（一句话，仅在需要时；不计入正文段落数）
2. **正文**：默认 4–8 个自然段
3. **术语注**（可选；术语较多或你要求时）
4. **补充说明**（可选：外部背景、未能核实的内容、原文本身的问题）

篇幅模式：

| 模式 | 段落数 | 何时使用 |
|---|---|---|
| 标准（默认） | 4–8 段 | 一般请求 |
| 紧凑 | 2–4 段 | 说“短一点”“不用太长” |
| 详版 | 可超过 8 段 | 明确要求“详细/完整”，或原文包含多个必须展开的并列结构 |

三种模式：

| 模式 | 用途 | 外部知识 |
|---|---|---|
| A. 忠实梳理（默认） | 重建原文结构与推进 | 不加入外部背景 |
| B. 讲解增强 | 补充背景、著作说明或思想谱系 | 必须标记“补充背景（非本小节原文）” |
| C. 文本审校 | 回答“是不是说错了” | 内部矛盾可直接判断；事实争议需要外部证据 |

需要固定结构的笔记时，使用 [skill/book-section-synthesis/templates/section-note.md](skill/book-section-synthesis/templates/section-note.md)。

---

## 它怎么工作

1. **锁定原文**：原文可得、版本可定、边界可定；缺原文就请求原文。
2. **确认知识基础**：零基础 / 学过相关课程 / 本专业读者。
3. **判定文本类型**：论证、定义、分类、过程、比较、机制、叙事、描述/说明。
4. **建立覆盖台账**：把原文的主要段落功能映射到输出环节。
5. **重建与保真**：区分原文主张、引用、隐含推理和外部补充。
6. **交付门**：边界、覆盖、保真、术语、篇幅、版权全部通过后输出。

详细规则见 [skill/book-section-synthesis/SKILL.md](skill/book-section-synthesis/SKILL.md)、[skill/book-section-synthesis/references/text-types.md](skill/book-section-synthesis/references/text-types.md) 和 [skill/book-section-synthesis/references/fidelity.md](skill/book-section-synthesis/references/fidelity.md)。

---

## 和普通摘要的区别

| | 普通摘要 | book-section-synthesis |
|---|---|---|
| 目标 | 压缩信息 | 重建结构与推进 |
| 原文 | 可能凭记忆 | 必须有原文 |
| 推断 | 不区分 | 明确标记 |
| 文本类型 | 一套模板 | 八类骨架 |
| 输出 | 要点列表 | 4–8 段自然段落 |
| 事实争议 | 直接下结论 | 需要外部证据 |

---

## 安装

官方 `skill-installer` 安装目录链接的方法见 [30 秒开始](#30-秒开始)。下面是其他安装方式。

### 跨 agent：npx skills

```bash
npx skills add https://github.com/liujieranjerry-lgtm/book-section-synthesis/tree/main/skill/book-section-synthesis --global
```

需要 Node.js，并已配置 Git 凭据。`--global` 安装到用户级 skills 目录；不加则安装到当前项目。

### 手动安装

手动安装需要把仓库里的 `skill/book-section-synthesis/` 复制到 agent 的 skills 目录。

```bash
TMP_DIR="$(mktemp -d)"
git clone --depth 1 https://github.com/liujieranjerry-lgtm/book-section-synthesis.git "$TMP_DIR/repo"
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R "$TMP_DIR/repo/skill/book-section-synthesis" "${CODEX_HOME:-$HOME/.codex}/skills/"
```

其他 agent 把目标路径换成对应的 skills 目录即可，例如 Claude Code 通常使用 `~/.claude/skills/`。`skill/book-section-synthesis/agents/openai.yaml` 是 Codex 的界面元数据，其他宿主可以忽略。

### 验证、更新、卸载

```bash
# 验证
test -f "${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis/SKILL.md" && echo "installed"

# 卸载
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis"
```

更新用 `npx skills` 最简单：

```bash
npx skills add https://github.com/liujieranjerry-lgtm/book-section-synthesis/tree/main/skill/book-section-synthesis --global
```

如果你用的是官方 `skill-installer`，先卸载再重新执行安装命令。

---

## 仓库结构

```text
book-section-synthesis/
├── README.md                    # 人类阅读的仓库说明（本文件）
├── QUICK_PROMPTS.md             # 可直接复制的提示词
├── evals/                       # 行为评测用例与评分表
├── scripts/
│   ├── validate.py              # 结构校验
│   └── check_links.py           # 本地 Markdown 链接检查
├── requirements-dev.txt         # 开发依赖
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .github/                     # CI、Dependabot 与 PR 模板
└── skill/
    └── book-section-synthesis/  # 真正安装到 Codex 的 skill
        ├── SKILL.md             # 模型执行入口
        ├── agents/
        │   └── openai.yaml      # Codex UI 元数据
        ├── references/
        │   ├── text-types.md    # 八类文本类型与骨架
        │   ├── fidelity.md      # 陈述分类、引用规则、Claim—Evidence—Verdict
        │   └── examples/        # 合成示例、完整输出、反例
        └── templates/
            └── section-note.md  # 固定笔记模板
```

真正安装到 Codex 的是 `skill/book-section-synthesis/`；模型实际读取的是其中的 `SKILL.md`、`references/` 和需要时的 `templates/section-note.md`。其余文件用于开发、评测和发布。

---

## 评测覆盖

行为用例见 [evals/fixtures/cases.md](evals/fixtures/cases.md)，评分标准见 [evals/rubric.md](evals/rubric.md)。

| 覆盖类别 | 代表性用例 |
|---|---|
| 输入门槛 | 有原文；只有书名没有原文 |
| 边界 | 边界清晰；标题层级歧义 |
| 文本类型 | 论证型；定义型；图表/表格承担论证 |
| 保真 | OCR 缺页；“前者/后者”指代错误 |
| 审校 | “是不是说错了”但没有外部证据 |
| 输出 | 标准 4–8 段；紧凑 2–4 段；可直接插入笔记 |
| 安全 | 原文中包含注入指令 |

当前状态：12 个行为用例已就绪，跨模型基线结果待补充。

---

## FAQ

**没有原文可以用吗？** 不可以。会先要求你提供原文，不会凭书名或记忆代写。

**可以总结整章或整本书吗？** 不适合。这个 skill 只做指定小节的脉络梳理。

**扫描件或图片可以吗？** 可以，但需要 OCR 或足够清晰；无法辨认处会标 `[无法辨认]`。

**可以判断作者是不是说错了吗？** 内部矛盾和指代错误可以直接判断；翻译问题需要原文对照；事实争议需要外部证据，否则写“需要外部核实”。

**支持 Claude Code 或其他 agent 吗？** 支持。把 `skill/book-section-synthesis/` 复制到对应 skills 目录即可；`skill/book-section-synthesis/agents/openai.yaml` 是 Codex 的可选元数据。

**默认输出多长？** 标准 4–8 段；说“短一点”时 2–4 段；明确要求详细时才超过 8 段。

**为什么安装命令是 Python，而不是 npm？** 因为 Codex 自带的官方安装器是一个 Python 脚本，负责把 skill 放进 `$CODEX_HOME/skills`；这不是在安装 Python 包。跨 agent 可以用 `npx skills add ...`，也可以直接 `git clone`。

---

## 限制与路线图

**限制**：

- 不能替代外部事实核查；
- OCR 和扫描件质量会影响覆盖；
- 不适用于整章总结、文献综述、逐句翻译或论文写作。

**路线图**：

- 跑跨模型行为评测，补充 `evals/results/baseline.md`；
- 增加定义型、分类型、机制型、定理—证明型 fixture；
- 增加 Claude Code 和其他宿主兼容性测试。

---

## 开发与贡献

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py .
python scripts/check_links.py .
```

CI 运行这两个脚本；它们只检查结构和链接，不验证行为。行为变更必须同步更新 `evals/fixtures/cases.md` 或新增 fixture。不要提交受版权保护的教材节选。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## License

MIT License，见 [LICENSE](LICENSE)。
