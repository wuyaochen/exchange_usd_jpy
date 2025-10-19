import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

def plot_graph_usd(df_csv, show = True):
    x = df_csv['Period']
    y = df_csv['NTD/USD']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, marker='.', color='#1f77b4')

    # 降低 X 軸顯示刻度數量
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    # Y 軸：主要/次要刻度
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(0.25))

    # 格線：主要=年度；次要=每月
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1.0, color='0.7')
    ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='0.85')

    # 外觀微調（避免刻度擠在一起）
    ax.tick_params(axis='x', which='major', labelsize=9, rotation=0, pad=10)
    ax.tick_params(axis='x', which='minor', labelsize=7, rotation=90, pad=18)
    ax.tick_params(axis='y', which='major', labelsize=9)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax

def plot_graph_jpy(df_csv, show = True):
    x = df_csv['Period']
    y = df_csv['NTD/JPY']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, marker='.', color='#ff7f0e')

    # 降低 X 軸顯示刻度數量
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    # 依資料動態設定主刻度間距，避免過多 y 軸刻度
    gbp_min = y.min()
    gbp_max = y.max()
    gap = (gbp_max - gbp_min) / 8 if gbp_max > gbp_min else 1
    ax.yaxis.set_major_locator(mticker.MultipleLocator(gap))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(gap/2))

    ax.grid(which='major', axis='both', linestyle='-', linewidth=1.0, color='0.7')
    ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='0.85')

    ax.tick_params(axis='x', which='major', labelsize=9, rotation=0, pad=10)
    ax.tick_params(axis='x', which='minor', labelsize=7, rotation=90, pad=18)
    ax.tick_params(axis='y', which='major', labelsize=9)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax

def plot_graph_gbp(df_csv, show=True):
    x = df_csv['Period']
    y = df_csv['NTD/GBP']

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker='.', color="#0ec7ff")

    # X 軸：降低顯示刻度數量
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    # Y 軸：依資料動態設定主刻度間距
    gbp_min = y.min()
    gbp_max = y.max()
    gap = (gbp_max - gbp_min) / 8 if gbp_max > gbp_min else 1
    ax.yaxis.set_major_locator(mticker.MultipleLocator(gap))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(gap / 2))

    # 格線與外觀
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1.0, color='0.7')
    ax.grid(which='minor', axis='x', linestyle='--', linewidth=0.5, color='0.85')

    ax.tick_params(axis='x', which='major', labelsize=9, rotation=0, pad=10)
    ax.tick_params(axis='x', which='minor', labelsize=7, rotation=90, pad=18)
    ax.tick_params(axis='y', which='major', labelsize=9)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax