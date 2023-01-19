from libs import *
from moving_average import MovingAverage


class FascioEma(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self.ma = MovingAverage(titolo_azionario)
        self.ema_fast = self._get_ema_fast()
        self.ema_slow = self._get_ema_slow()

    def _get_ema_fast(self):
        ema_fast_periodi = [3, 5, 8, 1, 12, 15]
        ema_fast = []
        for periodo in ema_fast_periodi:
            ema_fast.append(self.ma.ema(periodo))
        return ema_fast

    def _get_ema_slow(self):
        ema_fast_periodi = [30, 35, 40, 45, 50, 60]
        ema_slow = []
        for periodo in ema_fast_periodi:
            ema_slow.append(self.ma.ema(periodo))
        return ema_slow

    def plot(self, colore_fast, colore_slow):
        fig, ax = plt.subplots(figsize=(16, 9))
        candlestick_ohlc(ax, self.df.values, width=0.6, colorup="green",
                         colordown="red", alpha=0.8)
        width = 1

        for ema in self.ema_fast[:len(self.ema_fast)-1]:
            plt.plot(ema, linewidth=width, color=colore_fast)
        plt.plot(self.ema_fast[-1], linewidth=width, color=colore_fast, label="Veloce")

        for ema in self.ema_slow[:len(self.ema_slow)-1]:
            plt.plot(ema, linewidth=width, color=colore_slow)
        plt.plot(self.ema_slow[-1], linewidth=width, color=colore_slow, label="Lenta")

        date_format = mpl_dates.DateFormatter('%b')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mpl_dates.MonthLocator())
        plt.legend()

        if self.title is not None:
            plt.title(self.title)

        if self.marker is not None:
            plt.scatter(x=19047.166666666668, y=self.yaxis_marker, marker=self.marker, color="purple")
            plt.annotate('Inizio conflitto - 24 Febbraio', xy=(19047.166666666668, self.yaxis_marker),
                         xytext=(19017.166666666668, self.yaxis_text),
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        plt.show()
