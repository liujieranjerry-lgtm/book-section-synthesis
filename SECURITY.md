# 安全策略

## 报告问题

用 GitHub 的私密渠道：本仓库 **Security** 标签页 → **Report a vulnerability**（GitHub Security Advisories）。不要在公开 issue 里贴利用细节。

请说明：受影响的版本（`skill/book-section-synthesis/SKILL.md` 的 `metadata.version`）、复现所需的最小输入、你预期的行为和实际行为。

## 威胁模型

这个仓库分发的是**给 AI agent 读的指令文本**，不是可执行程序。因此威胁主要不在内存破坏那一类，而在这四处：

1. **指令注入**。`SKILL.md`、`references/`、`evals/` 里的文字最终会进入某个模型的上下文。一段看起来像规则的旁注，可能让下游 agent 去读不该读的文件、发不该发的请求。
2. **供应链**。CI 里多一个第三方 action、多一行 `pip install`，就多一条可以被劫持的路径；仓库本身要被改，最好也只能经由 PR。
3. **评测数据**。评测材料里放真实受版权原文，会让仓库成为侵权分发点，也会让「示例」和「用户材料」混在一起。
4. **用户材料外泄**。这个 skill 处理用户自己的教材与笔记，仓库不该出现任何用户原文。

## 为此做的控制

- CI 只运行 `scripts/` 下的标准库脚本，**不安装任何包**，没有 `requirements*.txt` 参与构建。
- 所有 GitHub Actions 固定到 commit SHA，不用浮动 tag；workflow 顶层 `permissions` 设为 `contents: read`，`checkout` 关掉 `persist-credentials`。
- 唯一的写权限在 `release` workflow 里，`contents: write` 只在 tag 推送时生效。
- 仓库内容全部是合成的示例材料；`references/examples/` 不来自任何真实教材。
- `SKILL.md` 不含可执行语句，也不含要求下游 agent 跳过用户确认的措辞。
- `main` 分支要求 PR、要求 `validate` 通过，管理员不豁免。

## 明确的非承诺

这个 skill 的产出**不是**对原书内容的权威解读，也不构成学术引用依据。它的准确性边界写在 `skill/book-section-synthesis/references/fidelity.md` 里：原文没写的推理会被标成 `*诠释*`，原书本身的错漏会被记进「存疑项」。不要把它当二手来源引用。

## 支持范围

只维护 `main` 上的最新版本和最新 Release。旧版本的问题请在最新版本上复现后再报告。
