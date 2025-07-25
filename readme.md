# 财务数据分析系统代码解释

## 系统架构概述

这是一个基于雪球网数据的股票财务分析系统，包含以下5个核心模块：

## 1. stock_report.py - 个股财务数据获取
**功能**: 从雪球网获取单只股票的完整财务数据

### 主要流程
1. **用户输入**: 输入股票代码（如SH000001、SZ000002）
2. **数据获取**: 
   - 资产负债表数据
   - 利润表数据  
   - 现金流量表数据
   - 分红派息数据
   - 股东人数变化数据
3. **数据处理**: 
   - 时间戳转换为日期格式
   - 字段重命名（英文→中文）
   - 数据清洗和格式化
4. **数据保存**: 保存为Excel文件，包含5个工作表

### 关键技术点
```python
# 模拟浏览器访问，获取cookies
ses = requests.session()
res = ses.get(url='https://xueqiu.com/hq', headers=headers)
cookies = dict(ses.cookies)

# 时间戳转换
item['report_date'] = datetime.fromtimestamp(item['report_date'] / 1000).strftime('%Y-%m-%d')
```

## 2. indus_financial_report.py - 行业财务数据批量获取
**功能**: 批量获取某个行业内所有股票的财务数据

### 主要流程
1. **行业选择**: 用户选择市场（cn/hk/us）和行业名称
2. **股票列表**: 自动获取该行业内所有股票代码和名称
3. **批量下载**: 
   - 遍历行业内每只股票
   - 获取资产负债表、利润表、现金流量表、分红数据
   - 每只股票保存为独立的Excel文件
4. **文件组织**: 按行业名称创建文件夹，统一管理

### 核心函数
- `get_stock_dict()`: 获取行业内股票列表
- `fetch_data()`: 获取财务数据并格式化
- `main()`: 批量处理主函数

## 3. analysis_stock.py - 个股财务分析与可视化
**功能**: 对单只股票进行深度财务分析，生成可视化图表

### 分析指标
- **ROE (净资产收益率)**: 衡量股东权益回报率
- **毛利率**: 反映产品盈利能力
- **经营性资产**: 应收账款+预付款项+存货+合同资产
- **营收增长率**: 同比增长情况

### 可视化功能
```python
# 创建三个独立图表
plt.figure(num=f'{stock_symbol}_{stock_name}', figsize=(12, 6))
plt.plot(analyze_df["报告期"], analyze_df["ROE"], marker='o', label="ROE")
plt.plot(analyze_df["报告期"], analyze_df["毛利率"], marker='s', label="毛利率")
```

生成三类图表：
1. ROE和毛利率趋势对比
2. 营收增长率变化
3. 经营性资产规模变化

## 4. analysis_industry_report.py - 行业对比分析
**功能**: 对整个行业进行横向对比分析

### 分析维度
- **ROE**: 净资产收益率
- **净利率**: 净利润/营业收入
- **毛利率**: (营业收入-营业成本)/营业收入
- **营收增长率**: 同比增长率
- **净利润增长率**: 净利润同比增长率
- **资产负债率**: 负债/总资产

### 数据处理特色
```python
# 数据透视转换
df_selected.set_index('报告期', inplace=True)
result = df_selected.T  # 行列转置

# 时间序列排序
result.columns = pd.to_datetime(result.columns)
result = result[sorted(result.columns)]
```

### 输出格式
- 每个公司生成一个分析矩阵
- 所有公司数据合并到一个CSV文件
- 便于Excel中进一步分析和制图

## 5. financial.json - 数据字段映射配置
**功能**: 英文字段名与中文字段名的映射关系

### 配置结构
```json
{
    "balance1": {...},    // 资产负债表字段映射
    "income1": {...},     // 利润表字段映射
    "cash1": {...},       // 现金流量表字段映射
    "bonus": {...},       // 分红数据字段映射
    "holders": {...}      // 股东数据字段映射
}
```

## 系统使用流程

### 第一步：获取数据
```bash
# 获取单只股票数据
python xq_financial_excel.py
# 输入：SH600000

# 获取行业数据
python indus_financial_report.py  
# 输入：cn, 银行
```

### 第二步：分析数据
```bash
# 个股分析
python analysis_stock.py
# 输入：SH600000_浦发银行_财务数据

# 行业分析  
python analysis_industry_report.py
# 输入：银行
```

## 技术特点

### 1. 数据获取
- 自动处理雪球网的反爬机制
- 支持批量数据下载
- 时间戳自动转换
- 异常处理机制

### 2. 数据分析
- 关键财务指标计算
- 同比增长率分析
- 时间序列数据处理
- 数据透视和转换

### 3. 可视化
- matplotlib图表生成
- 中文字体支持
- 多子图展示
- 交互式图表

### 4. 文件管理
- 按行业分类存储
- Excel多工作表结构
- CSV格式导出
- 路径自动创建

## 扩展建议

1. **增加分析指标**: 现金流量比率、资产周转率等
2. **预警系统**: 财务指标异常自动提醒
3. **行业排名**: 各指标在行业中的排名
4. **趋势预测**: 基于历史数据的趋势分析
5. **报告生成**: 自动生成PDF分析报告

这套系统为投资分析提供了完整的数据获取、处理、分析工具链，可以大大提高财务分析的效率和准确性。