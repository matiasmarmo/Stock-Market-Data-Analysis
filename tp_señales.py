import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mpl_dates
import numpy as np

##Get params
symbol = input('Enter Stock symbol (default: AAPL): ') or 'AAPL'
period1 = int(time.mktime(datetime.datetime(2021, 7, 1, 23, 59).timetuple()))
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
#data = data.set_index('Date')

#print(data)
#data['period'] = range(1,len(data)+1)
rsi_df = data.loc[:, ['Close']]
rsi_df['period'] = range(1,len(rsi_df)+1)
rsi_df = rsi_df.set_index('period')
rsi_df['diff'] = rsi_df.diff(1)
print(rsi_df)
rsi_df['gain'] = rsi_df['diff'].clip(lower=0)
rsi_df['loss'] = rsi_df['diff'].clip(upper=0).abs()
print(rsi_df)

# Get initial Averages
window_length = 14
rsi_df['avg_gain'] = rsi_df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
rsi_df['avg_loss'] = rsi_df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
print(rsi_df)
# Get WMS averages
# Average Gains
for i, row in enumerate(rsi_df['avg_gain'].iloc[window_length+1:]):
    rsi_df['avg_gain'].iloc[i + window_length + 1] =(rsi_df['avg_gain'].iloc[i + window_length] * (window_length - 1) + rsi_df['gain'].iloc[i + window_length + 1]) / window_length
for i, row in enumerate(rsi_df['avg_loss'].iloc[window_length+1:]):
    rsi_df['avg_loss'].iloc[i + window_length + 1] = (rsi_df['avg_loss'].iloc[i + window_length] * (window_length - 1) + rsi_df['loss'].iloc[i + window_length + 1]) / window_length
print(rsi_df)
# Calculate RS Values
rsi_df['rs'] = rsi_df['avg_gain'] / rsi_df['avg_loss']
print(rsi_df)
# Calculate RSI
rsi_df['rsi'] = 100 - (100 / (1.0 + rsi_df['rs']))
rsi_df['30s'] = [30] * len(rsi_df)
rsi_df['70s'] = [70] * len(rsi_df)
rsi_df['Date'] = data['Date']
print(rsi_df)
#plt.style.use('dark_background')
plt.figure(figsize=(12, 6))
plt.rcParams['axes.facecolor'] = '#181c27'
plt.grid(color='#9598a1', linestyle='-', linewidth=0.5)
#plt.subplot(2,1,1)
#mpf.plot(data, type='candle', title=symbol, style='yahoo')
#plt.subplot(2,1,2)
plt.plot(rsi_df['Date'],rsi_df['rsi'])
plt.plot(rsi_df['Date'],rsi_df['30s'],linestyle='dotted', linewidth=3, color='#9598a1')
plt.plot(rsi_df['Date'],rsi_df['70s'],linestyle='dotted', linewidth=3, color='#9598a1')
plt.fill_between(rsi_df['Date'],rsi_df['30s'], rsi_df['70s'], color='#232237')

plt.show()
## Moving Average
#mpf.plot(data, type='line')
#mpf.plot(data, type='candle', mav=(20,10), figratio=(20,10), title=symbol, style='yahoo')
