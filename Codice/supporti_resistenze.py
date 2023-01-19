from libs import *


class SupportiResistenze(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)

    def _is_support(self, i):
        cond1 = self.df['Low'][i] < self.df['Low'][i - 1]
        cond2 = self.df['Low'][i] < self.df['Low'][i + 1]
        cond3 = self.df['Low'][i + 1] < self.df['Low'][i + 2]
        cond4 = self.df['Low'][i - 1] < self.df['Low'][i - 2]
        return (cond1 and cond2 and cond3 and cond4)  # determine bearish fractal

    def _is_resistance(self, i):
        cond1 = self.df['High'][i] > self.df['High'][i - 1]
        cond2 = self.df['High'][i] > self.df['High'][i + 1]
        cond3 = self.df['High'][i + 1] > self.df['High'][i + 2]
        cond4 = self.df['High'][i - 1] > self.df['High'][i - 2]
        return (cond1 and cond2 and cond3 and cond4)  # to make sure the new level area does not exist already

    def _is_far_from_level(self, value, levels):
        ave = np.mean(self.df['High'] - self.df['Low'])
        return np.sum(
            [abs(value - level) < ave for _, level in levels]) == 0  # a list to store resistance and support levels

    def plot(self):
        levels = []

        for i in range(2, self.df.shape[0] - 2):
            if self._is_support(i):
                low = self.df['Low'][i]
                if self._is_far_from_level(low, levels):
                    levels.append((i, low))
            elif self._is_resistance(i):
                high = self.df['High'][i]
                if self._is_far_from_level(high, levels):
                    levels.append((i, high))

        pivots = []
        max_list = []
        min_list = []
        for i in range(5, len(self.df) - 5):
            # taking a window of 9 candles
            high_range = self.df['High'][i - 5:i + 4]
            current_max = high_range.max()
            # if we find a new maximum value, empty the max_list
            if current_max not in max_list:
                max_list = []
            max_list.append(current_max)
            # if the maximum value remains the same after shifting 5 times
            if len(max_list) == 5 and self._is_far_from_level(current_max, pivots):
                pivots.append((high_range.idxmax(), current_max))

            low_range = self.df['Low'][i - 5:i + 5]
            current_min = low_range.min()
            if current_min not in min_list:
                min_list = []
            min_list.append(current_min)
            if len(min_list) == 5 and self._is_far_from_level(current_min, pivots):
                pivots.append((low_range.idxmin(), current_min))

        fig, ax = plt.subplots(figsize=(16, 9))
        candlestick_ohlc(ax, self.df.values, width=0.6, colorup='green',
                         colordown='red', alpha=0.8)

        i = 0

        for level in pivots:
            i += 1
            plt.hlines(level[1], xmin=self.df['Date'][level[0]], xmax=
            max(self.df['Date']), colors='blue', linestyle='-.')
            plt.annotate(i, xy=(self.df['Date'].max() + 5, level[1]), xytext=(self.df['Date'].max() + 5, level[1]),
                         weight='bold',
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        if self.title is not None:
            plt.title(self.title)

        if self.marker is not None:
            plt.scatter(x=19047.166666666668, y=self.yaxis_marker, marker=self.marker, color="purple")
            plt.annotate('Inizio conflitto - 24 Febbraio', xy=(19047.166666666668, self.yaxis_marker),
                         xytext=(19017.166666666668, self.yaxis_text),
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        if self.yaxis_limit is not None:
            ax.set_ylim([self.yaxis_limit, ax.get_ylim()[1]])

        date_format = mpl_dates.DateFormatter('%b')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mpl_dates.MonthLocator())

        plt.show()
