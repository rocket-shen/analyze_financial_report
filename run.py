import numpy as np
from xq_financial_excel import fetch_financial_data

symbol_list = ['SZ000895','SZ002157']
folder_path = f'D:/雪球数据/财务报表'
fetch_financial_data(symbol_list, folder_path)
print(f"程序执行完成")
