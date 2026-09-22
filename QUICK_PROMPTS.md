# 快速提示词

把下面的提示词复制给 Codex，替换书名、章节和原文即可。所有场景都要求提供原文；没有原文时，skill 会先向你索要原文。

## 1. 标准梳理（默认 4–8 段）

```text
$book-section-synthesis 梳理 3.4 这一节，不要照本宣科。原文如下：
<粘贴原文>
```

## 2. 短版（2–4 段）

```text
$book-section-synthesis 梳理这一节，短一点，2–4 段。原文如下：
<粘贴原文>
```

## 3. 零基础解释

```text
$book-section-synthesis 我是零基础，请把关键术语解释清楚，避免未定义的行话。原文如下：
<粘贴原文>
```

## 4. 本专业读者（不解释常识术语）

```text
$book-section-synthesis 我是本专业读者，不用解释基础概念，重点写论证关系、分歧和限制。原文如下：
<粘贴原文>
```

## 5. 检查指代或译文问题

```text
$book-section-synthesis 这一节的“前者/后者”是不是指错了？请指出并给出可读的修正。原文如下：
<粘贴原文>
```

## 6. 事实争议（要求外部核实）

```text
$book-section-synthesis 这一节的事实判断有没有问题？没有外部证据时请写“需要外部核实”，不要凭记忆下结论。原文如下：
<粘贴原文>
```

## 7. 直接插入 Obsidian 笔记

```text
$book-section-synthesis 输出可以直接插入 Obsidian 笔记的 Markdown 段落，不加对话性前言或后记。原文如下：
<粘贴原文>
```

## 8. 固定结构笔记（使用模板）

```text
$book-section-synthesis 按 templates/section-note.md 的结构输出：边界说明、4–8 段正文、术语注、保真说明。原文如下：
<粘贴原文>
```

## 9. 保真审计

```text
$book-section-synthesis 请梳理这一节，并单独列出：外部补充、无法核实的内容、原文内部的矛盾或指代问题。原文如下：
<粘贴原文>
```

## 10. 相邻小节的衔接

```text
$book-section-synthesis 这一节和上一节的衔接是什么？只梳理指定小节；需要借用上一节的定义时请说明来源。本节原文如下：
<粘贴原文>
```
