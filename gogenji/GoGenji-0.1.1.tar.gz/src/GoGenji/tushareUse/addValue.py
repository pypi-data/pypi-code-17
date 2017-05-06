import pandas as pd

def addValue(stock,value):
    if value == 'Daily Return':
        dailyReturn = []
        for i in range(0, stock.shape[0]):  # pandas dataframe row count, column count is stock.shape[1]
            dailyR = (stock.iloc[i]['price_change'] / stock.iloc[i]['open'])
            dailyReturn.append(dailyR)
        dailyReturnSeries = pd.Series(dailyReturn)  # pandas dataframe add column
        stock['Daily Return'] = dailyReturnSeries.values

    if value == 'MACD':
        MACD = []
        Signal9Day = []
        EMA12 = []
        EMA26 = []
        EMA12Previous = 0
        EMA26Previous = 0
        signal9DayPrevious = 0
        for i in range(0, stock.shape[0]):
            closeP = stock.iloc[i]['close']
            EMA12Previous = closeP*2/(12+1)+ EMA12Previous*(1-2/(12+1))
            oneEMA12 = EMA12Previous
            EMA12.append(oneEMA12)
            EMA26Previous = closeP*2/(26+1)+ EMA26Previous*(1-2/(26+1))
            oneEMA26 = EMA26Previous
            EMA26.append(oneEMA26)
            oneMACD = oneEMA12 - oneEMA26
            MACD.append(oneMACD)
            signal9DayPrevious = oneMACD*2/(9+1) + signal9DayPrevious*(1-2/(9+1))
            oneSignal9Day = signal9DayPrevious
            Signal9Day.append(oneSignal9Day)
        stock['MACD'] = pd.Series(MACD).values# pandas dataframe add column
        stock['9-day-signal-MACD'] = pd.Series(Signal9Day).values# pandas dataframe add column

    if value == 'Double-volume':
        doubleVolume = []
        volumePrevious = 0
        for i in range(0, stock.shape[0]):
            volume = stock.iloc[i]['volume']
            if volumePrevious == 0:
                volumePrevious = volume
            if (volume/volumePrevious)>=2:
                doubleVolume.append(volume)
            else:
                doubleVolume.append(0)
            volumePrevious = volume
        stock['Double-volume'] = pd.Series(doubleVolume).values




    return stock


