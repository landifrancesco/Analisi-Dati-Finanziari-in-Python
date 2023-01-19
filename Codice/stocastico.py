from libs import *


class Stocastico(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self.df2 = self._get_stocastico(14, 3)

    def _get_stocastico(self, periodo_k, periodo_d):
        df = self.df.copy()
        df['n_high'] = df['High'].rolling(periodo_k).max()
        # Adds an "n_low" column with min value of previous 14 periods
        df['n_low'] = df['Low'].rolling(periodo_k).min()
        # Uses the min/max values to calculate the %k (as a percentage)
        df['%K'] = (df['Close'] - df['n_low']) * 100 / (df['n_high'] - df['n_low'])
        # Uses the %k to calculates a SMA over the past 3 values of %k
        df['%D'] = df['%K'].rolling(periodo_d).mean()

        # Add some indicators
        df.ta.stoch(high='High', low='Low', close='Close', k=periodo_k, d=periodo_d, append=True)

        # Avoid case-sensitive issues for accessing data.
        # Optional if using pandas_ta
        df.columns = [x.lower() for x in df.columns]

        return df

    def plot(self):
        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

        candlestick_ohlc(ax1, self.df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        ax2.plot(self.df2['stochk_14_3_3'], color='orange', label="Veloce")
        ax2.plot(self.df2['stochd_14_3_3'], color='blue', label="Lenta")

        ax2.set_ylim([0, 100])
        ax2.set_xlim(ax1.get_xlim())
        livelli = [20, 80]
        x1, y1 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[0], livelli[0]]
        x2, y2 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[1], livelli[1]]
        ax2.plot(x1, y1, color='grey', linestyle='--')
        ax2.plot(x2, y2, color='grey', linestyle='--')
        livelli = [30, 70]
        x1, y1 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[0], livelli[0]]
        x2, y2 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[1], livelli[1]]
        ax2.plot(x1, y1, color='grey', linestyle='-.')
        ax2.plot(x2, y2, color='grey', linestyle='-.')

        ax1.set(xticklabels=[])  # remove the tick labels
        ax1.tick_params(bottom=False)  # remove the ticks
        date_format = mpl_dates.DateFormatter('%b')
        ax2.xaxis.set_major_formatter(date_format)
        ax2.xaxis.set_major_locator(mpl_dates.MonthLocator())
        plt.legend(loc='lower left')

        if self.title is not None:
            ax1.set_title(self.title)

        if self.marker is not None:
            ax1.scatter(x=19047.166666666668, y=self.yaxis_marker, marker=self.marker, color="purple")
            ax1.annotate('Inizio conflitto - 24 Febbraio', xy=(19047.166666666668, self.yaxis_marker),
                         xytext=(19017.166666666668, self.yaxis_text),
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        plt.show()
