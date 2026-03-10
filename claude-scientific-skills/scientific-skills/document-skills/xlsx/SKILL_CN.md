---
name: xlsx
description: 电子表格工具包（.xlsx/.csv）。使用公式/格式创建/编辑、分析数据、可视化、重新计算公式，用于电子表格处理和分析。
license: 专有。LICENSE.txt 包含完整条款
---

# 输出要求

## 所有 Excel 文件

### 零公式错误
- 每个 Excel 模型必须交付零公式错误（#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?）

### 保留现有模板（更新模板时）
- 研究并完全匹配现有格式、样式和约定，当修改文件时
- 永远不要对具有既定模式的文件强加标准化格式
- 现有模板约定始终覆盖这些指南

## 财务模型

### 颜色编码标准

除非用户或现有模板另有说明

#### 行业标准颜色约定
- **蓝色文本（RGB：0,0,255）**：硬编码输入和用户将为场景更改的数字
- **黑色文本（RGB：0,0,0）**：所有公式和计算
- **绿色文本（RGB：0,128,0）**：从同一工作簿内的其他工作表拉取的链接
- **红色文本（RGB：255,0,0）**：到其他文件的外部链接
- **黄色背景（RGB：255,255,0）**：需要注意的关键假设或需要更新的单元格

### 数字格式标准

#### 必需格式规则
- **年份**：格式化为文本字符串（例如，"2024" 而不是 "2,024"）
- **货币**：使用 $#,##0 格式；始终在标题中指定单位（"Revenue ($mm)"）
- **零**：使用数字格式将所有零设为"-"，包括百分比（例如，"$#,##0;($#,##0);-"）
- **百分比**：默认为 0.0% 格式（一位小数）
- **倍数**：格式化为 0.0x 用于估值倍数（EV/EBITDA、P/E）
- **负数**：使用括号 (123) 而不是减号 -123

### 公式构建规则

#### 假设放置
- 将所有假设（增长率、利润率、倍数等）放在单独的假设单元格中
- 在公式中使用单元格引用而不是硬编码值
- 示例：使用 =B5*(1+$B$6) 而不是 =B5*1.05

#### 公式错误预防
- 验证所有单元格引用都正确
- 检查范围中的差一错误
- 确保所有预测期间的一致公式
- 使用边缘情况测试（零值、负数）
- 验证没有意外的循环引用

#### 硬编码的文档要求
- 在单元格中注释或放在单元格旁边（如果在表格末尾）。格式："来源：[系统/文档]、[日期]、[具体参考]、[URL（如适用）]"
- 示例：
  - "来源：公司 10-K、FY2024、第 45 页、收入说明、[SEC EDGAR URL]"
  - "来源：公司 10-Q、2025 年 Q2、展品 99.1、[SEC EDGAR URL]"
  - "来源：Bloomberg 终端、2025 年 8 月 15 日、AAPL US 股票"
  - "来源：FactSet、2025 年 8 月 20 日、共识估计筛选"

# XLSX 创建、编辑和分析

## 概述

使用公式、格式和数据分析创建、编辑或分析 Excel 电子表格。将此技能应用于使用 openpyxl 和 pandas 的电子表格处理。重新计算公式并确保零错误以获得出版质量的输出。

## 使用科学图表进行视觉增强

**使用此技能创建文档时，始终考虑添加科学图表和示意图以增强视觉沟通。**

如果您的文档尚未包含图表或示意图：
- 使用 **scientific-schematics** 技能生成 AI 驱动的出版级图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善示意图

**对于新文档：** 默认应生成科学示意图，以可视化表示文本中描述的关键概念、工作流、架构或关系。

**如何生成示意图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI 将自动：
- 创建具有适当格式的出版级图像
- 通过多次迭代审查和完善
- 确保可访问性（色盲友好、高对比度）
- 将输出保存在 figures/ 目录中

**何时添加示意图：**
- 电子表格工作流图
- 数据处理管道图
- 公式计算流程图
- 财务模型结构图
- 数据分析流程图
- 任何受益于可视化的复杂概念

有关创建示意图的详细指导，请参阅 scientific-schematics 技能文档。

---

## 重要要求

**需要 LibreOffice 进行公式重新计算**：您可以假设已安装 LibreOffice，用于使用 `recalc.py` 脚本重新计算公式值。该脚本在首次运行时自动配置 LibreOffice。

## 读取和分析数据

### 使用 pandas 进行数据分析

对于数据分析、可视化和基本操作，使用 **pandas**，它提供了强大的数据处理能力：

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel('file.xlsx')  # 默认：第一个工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 所有工作表作为字典

# 分析
df.head()      # 预览数据
df.info()      # 列信息
df.describe()  # 统计

# 写入 Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 文件工作流

## 关键：使用公式，而不是硬编码值

**始终使用 Excel 公式，而不是在 Python 中计算值并硬编码它们。** 这确保电子表格保持动态和可更新。

### ❌ 错误 - 硬编码计算值
```python
# 错误：在 Python 中计算并硬编码结果
total = df['Sales'].sum()
sheet['B10'] = total  # 硬编码 5000

# 错误：在 Python 中计算增长率
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # 硬编码 0.15

# 错误：用于平均值的 Python 计算
avg = sum(values) / len(values)
sheet['D20'] = avg  # 硬编码 42.5
```

### ✅ 正确 - 使用 Excel 公式
```python
# 正确：让 Excel 计算总和
sheet['B10'] = '=SUM(B2:B9)'

# 正确：增长率作为 Excel 公式
sheet['C5'] = '=(C4-C2)/C2'

# 正确：使用 Excel 函数求平均值
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用于所有计算 - 总和、百分比、比率、差异等。电子表格应该能够在源数据更改时重新计算。

## 常见工作流

1. **选择工具**：pandas 用于数据，openpyxl 用于公式/格式
2. **创建/加载**：创建新工作簿或加载现有文件
3. **修改**：添加/编辑数据、公式和格式
4. **保存**：写入文件
5. **重新计算公式（如果使用公式则必须）**：使用 recalc.py 脚本
   ```bash
   python recalc.py output.xlsx
   ```
6. **验证并修复任何错误**：
   - 该脚本返回带有错误详细信息的 JSON
   - 如果 `status` 为 `errors_found`，请检查 `error_summary` 以获取特定错误类型和位置
   - 修复识别的错误并重新计算
   - 要修复的常见错误：
     - `#REF!`：无效的单元格引用
     - `#DIV/0!`：除以零
     - `#VALUE!`：公式中的错误数据类型
     - `#NAME?`：无法识别的公式名称

### 创建新的 Excel 文件

```python
# 使用 openpyxl 进行公式和格式化
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 添加数据
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# 添加公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式化
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# 列宽
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有的 Excel 文件

```python
# 使用 openpyxl 保留公式和格式
from openpyxl import load_workbook

# 加载现有文件
wb = load_workbook('existing.xlsx')
sheet = wb.active  # 或 wb['SheetName'] 用于特定工作表

# 使用多个工作表
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"工作表：{sheet_name}")

# 修改单元格
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # 在位置 2 插入行
sheet.delete_cols(3)  # 删除第 3 列

# 添加新工作表
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新计算公式

由 openpyxl 创建或修改的 Excel 文件包含作为字符串但未计算值的公式。使用提供的 `recalc.py` 脚本重新计算公式：

```bash
python recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python recalc.py output.xlsx 30
```

该脚本：
- 在首次运行时自动设置 LibreOffice 宏
- 重新计算所有工作表中的所有公式
- 扫描所有单元格以查找 Excel 错误（#REF!、#DIV/0! 等）
- 返回带有详细错误位置和计数的 JSON
- 在 Linux 和 macOS 上都有效

## 公式验证清单

快速检查以确保公式正确工作：

### 基本验证
- [ ] **测试 2-3 个样本引用**：在构建完整模型之前验证它们拉取正确的值
- [ ] **列映射**：确认 Excel 列匹配（例如，列 64 = BL，而不是 BK）
- [ ] **行偏移**：记住 Excel 行是 1 索引的（DataFrame 行 5 = Excel 行 6）

### 常见陷阱
- [ ] **NaN 处理**：使用 `pd.notna()` 检查空值
- [ ] **最右列**：FY 数据通常在第 50+ 列中
- [ ] **多个匹配**：搜索所有出现，而不仅仅是第一个
- [ ] **除以零**：在公式中使用 `/` 之前检查分母（#DIV/0!）
- [ ] **错误引用**：验证所有单元格引用都指向预期的单元格（#REF!）
- [ ] **跨工作表引用**：使用正确的格式（Sheet1!A1）链接工作表

### 公式测试策略
- [ ] **从小开始**：在广泛应用之前在 2-3 个单元格上测试公式
- [ ] **验证依赖关系**：检查公式中引用的所有单元格都存在
- [ ] **测试边缘情况**：包括零、负数和非常大的值

### 解释 recalc.py 输出

该脚本返回带有错误详细信息的 JSON：
```json
{
  "status": "success",           // 或 "errors_found"
  "total_errors": 0,              // 总错误计数
  "total_formulas": 42,           // 文件中的公式数量
  "error_summary": {              // 仅在发现错误时存在
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库选择
- **pandas**：最适合数据分析、批量操作和简单数据导出
- **openpyxl**：最适合复杂格式化、公式和 Excel 特定功能

### 使用 openpyxl
- 单元格索引是基于 1 的（row=1、column=1 指的是单元格 A1）
- 使用 `data_only=True` 读取计算值：`load_workbook('file.xlsx', data_only=True)`
- **警告**：如果使用 `data_only=True` 打开并保存，公式将被值替换并永久丢失
- 对于大文件：使用 `read_only=True` 进行读取或 `write_only=True` 进行写入
- 公式被保留但不被评估 - 使用 recalc.py 更新值

### 使用 pandas
- 指定数据类型以避免推断问题：`pd.read_excel('file.xlsx', dtype={'id': str})`
- 对于大文件，读取特定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正确处理日期：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格指南

**重要**：为 Excel 操作生成 Python 代码时：
- 编写最少、简洁的 Python 代码，没有不必要的注释
- 避免冗长的变量名和冗余操作
- 避免不必要的打印语句

**对于 Excel 文件本身**：
- 为复杂公式或重要假设向单元格添加注释
- 为硬编码值记录数据来源
- 为关键计算和模型部分添加注释
