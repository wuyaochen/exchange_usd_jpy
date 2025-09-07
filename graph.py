import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

def plot_graph_usd(df_csv, show: bool = True):
    x = df_csv['Period']
    y = df_csv['NTD/USD']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, marker='.', color='#1f77b4')

    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    # Y 軸：主要/次要刻度
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(0.25))

    # 格線：主要=年度（較粗）；次要=每月
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1.0, color='0.7')

    # 外觀微調（只顯示每月標籤，旋轉避免重疊）
    ax.tick_params(axis='x', which='minor', labelsize=7, rotation=90, pad=20)
    ax.tick_params(axis='y', which='major', labelsize=9)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax

def plot_graph_jpy(df_csv, show: bool = True):
    x = df_csv['Period']
    y = df_csv['NTD/JPY']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, marker='.', color='#ff7f0e')

    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%Y-%m'))

    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.01))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(0.5))

    ax.grid(which='major', axis='both', linestyle='-', linewidth=1.0, color='0.7')
    ax.tick_params(axis='x', which='minor', labelsize=7, rotation=90, pad=20)
    ax.tick_params(axis='y', which='major', labelsize=9)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax