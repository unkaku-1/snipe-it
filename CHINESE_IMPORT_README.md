# Snipe-IT 中文字段 CSV 导入解决方案

本仓库提供了完整的 Snipe-IT 中文字段 CSV 导入解决方案，解决中文字符编码和字段映射问题。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install chardet
```

### 2. 转换 CSV 文件
```bash
# 修复编码问题
python encoding-converter.py fix input.csv temp.csv

# 转换字段名称
python csv-field-converter.py convert temp.csv output.csv --type assets
```

### 3. 导入到 Snipe-IT
使用转换后的 CSV 文件进行导入。

## 📁 文件说明

- `SNIPE_IT_CHINESE_IMPORT_GUIDE.md` - 详细使用指南
- `snipe-it-chinese-import-analysis.md` - 问题分析报告
- `chinese-field-mapping.json` - 字段映射配置
- `csv-field-converter.py` - CSV 字段转换工具
- `encoding-converter.py` - 文件编码转换工具
- `batch-convert.py` - 批量转换工具
- `sample-templates/` - 示例模板文件

## 🛠️ 工具使用

### 字段转换工具
```bash
# 转换字段名称
python csv-field-converter.py convert input.csv output.csv

# 生成模板
python csv-field-converter.py template assets template.csv

# 验证文件
python csv-field-converter.py validate input.csv
```

### 编码转换工具
```bash
# 自动修复编码
python encoding-converter.py fix input.csv output.csv

# 检测编码
python encoding-converter.py detect input.csv

# 验证 UTF-8
python encoding-converter.py validate input.csv
```

### 批量转换工具
```bash
# 批量处理目录中的所有 CSV 文件
python batch-convert.py process input_dir output_dir --type assets
```

## 📋 支持的字段映射

### 资产字段
- 资产名称 → Item Name
- 公司 → Company
- 类别 → Category
- 位置 → Location
- 购买日期 → Purchase Date
- 购买成本 → Purchase Cost
- 型号名称 → Model Name
- 制造商 → Manufacturer
- 序列号 → Serial
- 资产标签 → Asset Tag
- 备注 → Notes
- 状态 → Status

### 用户字段
- 姓名 → Full Name
- 邮箱 → Email
- 用户名 → Username
- 激活 → Active
- 部门 → Department
- 职位 → Job Title
- 电话 → Phone

## 🔧 故障排除

常见问题及解决方案请参考 `SNIPE_IT_CHINESE_IMPORT_GUIDE.md` 文件。

## 📞 技术支持

如有问题，请查看详细指南或提交 Issue。

---

**作者**: Manus AI  
**版本**: 1.0  
**日期**: 2025-07-23
