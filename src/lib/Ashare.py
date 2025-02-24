#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ashare - A股票行情数据双核心版
项目地址: https://github.com/mpquant/Ashare

本模块提供了从腾讯和新浪两个数据源获取A股股票行情数据的功能。
支持日线、周线、月线以及分钟级别的数据获取。
"""

import json
import requests
import datetime
import pandas as pd

def get_price_day_tx(code, end_date='', count=10, frequency='1d'):
    """从腾讯接口获取日线数据
    
    Args:
        code: 股票代码
        end_date: 结束日期，默认为空（当前日期）
        count: 获取数据的条数
        frequency: 数据周期，支持 '1d'（日线）, '1w'（周线）, '1M'（月线）
    
    Returns:
        DataFrame包含columns: ['time', 'open', 'close', 'high', 'low', 'volume']
    """
    # 确定数据周期单位，进行单位转换
    unit = 'week' if frequency in '1w' else 'month' if frequency in '1M' else 'day'
    
    # 处理结束日期
    if end_date:
        end_date = end_date.strftime('%Y-%m-%d') if isinstance(end_date, datetime.date) else end_date.split(' ')[0]
    end_date = '' if end_date == datetime.datetime.now().strftime('%Y-%m-%d') else end_date
    
    # 构建请求URL并获取数据
    URL = f'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code},{unit},,{end_date},{count},qfq'
    response = json.loads(requests.get(URL).content)
    
    # 解析数据
    ms = 'qfq' + unit #"前复权"（forward adjusted quote）
    stk = response['data'][code]
    #对于普通股票：使用 stk[ms]，即获取前复权数据（如 'qfqday'）
    #对于指数：使用 stk[unit]，即获取原始数据（如 'day'）
    #因为指数不需要复权处理，所以指数数据中没有 'qfq' 开头的键
    buf = stk[ms] if ms in stk else stk[unit]  # 指数返回不是qfqday，而是day
    
    # 创建DataFrame并处理数据类型
    df = pd.DataFrame(buf, columns=['time', 'open', 'close', 'high', 'low', 'volume'], dtype='float')
    df.time = pd.to_datetime(df.time)
    df.set_index(['time'], inplace=True)
    df.index.name = ''
    
    return df

def get_price_min_tx(code, end_date=None, count=10, frequency='1d'):
    """从腾讯接口获取分钟线数据
    
    Args:
        code: 股票代码
        end_date: 结束日期，默认为None
        count: 获取数据的条数
        frequency: 数据周期，如 '1m', '5m', '15m', '30m', '60m'
    
    Returns:
        DataFrame包含columns: ['time', 'open', 'close', 'high', 'low', 'volume']
    """
    # 解析K线周期数
    ts = int(frequency[:-1]) if frequency[:-1].isdigit() else 1
    
    # 处理结束日期
    if end_date:
        end_date = end_date.strftime('%Y-%m-%d') if isinstance(end_date, datetime.date) else end_date.split(' ')[0]
    
    # 获取数据
    URL = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={code},m{ts},,{count}'
    response = json.loads(requests.get(URL).content)
    buf = response['data'][code]['m'+str(ts)]
    
    # 创建DataFrame并处理数据
    df = pd.DataFrame(buf, columns=['time', 'open', 'close', 'high', 'low', 'volume', 'n1', 'n2'])
    df = df[['time', 'open', 'close', 'high', 'low', 'volume']]
    df[['open', 'close', 'high', 'low', 'volume']] = df[['open', 'close', 'high', 'low', 'volume']].astype('float')
    df.time = pd.to_datetime(df.time)
    df.set_index(['time'], inplace=True)
    df.index.name = ''
    
    # 更新最新数据
    df['close'][-1] = float(response['data'][code]['qt'][code][3])
    
    return df

def get_price_sina(code, end_date='', count=10, frequency='60m'):
    """从新浪接口获取全周期数据
    
    Args:
        code: 股票代码
        end_date: 结束日期
        count: 获取数据的条数
        frequency: 数据周期，支持分钟线(5m,15m,30m,60m)和日线(1d=240m)、周线(1w=1200m)、月线(1M=7200m)
    
    Returns:
        DataFrame包含columns: ['day', 'open', 'high', 'low', 'close', 'volume']
    """
    # 转换周期单位
    frequency = frequency.replace('1d','240m').replace('1w','1200m').replace('1M','7200m')
    mcount = count
    
    # 解析K线周期数
    ts = int(frequency[:-1]) if frequency[:-1].isdigit() else 1
    
    # 处理日期和数据量
    if (end_date != '') and (frequency in ['240m', '1200m', '7200m']):
        end_date = pd.to_datetime(end_date) if not isinstance(end_date, datetime.date) else end_date
        unit = 4 if frequency=='1200m' else 29 if frequency=='7200m' else 1
        count = count + (datetime.datetime.now()-end_date).days//unit
    
    # 获取数据
    URL = f'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={code}&scale={ts}&ma=5&datalen={count}'
    dstr = json.loads(requests.get(URL).content)
    
    # 创建DataFrame并处理数据类型
    df = pd.DataFrame(dstr, columns=['day', 'open', 'high', 'low', 'close', 'volume'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    
    # 处理索引
    df.day = pd.to_datetime(df.day)
    df.set_index(['day'], inplace=True)
    df.index.name = ''
    
    # 处理结束日期的数据截取
    if (end_date != '') and (frequency in ['240m', '1200m', '7200m']):
        return df[df.index <= end_date][-mcount:]
    return df

def get_price(code, end_date='', count=10, frequency='1d', fields=[]):
    """统一接口函数，用于获取股票行情数据
    
    Args:
        code: 股票代码，支持多种格式：
              - 'sh000001' 或 '000001.XSHG' (上证指数)
              - 'sz399006' 或 '399006.XSHE' (创业板指)
        end_date: 结束日期，默认为当前日期
        count: 获取的数据条数
        frequency: 数据周期，支持：
                  - 日线'1d'、周线'1w'、月线'1M'
                  - 分钟线'1m','5m','15m','30m','60m'
        fields: 保留参数，用于未来扩展
    
    Returns:
        DataFrame格式的股票行情数据
    """
    # 统一股票代码格式
    xcode = code.replace('.XSHG', '').replace('.XSHE', '')
    xcode = 'sh'+xcode if ('XSHG' in code) else 'sz'+xcode if ('XSHE' in code) else code

    # 处理日线、周线、月线数据
    if frequency in ['1d', '1w', '1M']:
        try:
            return get_price_sina(xcode, end_date=end_date, count=count, frequency=frequency)  # 主力数据源
        except:
            return get_price_day_tx(xcode, end_date=end_date, count=count, frequency=frequency)  # 备用数据源

    # 处理分钟线数据
    if frequency in ['1m', '5m', '15m', '30m', '60m']:
        if frequency in '1m':
            return get_price_min_tx(xcode, end_date=end_date, count=count, frequency=frequency)
        try:
            return get_price_sina(xcode, end_date=end_date, count=count, frequency=frequency)  # 主力数据源
        except:
            return get_price_min_tx(xcode, end_date=end_date, count=count, frequency=frequency)  # 备用数据源

if __name__ == '__main__':
    df = get_price('sh000001', frequency='1d', count=10)  # 支持'1d'日, '1w'周, '1M'月
    print('上证指数日线行情\n', df)

    df = get_price('000001.XSHG', frequency='15m', count=10)  # 支持'1m','5m','15m','30m','60m'
    print('上证指数分钟线\n', df)

# Ashare 股票行情数据( https://github.com/mpquant/Ashare )
