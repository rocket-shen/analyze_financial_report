import requests
import numpy as np
import pandas as pd
import time
import json
import os
from datetime import datetime

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Referer': 'https://xueqiu.com/hq'
}
url = 'https://xueqiu.com/hq'

url_balance = 'https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?'
url_income = 'https://stock.xueqiu.com/v5/stock/finance/cn/income.json?'
url_cash = 'https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?'
url_bonus = 'https://stock.xueqiu.com/v5/stock/f10/cn/bonus.json?'
url_holders = 'https://stock.xueqiu.com/v5/stock/f10/cn/holders.json?'

with open(r"./index/financial.json", "r", encoding="utf-8") as f:
    data_map = json.load(f)
# 选择 "资产负债表" 这个字典
balance_map = data_map.get("balance1", {})
income_map = data_map.get("income1", {})
cash_map = data_map.get("cash1", {})
bonus_map = data_map.get("bonus", {})
holders_map = data_map.get("holders", {})



def fetch_financial_data(symbol_list, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    stock_dict = np.load(r'./index/stock_dict.npy', allow_pickle=True).tolist()
    # 创建会话
    ses = requests.session()
    res = ses.get(url=url, headers=headers, timeout=10)
    cookies = dict(res.cookies)

    for symbol in symbol_list:
        stock_name = stock_dict.get(symbol, "未知证券名称")
        print(f'正在处理：{symbol} - {stock_name}')

        params1 = {'symbol': symbol, 'type': 'all', 'is_detail': 'true', 'count': 30,
                   'timestamp': int(round(time.time() * 1000))}
        params2 = {'symbol': symbol, 'size': '20', 'page': '1', 'extend': 'true'}

        try:
            balance = fetch_data(url_balance, cookies, params1)
            balance.rename(columns=balance_map, inplace=True)
            balance_data = balance.reindex(columns=balance_map.values())
            balance_data.to_csv(os.path.join(folder_path, f'{symbol}_{stock_name}_资产负债表.csv'), index=False)
            print(f"{symbol}_{stock_name}_资产负债表已保存到：{folder_path}文件夹中")

            income = fetch_data(url_income, cookies, params1)
            income.rename(columns=income_map, inplace=True)
            income_data = income.reindex(columns=income_map.values())
            income_data.to_csv(os.path.join(folder_path, f'{symbol}_{stock_name}_利润表.csv'), index=False)
            print(f"{symbol}_{stock_name}_利润表已保存到：{folder_path}文件夹中")

            cash = fetch_data(url_cash, cookies, params1)
            cash.rename(columns=cash_map, inplace=True)
            cash_data = cash.reindex(columns=cash_map.values())
            cash_data.to_csv(os.path.join(folder_path, f'{symbol}_{stock_name}_现金流量表.csv'), index=False)
            print(f"{symbol}_{stock_name}_现金流量表已保存到：{folder_path}文件夹中")

            bonus = fetch_bonus(url_bonus, cookies, params2)
            bonus.rename(columns=bonus_map, inplace=True)
            bonus_data = bonus.reindex(columns=bonus_map.values())
            bonus_data.to_csv(os.path.join(folder_path, f'{symbol}_{stock_name}_分红派息.csv'), index=False)
            print(f"{symbol}_{stock_name}_分红派息已保存到：{folder_path}文件夹中")

            holders = fetch_holders(url_holders, cookies, params2)
            holders.rename(columns=holders_map, inplace=True)
            holders_data = holders.reindex(columns=holders_map.values())
            holders_data.to_csv(os.path.join(folder_path, f'{symbol}_{stock_name}_股东户数.csv'), index=False)
            print(f"{symbol}_{stock_name}_股东户数已保存到：{folder_path}文件夹中")

        except Exception as e:
            print(f'获取{symbol}数据失败：{e}')

def fetch_data(data_url, cookies, params1):
    resp = requests.get(data_url,headers=headers,cookies=cookies,params=params1)
    data_list = resp.json()['data']['list']
    for item in data_list:
        if 'report_date' in item:
            item['report_date'] = datetime.fromtimestamp(item['report_date'] / 1000).strftime('%Y-%m-%d')
    df = pd.DataFrame(data_list)

    # 只取包含列表的字段的第一个值
    df = df.map(lambda x: x[0] if isinstance(x, list) else x)
    return df


def fetch_bonus(data_url, cookies, params2):
    response = requests.get(data_url,headers=headers,cookies=cookies, params=params2)
    data_list = response.json()['data']['items']
    for item in data_list:
        if item['ashare_ex_dividend_date'] is not None:
            item['ashare_ex_dividend_date'] = datetime.fromtimestamp(item['ashare_ex_dividend_date'] / 1000).strftime('%Y-%m-%d')
        else:
            item['dividend_date'] = None  # 或者设置为其他默认值，如空字符串 ''
        if item['dividend_date'] is not None:
            item['dividend_date'] = datetime.fromtimestamp(item['dividend_date'] / 1000).strftime('%Y-%m-%d')
        else:
            item['dividend_date'] = None  # 或者设置为其他默认值，如空字符串 ''
        if item['equity_date'] is not None:
            item['equity_date'] = datetime.fromtimestamp(item['equity_date'] / 1000).strftime('%Y-%m-%d')
        else:
            item['dividend_date'] = None  # 或者设置为其他默认值，如空字符串 ''
        if item['ex_dividend_date'] is not None:
            item['ex_dividend_date'] = datetime.fromtimestamp(item['ex_dividend_date'] / 1000).strftime('')
        else:
            item['dividend_date'] = None  # 或者设置为其他默认值，如空字符串 ''

    df = pd.DataFrame(data_list)
    return df


def fetch_holders(data_url, cookies, params2):
    response = requests.get(data_url, headers=headers, cookies=cookies, params=params2)
    data_list = response.json()['data']['items']
    for item in data_list:
        if item['timestamp'] is not None:
            item['timestamp'] = datetime.fromtimestamp(item['timestamp'] / 1000).strftime('%Y-%m-%d')
        else:
            item['timestamp'] = None

    df = pd.DataFrame(data_list)
    return df




# 请在运行前检查folder_path