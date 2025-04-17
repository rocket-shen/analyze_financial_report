# analyze_financial_report
依据A股上市公司行业分类，对财务报表["报告期", "ROE","净利率", "毛利率", "营收增长率", "净利润增长率", "资产负债率"]数据进行比对
# 起止日期：2018-03-31，2025-03-31
df_selected = df_selected.loc[(df_selected.index >= '2018-03-31') & (df_selected.index <= '2025-03-31')]
