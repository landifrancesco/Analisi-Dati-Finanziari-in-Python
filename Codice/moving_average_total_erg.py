from moving_average import MovingAverage


erg = MovingAverage("ERG.MI")
erg.title = "Media mobile esponenziale"
sma = erg.sma(20, "SMA 20")
ema = erg.ema(20, "EMA 20")
erg.plot(ema)