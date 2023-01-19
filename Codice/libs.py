import locale
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_ta as ta
from scipy.stats import linregress
import yfinance as yf

locale.setlocale(locale.LC_ALL, 'it_IT')


class DownloadDati:
    def __init__(self, titolo_azionario):
        self.df = None
        self._marker = None
        self._ylim = None
        self._ymarker = None
        self._ytext = None
        self._title = None
        if ".csv" in titolo_azionario:
            self.df = self.csv(titolo_azionario)
        else:
            self.df = self.yahoo(titolo_azionario)

    def yahoo(self, ticker):
        df = yf.download(ticker, start='2022-01-01', end='2022-12-31', threads=True)
        df['Date'] = pd.to_datetime(df.index)
        df['Date'] = df['Date'].apply(mpl_dates.date2num)
        df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        return df

    def csv(self, file):
        df = pd.read_csv(file, delimiter=";", index_col=0, keep_date_col=True)
        df['Date'] = pd.to_datetime(df.index)
        df['Date'] = df['Date'].apply(mpl_dates.date2num)
        df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        return df

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, value):
        self._marker = value

    @property
    def yaxis_limit(self):
        return self._ylim

    @yaxis_limit.setter
    def yaxis_limit(self, value):
        self._ylim = value

    @property
    def yaxis_marker(self):
        return self._ymarker

    @yaxis_marker.setter
    def yaxis_marker(self, value):
        self._ymarker = value

    @property
    def yaxis_text(self):
        return self._ytext

    @yaxis_text.setter
    def yaxis_text(self, value):
        self._ytext = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, text):
        self._title = text