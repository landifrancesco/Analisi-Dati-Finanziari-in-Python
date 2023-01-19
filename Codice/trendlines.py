from libs import *


class Trendlines(DownloadDati):
    def __init__(self, titolo_azionario):
        super().__init__(titolo_azionario)
        self._get_channel()

    def _get_channel(self):
        df_len = len(self.df)
        self.df['Number'] = np.arange(df_len) + 1
        df_high = self.df.copy()
        df_low = self.df.copy()

        while len(df_low) > 2:
            slope, intercept, r_value, p_value, std_err = linregress(x=df_low['Number'], y=df_low['Low'])
            df_low = df_low.loc[df_low['Low'] < slope * df_low['Number'] + intercept]

        while len(df_high) > 2:
            slope, intercept, r_value, p_value, std_err = linregress(x=df_high['Number'], y=df_high['High'])
            df_high = df_high.loc[df_high['High'] > slope * df_high['Number'] + intercept]

        slope, intercept, r_value, p_value, std_err = linregress(x=df_high['Number'], y=df_high['Close'])
        self.df['Downtrend'] = slope * self.df['Number'] + intercept

        slope, intercept, r_value, p_value, std_err = linregress(x=df_low['Number'], y=df_low['Close'])
        self.df['Uptrend'] = slope * self.df['Number'] + intercept

    def plot(self, downtrend=True, uptrend=True):
        fig, ax1 = plt.subplots(figsize=(16, 9))
        candlestick_ohlc(ax1, self.df.values, width=0.6, colorup='green',
                         colordown='red', alpha=0.8)

        ax2 = ax1.twiny()  # ax2 and ax1 will have common y axis and different x axis, twiny

        if downtrend:
            ax2.plot(self.df['Number'], self.df['Downtrend'], label="Downtrend", color="orange")

        if uptrend:
            ax2.plot(self.df['Number'], self.df['Uptrend'], label="Uptrend", color="blue")

        plt.legend()
        plt.tick_params(left=False, top=False, labelleft=False, labeltop=False)
        date_format = mpl_dates.DateFormatter('%b')
        ax1.xaxis.set_major_formatter(date_format)
        ax1.xaxis.set_major_locator(mpl_dates.MonthLocator())

        if self.title is not None:
            ax1.set_title(self.title)

        if self.marker is not None:
            ax1.scatter(x=19047.166666666668, y=self.yaxis_marker, marker=self.marker, color="purple")
            ax1.annotate('Inizio conflitto - 24 Febbraio', xy=(19047.166666666668, self.yaxis_marker),
                         xytext=(19017.166666666668, self.yaxis_text),
                         bbox={'facecolor': 'purple', 'alpha': 0.2, 'pad': 2})

        plt.show()


    