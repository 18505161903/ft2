import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def backtesting(file=None):
    df = pd.read_excel(file)
    capital = df.iloc[0, 12]
    df = df.drop(0)

    df['成交笔数'] = df['Lot']

    df["net_pnl"] = df["Profit"]
    df["balance"] = df["net_pnl"].cumsum() + capital  # 资金
    # print(df)
    df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
    df["highlevel"] = (
        df["balance"].rolling(
            min_periods=1, window=len(df), center=False).max()
    )
    df["drawdown"] = df["balance"] - df["highlevel"]
    df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

    start_date = df.iloc[1, 4]
    end_date = df.iloc[-1, 8]

    total_days = len(df)
    profit_days = len(df[df["net_pnl"] > 0])
    loss_days = len(df[df["net_pnl"] < 0])

    win = profit_days / total_days*100

    end_balance = df["balance"].iloc[-1]
    max_drawdown = df["drawdown"].min()
    max_ddpercent = df["ddpercent"].min()
    total_net_pnl = df["net_pnl"].sum()
    daily_net_pnl = total_net_pnl / total_days

    total_trade_count = df["成交笔数"].sum()
    average_profit = total_net_pnl / (total_trade_count/2)

    total_return = (end_balance / capital - 1) * 100
    annual_return = total_return / total_days * 240
    daily_return = df["return"].mean() * 100
    return_std = df["return"].std() * 100
    daily_trade_count = total_trade_count / total_days

    if return_std:
        sharpe_ratio = daily_return / return_std * np.sqrt(240)
    else:
        sharpe_ratio = 0

    return_drawdown_ratio = -total_return / max_ddpercent

    print("-" * 30)
    print(f"首个交易日：\t{start_date}")
    print(f"最后交易日：\t{end_date}")

    print(f"总交易日：\t{total_days}")
    print(f"盈利交易日：\t{profit_days}")
    print(f"亏损交易日：\t{loss_days}")
    print(f"胜率：\t{win:,.2f}%")

    print(f"起始资金：\t{capital:,.2f}")
    print(f"结束资金：\t{end_balance:,.2f}")

    print(f"总收益率：\t{total_return:,.2f}%")
    print(f"年化收益：\t{annual_return:,.2f}%")
    print(f"最大回撤: \t{max_drawdown:,.2f}")
    print(f"百分比最大回撤: {max_ddpercent:,.2f}%")

    print(f"总盈亏：\t{total_net_pnl:,.2f}")
    print(f"日均盈亏：\t{daily_net_pnl:,.2f}")
    print(f"总成交笔数：\t{total_trade_count}")
    print(f"平均利润：\t{average_profit:,.2f}")

    print(f"日均收益率：\t{daily_return:,.2f}%")
    print(f"收益标准差：\t{return_std:,.2f}%")
    print(f"夏普比率：\t{sharpe_ratio:,.2f}")
    print(f"收益回撤比：\t{return_drawdown_ratio:,.2f}")
    print(f"日均成交笔数：\t{daily_trade_count}")

    plt.figure(figsize=(15, 21))
    balance_plot = plt.subplot(4, 1, 1)
    balance_plot.set_title("Balance")  # 资金曲线
    df["balance"].plot(legend=True)

    drawdown_plot = plt.subplot(4, 1, 2)
    drawdown_plot.set_title("Drawdown")  # 最大回撤
    drawdown_plot.fill_between(range(len(df)), df["drawdown"].values)

    pnl_plot = plt.subplot(4, 1, 3)
    pnl_plot.set_title("Daily Pnl")  # 单笔盈亏
    df["net_pnl"].plot(kind="bar", legend=False, grid=False, xticks=[])

    distribution_plot = plt.subplot(4, 1, 4)
    distribution_plot.set_title("Daily Pnl Distribution")  # 正态分布
    df["net_pnl"].hist(bins=50)
    plt.show()

def txt_tb(file_csv=None, file_txt=None):
    data = pd.read_csv(file_csv, ',', encoding='gbk')
    data_t = pd.to_datetime(data['时间'])
    data['<Date>'] = data_t.apply(lambda x: x.strftime("%Y.%m.%d"))
    data['<Time>'] = data_t.apply(lambda x: x.strftime("%H:%M:%S"))
    data.drop(['时间', '持仓量'], axis=1, inplace=True)
    data = data[['<Date>', '<Time>', '开盘价', '最高价', '最低价', '收盘价', '成交量']]
    df = data.rename(columns={'开盘价': '<OPEN>', '最高价': '<HIGH>', '最低价': '<LOW>', '收盘价': '<CLOSE>', '成交量': '<VOL>'})
    df.to_csv(file_txt, index=0)
    print("OK")

if __name__ == '__main__':
    backtesting(r'C:\Users\Administrator\Documents\2013rb.xlsx')