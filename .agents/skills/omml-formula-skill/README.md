# OMML Formula Skill 🧮 | OMML 公式 Skill

[English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

An Agent Skill that converts LaTeX formulas into **editable Office Math (OMML)** for Word / PowerPoint — not screenshots or garbled text.

### When to use

- Convert LaTeX formulas to native Word/PowerPoint equations
- Make formulas editable (not image-based) in Office documents
- Migrate LaTeX-rendered formulas into Office Math format

---

<a id="中文"></a>
## 中文

# OMML Formula Skill 🧮

> 把 LaTeX 公式变成 **Word / PowerPoint 里可编辑的 Office Math**，而不是截图或乱码。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![Pandoc](https://img.shields.io/badge/Requires-Pandoc-orange)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)
[![Agent Skill](https://img.shields.io/badge/AI%20Agent-Skill-purple)]()

---

## 它解决什么问题？

用 python-docx / python-pptx / PptxGenJS 生成带公式的 Word 或 PPT 时，**公式经常显示为空白**。原因是 Office 不会渲染所有"合法"的 XML——PowerPoint 尤其会忽略直接插入的裸 `<m:oMath>` 节点。

```
❌ 直接插入裸 OMML → PowerPoint 显示空白
✅ 占位符先行 → 后处理注入正确的数学上下文 → 公式可见且可编辑
```

这个 skill 采用 **placeholder-first 工作流**解决这个根本问题：

```text
LaTeX → Pandoc 临时 DOCX → 提取 OMML → 替换 {{OMML:id}} 占位符 → 验证
```

## 核心能力

| 能力 | 脚本 | 说明 |
|------|------|------|
| **LaTeX → OMML 转换** | `latex_to_omml.py` | 委托 Pandoc 解析 LaTeX 数学，提取 Office Math XML |
| **Word 公式注入** | `insert_word_omml.py` | DOCX 占位符 → 可编辑 Word 公式（block 用 `m:oMathPara`，inline 用 `m:oMath`） |
| **PowerPoint 公式注入** | `inject_ppt_omml.py` | PPTX 占位符 → 可编辑 PPT 公式（`a14:m > m:oMathPara` 包装） |
| **结构验证** | `validate_office_math.py` | 检查残留占位符、OMML 计数、PPT 错误上下文（`--strict --json`） |
| **环境检查** | `preflight_check.py` | 验证 Pandoc + Python 依赖是否就绪 |
| **PNG 回退** | `render_latex_assets.py` | 当 OMML 渲染不可靠时，生成图片作为显示备用 |
| **OMML 提取** | `extract_office_math.py` | 从已有 Office 文件提取 OMML 片段用于调试 |

## 快速开始

### 1. 安装依赖

```bash
# 需要 Pandoc（LaTeX 数学解析）
pandoc --version

# Python 依赖
pip install -r requirements.txt

# 可选：PNG 回退渲染
pip install -r requirements-optional.txt

# 环境检查
python scripts/preflight_check.py
```

### 2. 准备公式定义

创建 `formulas.json`（参考 [`examples/formulas.json`](./examples/formulas.json)）：

```json
{
  "macros": { "\\E": "\\mathbb{E}", "\\R": "\\mathbb{R}" },
  "formulas": [
    {
      "id": "routing_weight",
      "latex": "\\alpha_{i,m}=\\frac{\\exp(z_{i,m})}{\\sum_{m'}\\exp(z_{i,m'})}",
      "display": true,
      "mode": "omml",
      "alt": "softmax routing weight over modalities"
    }
  ]
}
```

### 3. 在文档中放占位符

```text
损失函数为 {{OMML:bce_loss}}。

{{OMML:eq1}}
```

### 4. 注入公式

**Word：**

```bash
python scripts/insert_word_omml.py \
  --input input.docx \
  --formulas formulas.json \
  --output output.docx
```

**PowerPoint：**

```bash
python scripts/inject_ppt_omml.py \
  --input input.pptx \
  --formulas formulas.json \
  --output output.pptx
```

### 5. 验证

```bash
python scripts/validate_office_math.py output.docx --strict
python scripts/validate_office_math.py output.pptx --strict --json
```

> ⚠️ 结构验证 ≠ GUI 渲染验证。重要文件请在 Microsoft Word/PowerPoint 中打开确认。

## Agent 友好设计

这个 skill 专为 AI Agent 调用优化：

- **`--dry-run --json`**：Agent 先预览变更再决定执行
- **按需转换**：只转换目标文件中实际被引用的公式，避免无关公式报错中断
- **`--strict`**：严格模式让验证失败有明确返回码
- **`--scope all`**：PPT 可扫描 notes/masters/layouts 中的占位符

```bash
# Agent 典型调用序列
python scripts/preflight_check.py --json                          # 1. 检查环境
python scripts/insert_word_omml.py ... --dry-run --json           # 2. 预览
python scripts/insert_word_omml.py ...                            # 3. 执行
python scripts/validate_office_math.py output.docx --strict --json  # 4. 验证
```

完整 Agent 集成指南见 [`references/agent-integration.md`](./references/agent-integration.md)。

## 公式路由策略

不是所有 LaTeX 都适合转 OMML。skill 内置智能路由：

| 场景 | 策略 |
|------|------|
| 简单行内/块公式 | ✅ OMML |
| 分数/求和/积分 | ✅ OMML，然后验证 |
| 矩阵 | ✅ OMML，需在 Office 中检查 |
| 自定义宏 | 先在 `formulas.json` 的 `macros` 中展开 |
| TikZ/minipage/文字密集块 | 🖼️ PNG/SVG 回退，不可编辑 |
| PPT 渲染不确定 | 保留 OMML（可编辑优先）或用图片（显示优先） |

## 为什么不用 python-pptx 直接操作？

`python-pptx` 能创建文本框和形状，但**没有一等公民的 Office Math API**。直接追加裸 OMML 可能产出合法 XML，但 PowerPoint 仍然忽略它。更安全的做法是：先创建正常的 PPT，再后处理修补 OOXML。

技术细节见 [`references/implementation-notes.md`](./references/implementation-notes.md)。

## 命令速查

```bash
# 环境检查
python scripts/preflight_check.py

# Word 注入
python scripts/insert_word_omml.py --input in.docx --formulas f.json --output out.docx

# PPT 注入
python scripts/inject_ppt_omml.py --input in.pptx --formulas f.json --output out.pptx --scope all

# 验证
python scripts/validate_office_math.py out.pptx --strict --json

# 调试提取
python scripts/extract_office_math.py out.docx

# PNG 回退
python scripts/render_latex_assets.py --formulas f.json --out-dir assets/

# 端到端测试
python scripts/smoke_test.py
```

## 文档索引

| 文档 | 内容 |
|------|------|
| [`SKILL.md`](./SKILL.md) | Agent 技能定义、触发条件、工作流 |
| [`references/workflow.md`](./references/workflow.md) | 详细用户工作流 |
| [`references/implementation-notes.md`](./references/implementation-notes.md) | OOXML 实现细节 |
| [`references/troubleshooting.md`](./references/troubleshooting.md) | 常见问题排查 |
| [`references/agent-integration.md`](./references/agent-integration.md) | Agent 调用方指南 |
| [`references/skill-quality-review.md`](./references/skill-quality-review.md) | 质量自评 |
| [`examples/formulas.json`](./examples/formulas.json) | 公式 JSON 示例 |
| [`CHANGELOG.md`](./CHANGELOG.md) | 版本更新记录 |

## 使用建议

| 场景 | 建议 |
|------|------|
| 学术报告 / 论文转 Word | ✅ 先生成带占位符的 DOCX，再注入 OMML |
| 教学 PPT / 课程演示 | ✅ 一个占位符对应一个公式，避免同段落混排 |
| 混合样式文字 + 公式 | ⚠️ 注入器会重建段落，建议公式独占段落/文本框 |
| LibreOffice / WPS 用户 | ⚠️ OMML 兼容性与 MS Office 不同，最终请在 MS Office 验证 |
| 复杂 TikZ / 排版 | ❌ 不适合 OMML，使用 PNG 回退 |

## 技术约束

- **Pandoc 依赖**：LaTeX 数学解析委托给 Pandoc，必须安装并可在 PATH 中使用
- **Microsoft Office**：结构验证无法证明 GUI 渲染结果，重要文件需在 MS Office 中打开确认
- **段落重建**：注入器会重建受影响段落，保留段落属性 + 首个 run 样式，但不保留所有局部 run 样式
- **Python 3.10+**：使用 `|` 类型联合语法

## License

[MIT](./LICENSE)
