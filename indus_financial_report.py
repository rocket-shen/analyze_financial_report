import parsel
import json
import os.path
import requests
import pandas as pd
from datetime import datetime
import time
import numpy as np


def get_cookies():
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    ses = requests.session()
    ses.get('https://xueqiu.com/hq', headers=headers, timeout=10)
    cookies = dict(ses.cookies)
    return headers, cookies


def get_requests(url, params):
    headers, cookies = get_cookies()
    response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
    return response


def get_stock_dict(m,c):
    params = {
        'page': 1,
        'size': 90,
        'order': 'desc',
        'order_by': 'market_capital',
        'market': m,
        'ind_code': c
    }
    response = get_requests('https://stock.xueqiu.com/v5/stock/screener/quote/list.json?', params=params)
    stock_list = response.json()['data']['list']
    print(len(stock_list))
    stock_dict = {n['symbol']: n['name'] for n in stock_list}
    return stock_dict


def fetch_data(data_url,param):
    response= get_requests(data_url,params=param)
    data_list = response.json()['data']['list']
    for item in data_list:
        if 'report_date' in item:
            item['report_date'] = datetime.fromtimestamp(item['report_date'] / 1000).strftime('%Y-%m-%d')
    df = pd.DataFrame(data_list)
    # 只取包含列表的字段的第一个值
    df = df.map(lambda x: x[0] if isinstance(x, list) else x)
    return df


def fetch_bonus(url,param):
    response = get_requests(url, params=param)
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
            item['ex_dividend_date'] = datetime.fromtimestamp(item['ex_dividend_date'] / 1000).strftime('%Y-%m-%d')
        else:
            item['dividend_date'] = None  # 或者设置为其他默认值，如空字符串 ''

    df = pd.DataFrame(data_list)
    return df


def main(m,c,p):
    stock_dict = get_stock_dict(m,c)
    symbol_list = list(stock_dict.keys())
    stock_list = list(stock_dict.values())
    with open("C:/myWork/PY/financial.json", "r", encoding="utf-8") as f:
        data_map = json.load(f)
    # 选择 "资产负债表" 这个字典
    balance_map = data_map.get("balance1", {})
    income_map = data_map.get("income1", {})
    cash_map = data_map.get("cash1", {})
    bonus_map = data_map.get("bonus", {})
    for symbol, stock in zip(symbol_list, stock_list):
        stock_name = stock.replace('*', '')
        file_name = symbol + '_' + stock_name + '_财务报表.xlsx'
        file_path = os.path.join(p, file_name)
        params = {'symbol': symbol, 'type': 'all', 'is_detail': 'true', 'count': '41',
                  'timestamp': int(round(time.time() * 1000))}
        balance = fetch_data('https://stock.xueqiu.com/v5/stock/finance/cn/balance.json?',params)
        balance.rename(columns=balance_map, inplace=True)
        balance_data = balance.reindex(columns=balance_map.values())
        income = fetch_data('https://stock.xueqiu.com/v5/stock/finance/cn/income.json?',params)
        income.rename(columns=income_map, inplace=True)
        income_data = income.reindex(columns=income_map.values())
        cash = fetch_data('https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json?',params)
        cash.rename(columns=cash_map, inplace=True)
        cash_data = cash.reindex(columns=cash_map.values())
        bonus_params = {'symbol': symbol, 'size': '20', 'page': '1', 'extend': 'true'}
        bonus = fetch_bonus('https://stock.xueqiu.com/v5/stock/f10/cn/bonus.json?',bonus_params)
        bonus.rename(columns=bonus_map, inplace=True)
        bonus_data = bonus.reindex(columns=bonus_map.values())
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            balance_data.to_excel(writer, sheet_name='balance', index=False)
            income_data.to_excel(writer, sheet_name='income', index=False)
            cash_data.to_excel(writer, sheet_name='cash_flow', index=False)
            bonus_data.to_excel(writer, sheet_name='bonus', index=False)


market = input("请输入需要查询的市场（cn/hk/us）：")
indus_dict = np.load(r'D:\雪球数据\indus_dict.npy', allow_pickle=True).tolist()
print(indus_dict)

industry = input('请输入需要查询的行业名称：')
code = indus_dict[industry]
folder_path = f'D:/雪球数据/行业财务报表/{industry}'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
main(market,code,folder_path)


