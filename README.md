# book-section-synthesis

> 把教材或学术著作中的指定小节，重写成一份忠于原文、逻辑连贯、可以直接放进笔记的中文“脉络梳理”。

![version](https://img.shields.io/badge/version-2.0.0-blue)
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
- [FAQ](#faq)
- [限制与路线图](#限制与路线图)
- [开发与贡献](#开发与贡献)
- [License](#license)

---

## 30 秒开始

### 1. 安装

Codex 推荐用官方 `skill-installer`：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo liujieranjerry-lgtm/book-section-synthesis \
  --path . \
  --name book-section-synthesis \
  --method git
```

安装后重启 Codex。如果仓库还是私有的，命令里需要 `--method git`；仓库公开后可以去掉这个参数。

### 2. 使用

```text
$book-section-synthesis 梳理 3.4 这一节，不要照本宣科。原文如下：
<粘贴原文>
```

它会先确认三件事：

1. 原文是否可得；
2. 版本和边界是否明确；
3. 你希望按什么知识基础解释：零基础 / 学过相关课程 / 本专业读者。

如果原文缺失，它只会要求你提供原文，不会先写一段猜测。

---

## 它解决什么问题

普通 AI 摘要常见三个问题：

- **压缩成要点，丢掉论证**：信息还在，但“为什么这样推进”没了。
- **没有原文也敢写**：看起来像在梳理，实际在凭记忆复述。
- **把作者的主张和模型的解释混在一起**：读者分不清哪句来自原文，哪句是推断。

这个 skill 的约束正好相反：

- 没有原文，不写；
- 先判断小节类型，再选择结构骨架；
- 原文主张、直接引用、隐含推理、外部补充分开；
- 默认输出 4–8 个自然段，不写成要点清单。

---

## 效果示例

> 示例是合成材料，不是任何真实教材的节选。完整输入和输出见 [references/examples/expected-output.md](references/examples/expected-output.md)。

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
> 这个主张的关键在于区分“指标”与“指标想代表的目标”。指标是一个可计算的代理量，目标才是组织真正关心的事情；当两者被混为一谈时，人们就可能去优化代理量，而不是目标本身。作者用医院考核急诊等待时间的例子说明这一点：等待时间只统计从挂号到见到医生的时长，于是让患者在救护车里等待就可以压低数字，但患者得到救治的时间并没有改善。可以理解为，这个例子之所以能支持作者的主张，是因为它展示了“指标下降”和“目标改善”可以分离；一旦分离，度量就不再是镜子，而变成了被考核者要应对的任务。

[查看完整输出（4–8 段 + 术语注 + 边界说明）→](references/examples/expected-output.md)

---

## 适合与不适合

**适合**：

- 正在读教材、教科书或学术著作，需要把某一节讲清楚的人；
- 需要把阅读内容整理成笔记、讲义或知识库条目的人；
- 需要区分“作者原话”和“我的理解”的人；
- 需要解释术语、引用、图表、公式或隐含推理的人；
- 需要回答“这一节到底怎么推进”的人。

**不适合**：

- 只想要一段摘要或要点列表；
- 想做整章总结或整本书总结；
- 想做文献综述、论文写作或逐句翻译；
- 没有原文，想让模型凭记忆复述；
- 想让模型在没有外部证据的情况下判定作者事实错误。

---

## 怎么用

**标准梳理**

```text
$book-section-synthesis 梳理 3.4 这一节，不要照本宣科。原文如下：
<粘贴原文>
```

**短版：2–4 段**

```text
$book-section-synthesis 梳理这一节，短一点，2–4 段。原文如下：
<粘贴原文>
```

**指定知识基础**

```text
$book-section-synthesis 我是零基础，请把关键术语解释清楚。原文如下：
<粘贴原文>
```

**检查译文或指代**

```text
$book-section-synthesis 这一节的“前者/后者”是不是指错了？原文如下：
<粘贴原文>
```

**直接插入笔记**

```text
$book-section-synthesis 输出可以直接插入 Obsidian 笔记的 Markdown 段落。原文如下：
<粘贴原文>
```

---

## 它会产出什么

默认输出：

1. **边界说明**（一句话，仅在需要时；不计入正文段落数）
2. **正文**：默认 4–8 个自然段
3. **术语注**（可选；术语较多或你要求时）
4. **补充说明**（可选；外部背景、未能核实的内容、原文本身的问题）

篇幅模式：

| 模式 | 段落数 | 何时使用 |
|---|---|---|
| 标准（默认） | 4–8 个正文自然段 | 一般请求 |
| 紧凑 | 2–4 段 | 你说“短一点”“不用太长” |
| 详版 | 可超过 8 段 | 你明确要求“详细/完整”，或原文包含多个必须展开的并列结构 |

三种模式：

| 模式 | 用途 | 对外部知识的态度 |
|---|---|---|
| A. 忠实梳理（默认） | 重建原文结构与推进 | 不加入外部背景 |
| B. 讲解增强 | 在 A 的基础上补充背景、著作说明或思想谱系 | 外部内容必须标为“补充背景（非本小节原文）” |
| C. 文本审校 | 回答“这里是不是说错了”“前后是否矛盾” | 内部矛盾可直接判断；事实争议需要外部证据 |

默认使用自然段落。只有原文本身是分类或流程结构，且你要求结构化输出时，才使用少量列表。

---

## 它怎么工作

1. **锁定原文**：确认原文可得、版本可定、边界可定；缺原文就请求原文。
2. **确认知识基础**：零基础 / 学过相关课程 / 本专业读者，用来调整术语解释密度。
3. **判定文本类型**：论证、定义、分类、过程、比较、机制、叙事、描述/说明；混合类型以主导类型为主。
4. **建立覆盖台账**：把原文的主要标题块或段落功能映射到输出环节，防止漏掉论证、图表、公式或注释。
5. **重建与保真**：区分原文主张、直接引用、隐含推理和外部补充；逻辑补全必须标为推断。
6. **交付门**：边界、覆盖、保真、术语、篇幅、版权全部通过后，才输出最终结果。

详细规则在 [SKILL.md](SKILL.md)；各文本类型的骨架和例子在 [references/text-types.md](references/text-types.md)，保真与引用规则在 [references/fidelity.md](references/fidelity.md)。

---

## 和普通摘要的区别

| | 普通摘要 | book-section-synthesis |
|---|---|---|
| 目标 | 压缩信息 | 重建结构与推进 |
| 原文 | 可能凭记忆 | 必须有原文 |
| 推断 | 不区分 | 明确标记 |
| 文本类型 | 一套模板 | 八类骨架 |
| 术语 | 可能跳过 | 按知识基础解释 |
| 输出 | 要点列表 | 4–8 段自然段落 |
| 事实争议 | 直接下结论 | 需要外部证据 |

---

## 安装

### 前置条件

- Codex App 或 Codex CLI，且支持 skills；
- Python 3.9+（用于官方 `skill-installer` 脚本）；
- 如果仓库还是私有的，需要先完成 GitHub 登录：

```bash
brew install gh
gh auth login
gh auth setup-git
```

非 macOS 请用对应包管理器安装 `gh`，例如 `sudo apt install gh` 或 `winget install GitHub.cli`。

### Codex 推荐：官方 skill-installer

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo liujieranjerry-lgtm/book-section-synthesis \
  --path . \
  --name book-section-synthesis \
  --method git
```

安装后重启 Codex。

### 跨 agent：npx skills

如果使用 Claude Code、Cursor、Cline 等支持 Agent Skills 的 agent，可以用 `npx skills`：

```bash
npx skills add liujieranjerry-lgtm/book-section-synthesis --global
```

需要 Node.js，并已配置 Git 凭据；私有仓库依赖你本机已有的 GitHub 登录。`--global` 表示安装到用户级 skills 目录；不加时安装到当前项目。

### 手动安装

Codex：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis"
mkdir -p "$(dirname "$SKILL_DIR")"
gh repo clone liujieranjerry-lgtm/book-section-synthesis "$SKILL_DIR"
```

仓库公开后，可以改用：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis"
mkdir -p "$(dirname "$SKILL_DIR")"
git clone https://github.com/liujieranjerry-lgtm/book-section-synthesis.git "$SKILL_DIR"
```

其他 agent：

```bash
SKILL_DIR="$HOME/.claude/skills/book-section-synthesis"
mkdir -p "$(dirname "$SKILL_DIR")"
gh repo clone liujieranjerry-lgtm/book-section-synthesis "$SKILL_DIR"
```

具体 skills 目录以对应 agent 的文档为准。

通用形式：

```bash
gh repo clone liujieranjerry-lgtm/book-section-synthesis "/path/to/your/skills/book-section-synthesis"
```

### 验证、更新、卸载

```bash
# 验证
test -f "${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis/SKILL.md" && echo "installed"

# 更新
git -C "${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis" pull --ff-only

# 卸载
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/book-section-synthesis"
```

`agents/openai.yaml` 是 Codex 的界面元数据，其他宿主可以忽略；核心行为定义在 `SKILL.md` 和 `references/` 中。

---

## 仓库结构

```text
book-section-synthesis/
├── SKILL.md                    # 模型执行入口：流程、模式、交付门
├── agents/
│   └── openai.yaml              # Codex UI 元数据（可选）
├── references/
│   ├── text-types.md            # 八类文本类型与骨架
│   ├── fidelity.md              # 四类陈述、引用规则、错误分类
│   └── examples/                # 合成示例、完整输出、反例
├── README.md                    # 人类阅读的仓库说明（本文件）
├── evals/                       # 行为评测用例与评分表
├── scripts/
│   └── validate.py              # 结构校验
├── requirements-dev.txt         # 开发依赖
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── .github/                     # CI 与 PR 模板
```

运行 skill 需要的是 `SKILL.md` 和 `references/`；`agents/openai.yaml` 是 Codex 的界面元数据。其余文件用于开发、评测和发布。

---

## FAQ

**没有原文可以用吗？**

不可以。它会先要求你提供原文，不会凭书名、目录或模型记忆代写。

**可以总结整章或整本书吗？**

不适合。这个 skill 只做指定小节的脉络梳理；整章或整本书请使用总结或阅读笔记类工具。

**扫描件或图片可以吗？**

可以，但需要 OCR 或足够清晰的图片。无法辨认的内容会标为 `[无法辨认]`，不会根据上下文补写。

**可以判断作者是不是说错了吗？**

- 内部矛盾、指代错误：可以依据本小节直接判断；
- 翻译或编辑问题：有原文时对照判断，没有原文时只能说明译文层面的异常；
- 事实争议：需要外部来源；没有外部来源时会写“需要外部核实”。

**会解释术语吗？**

会，解释密度按你提供的知识基础调整。默认按“能读懂该书、但不是该领域专家”处理。

**会大段复制原文吗？**

不会。引文简短、必要并标注；输出不能替代原文。

**支持 Claude Code 或其他 agent 吗？**

支持。把仓库克隆到对应 agent 的 skills 目录即可；`agents/openai.yaml` 是 Codex 的可选界面元数据。

**默认输出多长？**

标准模式 4–8 个正文自然段；说“短一点”时 2–4 段；明确要求详细时才超过 8 段。

**为什么安装后要重启 Codex？**

Codex 在启动时加载 skill 元数据；重启后才会发现新安装的 skill。

**需要联网吗？**

核心梳理只需要你提供的原文。只有当你要补充外部背景或核查事实时，才需要外部来源。

---

## 限制与路线图

**限制**：

- 不能替代外部事实核查；没有外部来源时会明确标注“需要外部核实”；
- OCR 和扫描件质量会影响覆盖范围；
- 行为会受模型版本影响，发布前应跑行为评测基线；
- 不适用于整章总结、文献综述、逐句翻译或论文写作；
- 不做法律、医学、金融等专业结论，只梳理原文。

**路线图**：

- 跑跨模型行为评测，补充 `evals/results/baseline.md`；
- 增加定义型、分类型、机制型、定理—证明型的评测 fixture；
- 增加 Claude Code 和其他宿主兼容性测试；
- 建立正式的版本 tag 与 release 流程。

---

## 开发与贡献

本地校验：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py .
```

行为变更必须同时更新 `evals/fixtures/cases.md` 或新增 fixture，并说明评分影响。不要提交受版权保护的教材节选；示例使用合成材料或公共领域文本。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

评测用例和评分表见 [evals/fixtures/cases.md](evals/fixtures/cases.md) 和 [evals/rubric.md](evals/rubric.md)。

---

## License

MIT License，见 [LICENSE](LICENSE)。
