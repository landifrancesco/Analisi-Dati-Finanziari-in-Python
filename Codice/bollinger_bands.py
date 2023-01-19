from libs import *


class BollingerBands(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self._get_bb(20)

    def _get_bb(self, periodo):
        sma_str = 'SMA_' + str(periodo)
        self.df[sma_str] = self.df['Close'].rolling(window=periodo).mean()
        std = self.df['Close'].rolling(window = periodo).std()
        self.df['UpperBB'] = self.df[sma_str] + std * 2
        self.df['LowerBB'] = self.df[sma_str] - std * 2
        self.df['Bandwidth'] = (4*std)/self.df[sma_str]

    def plot(self, upper_bb=True, sma=True, lower_bb=True):
        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

        candlestick_ohlc(ax1, self.df.values, width=0.6, colorup='green',
                         colordown='red', alpha=0.8)

        if upper_bb:
            ax1.plot(self.df['UpperBB'], linestyle='--', linewidth=1, color='black')

        if sma:
            ax1.plot(self.df.filter(regex='^SMA', axis=1), linestyle='--', linewidth=1.2, color='grey')

        if lower_bb:
            ax1.plot(self.df['LowerBB'], linestyle='--', linewidth=1, color='black')

        ax2.set_xlim(ax1.get_xlim())
        ax2.plot(self.df['Bandwidth'], linewidth=1, color='black')

        date_format = mpl_dates.DateFormatter('%b')
        ax2.xaxis.set_major_formatter(date_format)
        ax2.xaxis.set_major_locator(mpl_dates.MonthLocator())
        ax1.set(xticklabels=[])  # remove the tick labels
        ax1.tick_params(bottom=False)  # remove the ticks
        plt.legend(loc='lower left')

        if self.title is not None:
            ax1.set_title(self.title)

        plt.show()
