import os
import glob
import pandas as pd

# 行业财务报表分析

pd.set_option('display.max_columns', 16)
# 设置每行显示的最大宽度
pd.set_option('display.width', 300)  # 可以根据需要调整宽度
pd.set_option('display.max_rows', 30)  # 显示的最大行数
# 设置 Pandas 显示选项，限制小数位数
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def analysis_data(f):
    df_income = pd.read_excel(f, sheet_name="income")
    df_balance = pd.read_excel(f, sheet_name="balance")
    df_cash_flow = pd.read_excel(f, sheet_name="cash_flow")


    df_analysis = pd.DataFrame()
    df_analysis["报告期"] = df_balance["报告期"]
    df_analysis["ROE"] = (df_income["归属于母公司股东的净利润"] / df_balance["归属于母公司股东权益合计"]) * 100
    df_analysis["净利率"] = (df_income["净利润"] / df_income["其中：营业收入"]) * 100
    df_analysis["毛利率"] = (1 - (df_income["其中：营业成本"] / df_income["其中：营业收入"])) * 100
    df_analysis["净利润增长率"] = ((df_income["归属于母公司股东的净利润"] / df_income["归属于母公司股东的净利润"].shift(-4)) - 1) * 100
    df_analysis["营收增长率"] = ((df_income["其中：营业收入"] / df_income["其中：营业收入"].shift(-4)) - 1) * 100
    df_analysis["资产负债率"] = df_balance["负债合计"] / df_balance["负债和股东权益总计"]
    df_selected = df_analysis[["报告期", "ROE","净利率", "毛利率", "营收增长率", "净利润增长率", "资产负债率"]]

    # 将 "报告期" 列设置为索引
    df_selected.set_index('报告期', inplace=True)
    # df_selected = df_selected.loc[(df_selected.index >= '2018-03-31') & (df_selected.index <= '2025-03-31')]
    # 行列翻转（让 "报告期" 变成列索引）
    result = df_selected.T

    # 对列名（报告期）进行排序，按日期从早到晚
    result.columns = pd.to_datetime(result.columns)  # 将报告期转换为日期格式
    result = result[sorted(result.columns)]  # 按日期排序
    result.columns = result.columns.strftime('%Y/%m/%d')  # 转换回字符串格式
    return result

directory = r"D:/雪球数据/行业财务报表"  # 注意：路径中的反斜杠需要转义，或者使用原始字符串（前面加r）

def list_industry(d):
    industries = [name for name in os.listdir(d) if os.path.isdir(os.path.join(d, name))]
    print("可用的行业名称：", industries)

list_industry(directory)

industry = input("请输入行业名称：")
dir_path = os.path.join(directory, industry)

# 检查目录是否存在
if not os.path.exists(dir_path):
    print(f"目录 {dir_path} 不存在，请检查输入的行业名称是否正确。")
else:
    file_list = glob.glob(os.path.join(dir_path, '*_财务报表.xlsx'))

    # 定义CSV文件的路径
    csv_file_path = os.path.join(directory, f"{industry}_analysis_results.csv")

    # 初始化一个空的DataFrame，用于存储所有文件的分析结果
    all_analysis = pd.DataFrame()

    for file in file_list:
        analiese_data = analysis_data(file)  # 调用分析函数
        file_name = '_'.join(os.path.basename(file).split('_')[:2])  # 提取文件名的前两部分并重新组合
        print("文件名:", file_name)
        print(analiese_data)

        # 将文件名作为一列添加到分析结果中，并确保它是第一列
        analiese_data.insert(0, '文件名', file_name)  # 使用 insert 方法将文件名列插入到第一列

        projects = ["ROE", "净利率",  "毛利率", "营收增长率", "净利润增长率", "资产负债率"]

        # 将项目名称作为一列插入到 DataFrame 的第二列位置
        analiese_data.insert(1, '项目', projects)  # 重复项目名称以匹配行数

        # 将当前文件的分析结果追加到总结果中
        all_analysis = pd.concat([all_analysis, analiese_data])

    # 将所有分析结果保存到一个CSV文件中
    all_analysis.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    print(f"所有文件的分析结果已保存到 {csv_file_path}")

