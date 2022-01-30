import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
#from synthetic_tests_lib import crosscorr

# Time lagged cross correlation
def crosscorr(datax, datay, lag=0):
    """ Lag-N cross correlation.
    Shifted data filled with NaNs

    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length
    Returns
    ----------
    crosscorr : float
    """
    return datax.corr(datay.shift(lag))

def generate_dataset():
    ##Get params
    symbol = input('Enter Stock symbol (default: AAPL): ') or 'AAPL'
    period1 = int(time.mktime(datetime.datetime(2020, 4, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2021, 11, 26, 23, 59).timetuple()))
    interval = input('Enter interval (default: 1d):') or '1d'

    ## Get market stock data
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    ## Extracting Data for plotting
    df = pd.read_csv(query_string)
    print(df)
    data = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    data['Date'] = pd.to_datetime(data['Date'])
    print(data)
    data.to_csv(path_or_buf='data/' + symbol + '.txt',sep='\t')
    return symbol


dataset1 = generate_dataset()
dataset2 = generate_dataset()
time_series = [dataset1, dataset2]
#time_series = ['BO.NOK', 'BO.ABU']
dirName = "data/"
#fs = 748  # take 748 samples only
MR = len(time_series)
#Create array 2 rows x 748 columns
#Y = np.zeros((MR, fs))
#Initialize empty dictionary
dictVals = {}

for ind, series in enumerate(time_series):
    filename = dirName + series + ".txt"
    df = pd.read_csv(filename, usecols=['Close'], delimiter='\t')  # reading file as pandas dataframe to work easily
    #df = pd.read_csv(filename, names=['time', 'U'], skiprows=1, delimiter='\s+')
    print('------')
    print(df)
    # this code block is required as the different time series has not even sampling, so dealing with each data point separately comes handy
    # can be replaced by simply `yvalues = df['U]`
    yvalues = []
    #for i in range(1, fs+1):
    #    val = df.loc[df['time'] == i]['U'].values[0]
    #    yvalues.append(val)
    for i in df.index:
        val = df['Close'][i]
        yvalues.append(val)

    dictVals[time_series[ind]] = yvalues


timeSeriesDf = pd.DataFrame(dictVals)

print(timeSeriesDf)

#-----------------

d1, d2 = timeSeriesDf[time_series[0]], timeSeriesDf[time_series[1]]
print(d1)
#window = 10
#lags = np.arange(-(fs), (fs), 1)  # uncontrained
lags = np.arange(-(200), (200), 1)  # contrained
rs = np.nan_to_num([crosscorr(d1, d2, lag) for lag in lags])

print("xcorr {}-{}".format(time_series[0], time_series[1]), lags[np.argmax(rs)], np.max(rs))

print(type(time_series[0]))
print(type(rs))

# plot time series
# simple `timeSeriesDf.plot()` is a quick way to plot
fig, ax = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
ax[0].plot(timeSeriesDf[time_series[0]], color='b', label=time_series[0])
ax[0].legend()
ax[1].plot(timeSeriesDf[time_series[1]], color='r', label=time_series[1])
ax[1].legend()
#ax[2].plot(rs, color='g',label='Lag: ' + str(lags[np.argmax(rs)]) + ' | Correlación: ' + str(np.max(rs)))
ax[2].plot(rs, color='g',label='Lag: ' + str(lags[np.argmin(rs)]) + ' | Correlación: ' + str(np.min(rs)))
ax[2].legend()
plt.show()