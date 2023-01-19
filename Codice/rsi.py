from libs import *


class RSI(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self.df_rsi = self._get_rsi(14)
        
    def _get_rsi(self, periodo):
        df = self.df['Close'].copy().to_frame()

        df['Diff'] = df.diff(1)
        df['Gain'] = df['Diff'].clip(lower=0).round(2)
        df['Loss'] = df['Diff'].clip(upper=0).abs().round(2)
        df['AvgGain'] = df['Gain'].rolling(window=periodo, min_periods=periodo).mean()[:periodo + 1]
        df['AvgLoss'] = df['Loss'].rolling(window=periodo, min_periods=periodo).mean()[:periodo + 1]

        for i, row in enumerate(df['AvgGain'].iloc[periodo + 1:]):
            df['AvgGain'].iloc[i + periodo + 1] = \
                (df['AvgGain'].iloc[i + periodo] *
                 (periodo - 1) +
                 df['Gain'].iloc[i + periodo + 1]) \
                / periodo

        for i, row in enumerate(df['AvgLoss'].iloc[periodo + 1:]):
            df['AvgLoss'].iloc[i + periodo + 1] = \
                (df['AvgLoss'].iloc[i + periodo] *
                 (periodo - 1) +
                 df['Loss'].iloc[i + periodo + 1]) \
                / periodo

        df['Rs'] = df['AvgGain'] / df['AvgLoss']
        df['Rsi'] = 100 - (100 / (1.0 + df['Rs']))
        
        return df

    def plot(self, livelli):
        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

        candlestick_ohlc(ax1, self.df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        ax2.plot(self.df_rsi['Rsi'], linewidth=1, color='black')
        ax2.set_xlim(ax1.get_xlim())
        x1, y1 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[0], livelli[0]]
        x2, y2 = [ax2.get_xlim()[0], ax2.get_xlim()[1]], [livelli[1], livelli[1]]
        ax2.plot(x1, y1, color='grey', linestyle='--')
        ax2.plot(x2, y2, color='grey', linestyle='--')

        ax1.set(xticklabels=[])  # remove the tick labels
        ax1.tick_params(bottom=False)  # remove the ticks

        if self.title is not None:
            ax1.set_title(self.title)

        date_format = mpl_dates.DateFormatter('%b')
        ax2.xaxis.set_major_formatter(date_format)
        ax2.xaxis.set_major_locator(mpl_dates.MonthLocator())

        plt.show()