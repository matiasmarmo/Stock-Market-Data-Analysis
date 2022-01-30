import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mpl_dates
import numpy as np

##Get params
symbol = input('Enter Stock symbol (default: AAPL): ') or 'AAPL'
period1 = int(time.mktime(datetime.datetime(2021, 3, 1, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2021, 10, 11, 23, 59).timetuple()))
interval = input('Enter interval (default: 1d):') or '1d'

## Get market stock data
query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

## Extracting Data for plotting
df = pd.read_csv(query_string)
print(df)
data = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
data['Date'] = pd.to_datetime(data['Date'])
print(data)

## Creating Subplots
data = data.set_index('Date')

print(data)
data['period'] = range(1,len(data)+1)

data_to_show = data.tail(250)
#plt.style.use('dark_background')
#plt.figure(figsize=(12, 6))
#plt.rcParams['axes.facecolor'] = '#181c27'
#plt.grid(color='#9598a1', linestyle='-', linewidth=0.5)
#plt.subplot(2,1,1)
mpf.plot(data, type='candle', title=symbol, style='yahoo', figratio=(25,10))
#plt.subplot(2,1,2)
#plt.plot(rsi_df['Date'],rsi_df['rsi'])
#plt.plot(rsi_df['Date'],rsi_df['30s'],linestyle='dotted', linewidth=3, color='#9598a1')
#plt.plot(rsi_df['Date'],rsi_df['70s'],linestyle='dotted', linewidth=3, color='#9598a1')
#plt.fill_between(rsi_df['Date'],rsi_df['30s'], rsi_df['70s'], color='#232237')

plt.show()
## Moving Average
mpf.plot(data, type='line', figratio=(25,10))
mpf.plot(data, type='candle', mav=(200,21), figratio=(25,10), title=symbol, style='yahoo')
mpf.show()
