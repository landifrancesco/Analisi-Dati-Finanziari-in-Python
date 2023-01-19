from libs import *


class MovingAverage(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)

    def sma(self, periodo, etichetta=None):
        return [self.df['Close'].rolling(window=periodo).mean(), etichetta] if etichetta is not None else self.df['Close'].rolling(window=periodo).mean()

    def ema(self, periodo, etichetta=None):
        return [self.df['Close'].ewm(span=periodo, adjust=False).mean(), etichetta] if etichetta is not None else self.df['Close'].ewm(span=periodo, adjust=False).mean()

    def plot(self, *args):
        fig, ax = plt.subplots(figsize=(16, 9))
        candlestick_ohlc(ax, self.df.values, width=0.6, colorup='green',
                         colordown='red', alpha=0.8)

        for arg in args:
            plt.plot(arg[0], label=arg[1])

        date_format = mpl_dates.DateFormatter('%b')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mpl_dates.MonthLocator())
        plt.legend()

        if self.title is not None:
            plt.title(self.title)

        plt.show()