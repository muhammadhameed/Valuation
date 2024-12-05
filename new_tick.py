import pandas as pd
import yfinance as yf

# List of ticker symbols
ticker_symbols = [
    "XHS.MI", "WTBL.XC", "WTBDY", "WTB.L", "WHF4.SG", "WHF4.MU", "WHF4.F", "WHF4.DU", "WHF4.BE", "WH",
    "VELHO.BO", "VACBT.PA", "VACBS.PA", "VAC.PA", "UPHOT.BO", "ULAS.IS", "THW.AQ", "TGBHOTELS.NS", "TGBHOTELS.BO", "TEKTU.IS",
    "TAJGVK.NS", "TAJGVK.BO", "SSU.JO", "SSTY.L", "SST.SG", "SOTS.JK", "SONDW", "SOND", "SOKOUK.KW", "SNLK.JK",
    "SKTP", "SKLN.TA", "SINCLAIR.BO", "SHOT.ST", "SHN.SG", "SHN.MU", "SHN.F", "SHN.DU", "SHN.BE", "SHID.JK",
    "SHCO", "SHANG.BK", "SHANG-R.BK", "SHALY", "SHALF", "SAYAJIHOTL.BO", "SAVERA.BO", "SAMHI.NS", "SAMHI.BO", "S07.SI",
    "ROHLTD.NS", "ROHLTD.BO", "ROH.BK", "ROH-R.BK", "RHL.NS", "RHL.BO", "RH6B.SG", "RH6B.F", "RELIABVEN.BO", "RAYALEMA.BO",
    "RASRESOR.BO", "QU5A.SG", "QU5A.MU", "QU5A.F", "PV6.SG", "PV6.MU", "PV6.F", "PV6.DU", "PV6.BE", "PSKT.JK",
    "PPHL.XC", "PPH.L", "PLAN.JK", "PHOENIXTN.BO", "PGLI.JK", "PARKHOTELS.NS", "PARKHOTELS.BO", "OU8.SI", "ORIENTHOT.NS",
    "ORIENTHOT.BO", "OHTL.BK", "OHTL-R.BK", "NHH.MC", "NH5.SG", "NH5.MU", "NH5.F", "NH5.DU", "NH5.BE", "NE4H.F",
    "NATO.JK", "MLHMC.PA", "MLHBP.PA", "MLAZR.PA", "MINT.BK", "MINT-R.BK", "MINA.JK", "MEL.VI", "MEL.SG", "MEL.MU","MEL.MC", "MEL.F", "MEL.DU", "MEL.BE", "MCK.NZ", "MARTI.IS", "MAR.VI", "MAR", "MAQ.SG", "MAQ.MU", "MAQ.HM", "MAQ.HA", "MAQ.F", "MAQ.DU", "MAQ.BE", "MAORF", "MANRIN.BK", "MANRIN-R.BK", "MAALT.IS", "M1TT34.SA", "M04.SI", "LUXHP", "LUXH", "LRH.BK", "LRH-R.BK", "LORDSHOTL.BO", "LEMONTREE.NS", "LEMONTREE.BO", "LAMPS.AT", "L38.SI", "KSTUR.IS", "KEC.SG", "KEC.MU", "KEC.F", "KAMATHOTEL.NS", "KAMATHOTEL.BO", "JUNIPER.NS", "JUNIPER.BO", "JK9.SG", "JK9.F", "JINDHOT.BO", "JIHD.JK", "ITDC.NS", "ITDC.BO", "ISRO.TA", "INTG", "INL.AX", "INDO.JK", "INDHOTEL.NS", "INDHOTEL.BO", "IHGL.XC", "IHG.L", "IHG", "IFA.HM", "ICON.JK", "IC1H.SG", "IC1H.MU", "IC1H.HA", "IC1H.F", "IC1H.DU", "IC1H.BE", "IC1B.F", "HYDP.AQ", "HTHT", "HSG.MU", "HSG.F", "HSG.BE", "HRME.JK", "HOWARHO.BO", "HOTLSILV.BO", "HOTEL.MX", "HOOT4.SA", "HLVLTD.NS", "HLVLTD.BO", "HLTW.VI", "HLT.MX", "HLT", "HI91.SG", "HI91.MU", "HI91.HA", "HI91.F", "HI91.DU", "HI91.BE", "HFUS", "HDP.PA", "HCITY.MX", "HAVISHA.NS", "HAVISHA.BO", "H1LT34.SA", "H18.SI", "H15.SI", "H07.SI", "H", "GUJHOTE.BO", "GT1A.SG", "GT1A.F", "GRPH.JK", "GRAVISSHO.BO", "GRAND.BK", "GRAND-R.BK",
    "GHG", "GD1M.F", "FTAL.TA", "FITT.JK", "ESTA.JK", "ERW.BK", "ERW-R.BK", "EIHOTEL.NS", "EIHOTEL.BO", "EIHAHOTELS.NS", "EIHAHOTELS.BO", "EBG.AX", "EAST.JK", "DUSIT.BK", "DUSIT-R.BK", "DHG.SG", "DHG.MU", "DHG.IR", "DHG.F", "DHG.DU", "DHG.BE", "DANH.TA", "DAL.L", "DAH.VN", "D5LA.F", "CZH.SG", "CZH.F", "CLH.JO", "CL4A.SG", "CL4A.MU", "CL4A.F", "CL4A.BE", "CL4.MU", "CL4.F", "CKI.TO", "CK5A.F", "CK5A.DU", "CINDHO.BO", "CHLLTD.BO", "CHH", "CHALET.NS", "CHALET.BO", "CDZ0.MU", "CDZ0.F", "CDZ0.DU", "CDZ0.DE", "CDZ0.BE", "CCHHL.NS", "CCHHL.BO", "C7P.BE", "BYKE.NS", "BYKE.BO", "BUVA.JK", "BSP.OL", "BLUECOAST.NS", "BKW.SI", "BEYOND.BK", "BEYOND-R.BK", "BESTEAST.BO", "BENARAS.BO", "AVX.SI", "ATAT", "ASIANHOTNR.NS", "ASIANHOTNR.BO", "ASIA.BK", "ASIA-R.BK", "ARUNAHTEL.BO", "ARTA.JK", "ALLHB.PA", "AKKU.JK", "AHLEAST.NS", "AHLEAST.BO", "ADVANIHOTR.NS", "ADVANIHOTR.BO", "ACRFF", "ACR1.MU", "ACR1.F", "ACR1.DU", "ACR.SG", "ACR.MU", "ACR.HM", "ACR.HA", "ACR.F", "ACR.DU", "ACR.DE", "ACR.BE", "ACCYY", "AC.VI", "AC.PA", "A34.SI", "9723.T", "9722.T", "9720.T", "9713.T", "9708.T", "9704.T", "9616.T", "900942.SS", "900934.SS", "900929.SS",
    "8MI.SG", "8MI.BE", "8885.KL", "8237.HK", "8077.TWO", "7KW.F", "75Z.MU", "75Z.F", "75Z.DU", "7243.KL", "6565.T", "6547.T", "648.SG", "648.F", "648.DU", "6076.F", "603136.SS", "601007.SS", "600754.SS", "600749.SS", "600258.SS", "600138.SS", "600054.SS", "5RI.F", "5RA.SI", "5I4.SI", "5HH.SI", "5DP.SI", "5738.KL", "5704.TWO", "5703.TWO", "5592.KL", "5517.KL", "5364.TWO", "4691.T", "4250.SR", "4100.SR", "3WP.SG", "3R8.F", "3891.KL", "3573.KL", "32P.SG", "32P.F", "32P.BE", "301073.SZ", "2WY.MU", "2WY.F", "2WY.DU", "2WY.BE", "2HN.F", "2748.TW", "2739.TW", "2736.TWO", "2730.TWO", "2724.TWO", "2718.TWO", "2707.TW", "2706.TW", "2705.TW", "2704.TW", "2702.TW", "2404.T", "2097.KL", "1HTA.SG", "1HTA.MU", "1HTA.F", "1HTA.DU", "1HTA.BE", "1C4.F", "1832.HK", "1820.SR", "1643.KL", "1355.HK", "1270.HK", "1221.HK", "1215.HK", "1189.HK", "1179.HK", "10H.MU", "10H.F", "10H.DU", "10H.BE", "0RD7.IL", "0MKO.IL", "0H59.IL", "0617.HK", "0559.HK", "0253.HK", "0219.HK", "0201.HK", "0199.HK", "0193.HK", "0184.HK", "0181.HK", "0078.HK", "0069.HK", "006730.KQ", "0045.HK", "0042.HK"
]

# Create an empty DataFrame
df = pd.DataFrame(columns=["Ticker", "Country", "Business Summary"])

# Iterate over ticker symbols and fetch information
for symbol in ticker_symbols:
    # Fetching stock information using yfinance
    stock_info = yf.Ticker(symbol).info
    # Extracting required information
    country = stock_info.get("country", "N/A")
    business_summary = stock_info.get("longBusinessSummary", "N/A")
    # Append to DataFrame
    df = df.append({"Ticker": symbol, "Country": country, "Business Summary": business_summary}, ignore_index=True)

# Write DataFrame to Excel
df.to_excel("ticker_info.xlsx", index=False)
