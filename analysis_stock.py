import os
import pandas as pd
import matplotlib.pyplot as plt

file_list = []
directory =  "D:/雪球数据/个股财务报表"
for item in os.listdir(directory):
    if item.endswith('.xlsx'):
        file_list.append(item)
print(file_list)

file_name = input('输入要查询的文件名称：')
stock_symbol = file_name.split('_')[0]
stock_name = file_name.split('_')[1]

print(stock_symbol,stock_name)
file_path = f"D:/雪球数据/个股财务报表/{file_name}.xlsx"  # 请确保文件路径正确
print(file_path)
df_income = pd.read_excel(file_path, sheet_name="income")
df_balance = pd.read_excel(file_path, sheet_name="balance")
# 处理df_中的所有空值
df_income.fillna(0, inplace=True)
df_balance.fillna(0, inplace=True)

analyze_df = pd.DataFrame()
analyze_df['报告期'] = df_balance['报告期']
analyze_df["ROE"] = (df_income["归属于母公司股东的净利润"] / df_balance["归属于母公司股东权益合计"])*100
analyze_df["毛利率"] = (1 - (df_income["其中：营业成本"] / df_income["其中：营业收入"]))*100
analyze_df['经营性资产(百万)'] = (df_balance['应收票据及应收账款'] + df_balance['预付款项'] + df_balance['存货'] + df_balance['合同资产'])/1000000
analyze_df["营收增长率"] = ((df_income["其中：营业收入"] / df_income["其中：营业收入"].shift(-4)) - 1) * 100

pd.set_option('display.max_columns', 26)
# 设置每行显示的最大宽度
pd.set_option('display.width', 200)  # 可以根据需要调整宽度
# 设置 Pandas 显示选项，限制小数位数
pd.set_option('display.float_format', lambda x: '%.2f' % x)
print(analyze_df.T)

# 设置中文字体（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制折线图
plt.figure(num= f'{stock_symbol}_{stock_name}',figsize=(12, 6))
# 绘制 ROE 折线图
plt.plot(analyze_df["报告期"], analyze_df["ROE"], marker='o', label="ROE")
# 绘制 毛利率 折线图
plt.plot(analyze_df["报告期"], analyze_df["毛利率"], marker='s', label="毛利率")
# 添加标题和标签
plt.title(f"{stock_symbol}_{stock_name}")
plt.xlabel("报告期")
plt.ylabel("比率")
plt.xticks(rotation=45)  # 旋转x轴标签
plt.tight_layout()
plt.legend()
# 显示网格
plt.grid(True)

# 绘制折线图
plt.figure(num= '营收增长率',figsize=(12, 6))
# 绘制 ROE 折线图
plt.plot(analyze_df["报告期"], analyze_df["营收增长率"], marker='o', label="营收增长率")
# 添加标题和标签
plt.title(f"{stock_symbol}_{stock_name}")
plt.xlabel("报告期")
plt.ylabel("百万")
plt.xticks(rotation=45)  # 旋转x轴标签
plt.tight_layout()
plt.legend()
# 显示网格
plt.grid(True)

# 绘制折线图
plt.figure(num= '经营性资产',figsize=(12, 6))
# 绘制 ROE 折线图
plt.plot(analyze_df["报告期"], analyze_df["经营性资产(百万)"], marker='o', label="经营性资产")
# 添加标题和标签
plt.title(f"{stock_symbol}_{stock_name}")
plt.xlabel("报告期")
plt.ylabel("百万")
plt.xticks(rotation=45)  # 旋转x轴标签
plt.tight_layout()
plt.legend()
# 显示网格
plt.grid(True)
# 显示图表
plt.show()

