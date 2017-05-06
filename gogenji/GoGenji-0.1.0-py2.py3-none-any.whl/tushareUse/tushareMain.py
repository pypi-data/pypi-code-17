print("STARTED .....")
from .addValue import *
from .Helper import *
from .Save import *
from tabulate import tabulate




def movie():
    movie = ts.realtime_boxoffice()
    movieDetail = ''
    for i in range(0, movie.shape[0]):
        rank = movie.iloc[i]['Irank']
        name = movie.iloc[i]['MovieName']
        sumBoxOffice = movie.iloc[i]['sumBoxOffice']
        boxPerMovie = movie.iloc[i]['boxPer']
        movieDay = movie.iloc[i]['movieDay']
        movieD = '['+ rank + ' '+ name + ' ' + 'day' + movieDay + '] '
        # movieD = rank + ' '+ name + ' ' + movieDay + '天'+ ' 总票房' + sumBoxOffice + ' 票房/影院' + boxPerMovie + '|'
        movieDetail = movieDetail+ movieD
    return movieDetail

'''Adding Columns to stock dataframe'''
# stock = addValue(stock, 'Daily Return')
# stock = addValue(stock, 'MACD')
# stock = addValue(stock,'Double-volume')

''' MATPLOT PLOT and SHOW and SAVE'''
# stock['close'].plot(legend=True ,figsize=(10,4))
# stock['Daily Return'] = stock['close'].pct_change()
# stock['Daily Return'].plot(legend=True,figsize=(10,4))
# stock['volume'].plot(legend=True,figsize=(8,4))
# stock[['MACD','9-day-signal-MACD']].plot(legend=True,figsize=(8,4))
# stock['Double-volume'].plot(legend=True,figsize=(8,4))
# saveImage(plt,1)

''' SAVE to WORD'''
# saveImagesToWord('Double-Volume',1)

''' SEABORN STYLE'''
# sns.set_style("whitegrid")

''' SEABORN  Plot & SAVE'''
# sns.kdeplot(stock['Daily Return'].dropna())
# sns.jointplot(stock['Daily Return'],stock['Daily Return'],alpha=0.2)
# sns_plot = sns.kdeplot(stock['Daily Return'])
# fig = sns_plot.get_figure()
# fig.savefig('Files/output.png')

''' PLOT SHOW '''
# plt.show()

''' TEST '''
# print(stock)
# print(movie)



