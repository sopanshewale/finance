'''Works Best on Python3 '''

import urllib.request
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt



def pull_data_for_stock(stock):
    '''This pulls data from yahoo finance api
    returns close, high, low, open & volume data lists'''

    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1y/csv'
    #print ("Data from URL: " + url)
    with urllib.request.urlopen(url) as f:
        source = f.read().decode('utf-8')
    split_source = source.split('\n')
    day    = []
    close  = []
    high   = []
    low    = []
    open_p   = [] 
    volume = []
    
    for line in split_source:
        if re.search('^\d+', line):
            (d, c, h, l, o, v) = line.split(",")
            day.append(d)
            close.append(c)
            high.append(h)
            low.append(l)
            open_p.append(o)
            volume.append(v)
            
        #print (line)
    return [day, close, high, low, open_p, volume]

def get_dates(d_list):
    '''Helps covert day field to datetime date object'''
    d_strings = [d[4:6] + '/' + d[6:8] + '/' + d[0:4] for d in d_list] 
    return [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in d_strings]

def draw_chart(days, prices, graph_type):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.xlabel("Trading Days")
    plt.ylabel("Stock Price")
    plt.title(graph_type)
    plt.plot(days,prices)
    plt.gcf().autofmt_xdate()
    plt.show()

my_data = pull_data_for_stock('GOOG')
#correct dates 
days = get_dates(my_data[0])
draw_chart(days, my_data[1], "Closing Price Chart")

