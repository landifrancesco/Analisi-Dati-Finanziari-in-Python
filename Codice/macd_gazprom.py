from macd import MACD

gzp = MACD("data_tradingview/gazprom.csv")
gzp.title = "PJSC Gazprom - Azienda petrolifera russa"
gzp.marker = 7
gzp.yaxis_marker = 350
gzp.yaxis_text = 358
gzp.plot()
