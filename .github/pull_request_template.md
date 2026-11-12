## What changed

<!-- 一句话说清改了什么规则或哪个文件。中文，动词开头。 -->

## Why

<!-- 旧的做法哪里不够好；这次改动让哪类失败不再发生。 -->

## Version

- [ ] 主版本（规则兼容性破坏：旧产出不再符合新规则）
- [ ] 次版本（新增能力或输出格式新增字段）
- [ ] 补丁版本（措辞、文档、脚本、CI）

`CHANGELOG.md` 的 `[Unreleased]` 段已同步。

## Behavior impact

- [ ] This PR changes observable skill behavior.
- [ ] I added or updated a fixture in `evals/fixtures/cases.md`.
- [ ] I updated `evals/rubric.md` if the scoring standard changed.
- [ ] I synced the files in the AGENTS.md 「改这里必须同步改那里」 table.
- [ ] I did not include copyrighted, private, or sensitive source material.

## Validation

- [ ] `python3 scripts/validate.py .` passes.
- [ ] `python3 scripts/check_links.py .` passes.
- [ ] I recorded the model, version, and date used for any behavioral check.

Model / version / date:

Notes for reviewers:
