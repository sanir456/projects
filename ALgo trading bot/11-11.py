import datetime as dt
import yfinance as yf
import pandas as pd
import mplfinance as fplt

st_date = dt.datetime.today() - dt.timedelta(1825)
end_date = dt.datetime.today()
tiker_name = "TCS.NS"
ohlcv = yf.download(tiker_name,st_date,end_date)


# Function to calculate average true range
def ATR(DF, day):
  df = DF.copy() 
  df['H-L'] = abs(df['High'] - df['Low']) 
  df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
  df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1)) 
  df['TR'] = df[['H-L','H-PC','L-PC']].max(axis =1, skipna = False) 
  df['ATR'] = df['TR'].rolling(day).mean() 
  df = df.drop(['H-L','H-PC','L-PC'], axis =1) 
  df.dropna(inplace = True) 
  return df

print(ATR(ohlcv,50))

bricks = round(ATR(ohlcv,50)["ATR"][-1],0) #capturing the latest ATR
print(bricks)

fplt.plot(ohlcv,type='renko',renko_params=dict(brick_size=bricks, atr_length=14),
          style='yahoo',figsize =(18,7),
          title = "RENKO CHART WITH ATR{0}".format('ticker_name'))

