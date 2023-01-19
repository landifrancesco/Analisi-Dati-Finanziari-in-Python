from supporti_resistenze import SupportiResistenze

luk = SupportiResistenze("data_tradingview/lukoil.csv")
luk.title = "PJSC Lukoil - Azienda petrolifera russa"
luk.marker = 6
luk.yaxis_limit = 2000
luk.yaxis_marker = 2700
luk.yaxis_text = 2450
luk.plot()
