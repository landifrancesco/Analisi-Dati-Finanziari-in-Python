from fascio_ema import FascioEma

srs = FascioEma("SRS.MI")
srs.title = "Fascio di medie mobili - Saras S.p.A"
srs.marker = 7
srs.yaxis_marker = 1
srs.yaxis_text = 1.05
srs.plot("blue", "orange")
