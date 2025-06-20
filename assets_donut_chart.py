import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_donut_chart(values, categories, report_date, file_name, title=None, save_path=None):
    """
    绘制专业环形饼图，展示资产构成分析，包含引出线标注。
    
    参数：
        values (list): 资产值列表。
        categories (list): 资产类别名称列表。
        report_date (str): 报告期，如 '2023-12-31'。
        file_name (str): 数据来源文件名。
        title (str, optional): 图表标题，默认为 '{file_name}_{report_date} 主要资产构成分析'。
        save_path (str, optional): 保存图表的路径，默认为 None（不保存）。
    """
    # 设置专业配色方案（金融主题）
    colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
              '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC',
              '#8CD17D', '#499894', '#79706E', '#B2B2B2', '#D9D9D9']

    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建画布
    fig, ax = plt.subplots(figsize=(12, 10), facecolor='#f5f5f5')
    
    # 设置标题
    if title is None:
        title = f'{file_name}_{report_date} 主要资产构成分析'
    fig.suptitle(title, y=0.95, fontsize=16, fontweight='bold', color='#333333')

    # 绘制环形饼图
    wedges, texts, autotexts = ax.pie(
        values, 
        colors=colors,
        pctdistance=0.85,
        startangle=90,
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2),
        autopct=lambda p: f'{p:.1f}%\n({p*sum(values)/100:,.0f})' if p >= 5 else ''
    )

    # 添加中心空白圆（环形图效果）
    centre_circle = plt.Circle((0, 0), 0.5, color='white')
    ax.add_artist(centre_circle)

    # 添加图例（右侧垂直排列）
    legend_labels = [
        f"{name} {value:,.0f}元 ({value/sum(values):.1%})" 
        for name, value in zip(categories, values)
    ]
    legend = ax.legend(
        wedges,
        legend_labels,
        title="资产类别及金额",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        frameon=False,
        fontsize=10,
        handlelength=1.5,
        borderpad=1
    )
    legend.get_title().set_fontweight('bold')

    # 美化百分比文本
    plt.setp(autotexts, size=9, weight="bold", color='white')

    # 添加注释信息
    ax.text(0, -1.2, 
            f"数据来源: {file_name} | 总资产: {sum(values):,.0f}元",
            ha='center', va='center', fontsize=9, color='#666666')

    # 调整布局
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.75)

    # 保存图表（如果提供 save_path）
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # 显示图形
    plt.show()


folder_list = os.listdir('D:/雪球数据/个股财务报表')
print(folder_list)
folder_name = input('输入要查询的文件夹名称：')
folder_path = f'D:/雪球数据/个股财务报表/{folder_name}'
file_list = os.listdir(folder_path)
print(file_list)
file_name = folder_name + '_资产负债表.csv'  
df_balance = pd.read_csv(os.path.join(folder_path, file_name), encoding='utf-8')
print(df_balance.columns)
report_date = input('输入要查询的报告期：')
data = df_balance[df_balance['报告期']== report_date]
data = data.fillna(0)
assets = {
    "货币资金":data['货币资金'].values[0],
    "交易性金融资产":data['交易性金融资产'].values[0],
    "应收票据及应收账款":data['应收票据及应收账款'].values[0],
    "预付款项":data['预付款项'].values[0],
    "其他应收款":data['其他应收款'].values[0],
    "存货":data['存货'].values[0],
    "其他流动资产":data['其他流动资产'].values[0],
    "可供出售金融资产":data['可供出售金融资产'].values[0],
    "持有至到期投资":data['持有至到期投资'].values[0],
    "长期应收款":data['长期应收款'].values[0],
    "长期股权投资":data['长期股权投资'].values[0],
    "其他权益工具投资":data['其他权益工具投资'].values[0],
    "其他非流动金融资产":data['其他非流动金融资产'].values[0],
    "投资性房地产":data['投资性房地产'].values[0],
    "固定资产合计":data['固定资产合计'].values[0],
    "在建工程合计":data['在建工程合计'].values[0],  
    "无形资产":data['无形资产'].values[0],
    "开发支出":data['开发支出'].values[0],
    "商誉":data['商誉'].values[0],
    "长期待摊费用":data['长期待摊费用'].values[0],
    "递延所得税资产":data['递延所得税资产'].values[0],
    "其他非流动资产":data['其他非流动资产'].values[0],
    }

categories = list(assets.keys())
values = list(assets.values())
# 剔除占比小于 3% 的项目，汇总到“其他”

total_value = sum(values)
other_value = 0
filtered_categories = []
filtered_values = []

for cat, val in zip(categories, values):
    if val / total_value < 0.03:
        other_value += val
    else:
        filtered_categories.append(cat)
        filtered_values.append(val)

if other_value > 0:
    filtered_categories.append("其他")
    filtered_values.append(other_value)

chart_folder ='D:/雪球数据/个股财务报表/图表'
if not os.path.exists(chart_folder):
    os.makedirs(chart_folder)
save_path = f'{chart_folder}/{file_name.replace("_资产负债表.csv", f"{report_date}_donut_chart.png")}'

plot_donut_chart(filtered_values, filtered_categories, report_date, file_name, title=None, save_path=save_path)
                  