from libs import *


class MACD(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self.df_macd = self._get_macd(26, 12, 9)

    def _get_macd(self, slow, fast, smooth):
        price = self.df['Close']
        exp1 = price.ewm(span=fast, adjust=False).mean()
        exp2 = price.ewm(span=slow, adjust=False).mean()
        macd = pd.DataFrame(exp1 - exp2).rename(columns={'Close': 'Macd'})
        signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(columns={'Macd': 'Signal'})
        hist = pd.DataFrame(macd['Macd'] - signal['Signal']).rename(columns={0: 'Hist'})
        frames = [macd, signal, hist]
        return pd.concat(frames, join='inner', axis=1)

    def plot(self):
        prices = self.df
        macd = self.df_macd['Macd']
        signal = self.df_macd['Signal']
        hist = self.df_macd['Hist']

        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

        candlestick_ohlc(ax1, prices.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

        ax2.plot(macd, color='blue', linewidth=1.5, label='MACD')
        ax2.plot(signal, color='orange', linewidth=1.5, label='SEGNALE')

        for i in range(len(prices)):
            if str(hist[i])[0] == '-':
                ax2.bar(prices.index[i], hist[i], color='red')
                # ef5350 rosso
            else:
                ax2.bar(prices.index[i], hist[i], color='green')
                # 26a69a verde

        date_format = mpl_dates.DateFormatter('%b')
        ax2.xaxis.set_major_formatter(date_format)
        ax2.xaxis.set_major_locator(mpl_dates.MonthLocator())
        ax1.set(xticklabels=[])  # remove the tick labels
        ax1.tick_params(bottom=False)  # remove the ticks
        plt.legend(loc='lower left')

        if self.title is not None:
            ax1.set_title(self.title)

        if self.marker is not None:
            ax1.scatter(x=19047.166666666668, y=self.yaxis_marker, marker=self.marker, color="purple")
            ax1.annotate('Inizio conflitto - 24 Febbraio', xy=(19047.166666666668, self.yaxis_marker),
                         xytext=(19017.166666666668, self.yaxis_text),
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        plt.show()