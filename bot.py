import telebot
#Импорт библиотек
import yfinance as yf
import yahoofinancials
import investpy
import pandas as pd
import numpy as np 
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import date
import datetime as dt
plt.style.use('fivethirtyeight') # специальное отображение графиков для pyplot
import bot
from telebot import types

stock = ''
country = ''


bot = telebot.TeleBot('1572280128:AAFKQ4J9is5lwb3ivvcaJ-EmdhPjEIjonE4')


def Stock_SMA(stock,country):
    ''' stock - stock exchange abbreviation; country - the name of the country'''
    #Read data
    current_date = str(date.today().day) + '/'+ str(date.today().month) +'/' + str(date.today().year)
    try:
        #try:
            df = investpy.get_stock_historical_data(stock = stock,country = country,from_date='01/01/2019',to_date=current_date)
        #except Failed download:
            #print('fail') 

    except:
        df = yf.download(stock,start ='2019-01-01',end = date.today(),progress=False)

    #Count SMA30 / SMA90
    SMA30 = pd.DataFrame()
    SMA30['Close Price'] = df['Close'].rolling(window = 30).mean()
    SMA90 = pd.DataFrame()
    SMA90['Close Price'] = df['Close'].rolling(window = 90).mean()
    data = pd.DataFrame()
    data['Stock'] = df['Close']
    data['SMA30'] = SMA30['Close Price']
    data['SMA90'] = SMA90['Close Price']
    
    # Визуализируем 
    plt.figure(figsize = (12.6,7))
    plt.plot(data['Stock'], label = stock )
    plt.plot(SMA30['Close Price'], label = 'SMA30',alpha = 0.5)
    plt.plot(SMA90['Close Price'], label = 'SMA90',alpha = 0.5)
    plt.title(stock + ' history (SMA)')
    plt.xlabel('01/01/2019 - '+ current_date)
    plt.ylabel('Close price')
    plt.legend(loc = 'upper left')
    plt.savefig('C:/Users/Admin/Desktop/telegram_bot/test/SMA.png')
    #plt.show()




def Stock_EMA(stock,country):
    ''' stock - stock exchange abbreviation; country - the name of the country'''
    #Read data
    current_date = str(date.today().day) + '/'+ str(date.today().month) +'/' + str(date.today().year)
    try:
        df = investpy.get_stock_historical_data(stock = stock,country = country,from_date='01/01/2019',to_date=current_date)
    except:
        df = yf.download(stock,start ='2019-01-01',end = date.today(),progress=False)
    #Count EMA20 / EMA60
    EMA20 = pd.DataFrame()
    EMA20['Close Price'] = df['Close'].ewm(span=20).mean()
    EMA60 = pd.DataFrame()
    EMA60['Close Price'] = df['Close'].ewm(span=60).mean()
    data = pd.DataFrame()
    data['Stock'] = df['Close']
    data['EMA20'] = EMA20['Close Price']
    data['EMA60'] = EMA60['Close Price']
    
    # Визуализируем 
    plt.figure(figsize = (12.6,7))
    plt.plot(data['Stock'], label = stock)
    plt.plot(EMA20['Close Price'], label = 'EMA30',alpha = 0.5)
    plt.plot(EMA60['Close Price'], label = 'EMA60',alpha = 0.5)
    plt.title(stock + ' history (EMA)')
    plt.xlabel('01/01/2019 - '+ current_date)
    plt.ylabel('Close price')
    plt.legend(loc = 'upper left')
    plt.savefig('C:/Users/Admin/Desktop/telegram_bot/test/EMA.png')
    #plt.show()
    

def Upper_levels(stock,country):
    current_date = str(date.today().day) + '/'+ str(date.today().month) +'/' + str(date.today().year)
    try:
        df = investpy.get_stock_historical_data(stock = stock,country = country,from_date='01/01/2019',to_date=current_date)
    except:
        df = yf.download(stock,start ='2019-01-01',end = date.today(),progress=False)

    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [0,0,0,0,0,0,0,0,0,0]
    dateRange = [0,0,0,0,0,0,0,0,0,0]

    for i in df.index:
        currentMax = max(Range,default = 0)
        value = round(df['High'][i],2)

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(Range,default = 0):
            counter+=1
        else:
            counter =0
        if counter == 5:
            lastPivot=currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]
            pivots.append(lastPivot)
            dates.append(lastDate)


    timeD = dt.timedelta(days=30)

    plt.figure(figsize = (12.6,7))
    plt.title(stock + ' history (upper levels)')
    plt.xlabel('01/01/2019 - '+ current_date)
    plt.ylabel('Close price')
    plt.plot(df['High'], label = stock ,alpha = 0.5)
    for index in range(len(pivots)):
        plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],pivots[index]], linestyle ='-',linewidth = 2,marker = ",")
    plt.legend(loc = 'upper left')
    plt.savefig('C:/Users/Admin/Desktop/telegram_bot/test/Upper.png') 
    #plt.show()
    #print('Dates / Prices of pivot points:')
    #for index in range(len(pivots)):
    #    print(str(dates[index].date())+': '+str(pivots[index]))
        



def Low_levels(stock,country):
    current_date = str(date.today().day) + '/'+ str(date.today().month) +'/' + str(date.today().year)
    try:
        df = investpy.get_stock_historical_data(stock = stock,country = country,from_date='01/01/2019',to_date=current_date)
    except:
        df = yf.download(stock,start ='2019-01-01',end = date.today(),progress=False)

    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [999999]*10
    dateRange = [0,0,0,0,0,0,0,0,0,0]

    for i in df.index:
        currentMin = min(Range,default = 0)
        value = round(df['Low'][i],2)

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMin == min(Range,default = 0):
            counter+=1
        else:
            counter =0
        if counter == 5:
            lastPivot=currentMin
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]
            pivots.append(lastPivot)
            dates.append(lastDate)


    timeD = dt.timedelta(days=30)

    plt.figure(figsize = (12.6,7))
    plt.title(stock + ' history (low levels)')
    plt.xlabel('01/01/2019 - '+ current_date)
    plt.ylabel('Close price')
    plt.plot(df['Low'], label = stock ,alpha = 0.5)
    for index in range(len(pivots)):
        plt.plot_date([dates[index],dates[index]+timeD],[pivots[index],pivots[index]], linestyle ='-',linewidth = 2,marker = ",")
    plt.legend(loc = 'upper left')
    plt.savefig('C:/Users/Admin/Desktop/telegram_bot/test/Low.png') 
    #plt.show()
    #print('Dates / Prices of pivot points:')
    #for index in range(len(pivots)):
    #    print(str(dates[index].date())+': '+str(pivots[index]))




def Last_Month(stock,country):
    current_date = str(date.today().day) + '/'+ str(date.today().month) +'/' + str(date.today().year)
    try:
        df = investpy.get_stock_historical_data(stock = stock,country = country,from_date='01/01/2019',to_date=current_date)
    except:
        df = yf.download(stock,start ='2019-01-01',end = date.today(),progress=False)
    plt.figure(figsize = (12.6,7))
    plt.plot(df['Close'][-30:], label = stock ,alpha = 0.5)
    plt.title(stock + ' history last 30 days')
    plt.xlabel('Last 30 days')
    plt.ylabel('Close price')
    plt.legend(loc = 'upper left')
    plt.savefig('C:/Users/Admin/Desktop/telegram_bot/test/Mounth.png')
    #plt.show()



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Доброго времени суток! Какую акцию будем оценивать сегодня?', reply_markup=keyboard1)
    print ('start')
    print(message.from_user.first_name)
    print(message.from_user.last_name)
    print(message.from_user.username)
    print(message.from_user)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Провести анализ акции')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'здравствуй'  :
        bot.send_message(message.chat.id, 'Доброго дня!')
        print('hello')
        
    elif message.text.lower() == 'пока' or message.text.lower() == 'досвидания'  :
        bot.send_message(message.chat.id, 'До встречи!')
        print('good day')
    elif message.text.lower() == 'провести анализ акции':
        bot.send_message(message.chat.id, 'введите тикер')
        bot.register_next_step_handler(message,reg_stock)
        print('analis')

    else:
        print(message.from_user.username)
        print(message.text)
        bot.send_message(message.chat.id, 'я вас не понимаю')
        print('dontunderstanded')



def reg_stock(message):
    global stock 
    print (message.text)
    stock = message.text
    #print (stock)
    bot.send_message(message.chat.id, 'введите страну и немного подождите')
    bot.register_next_step_handler(message,reg_country)
    

    Stock_SMA(stock,country)
    Stock_EMA(stock,country)
    Upper_levels(stock,country)
    Low_levels(stock,country)
    Last_Month(stock,country)

    SMA_img = open('C:/Users/Admin/Desktop/telegram_bot/test/SMA.png', 'rb')
    EMA_img = open('C:/Users/Admin/Desktop/telegram_bot/test/EMA.png', 'rb')
    Upper_img = open('C:/Users/Admin/Desktop/telegram_bot/test/Upper.png', 'rb')
    Lower_img = open('C:/Users/Admin/Desktop/telegram_bot/test/Low.png', 'rb')
    Mounth_img = open('C:/Users/Admin/Desktop/telegram_bot/test/Mounth.png', 'rb')

    bot.send_photo(message.chat.id, SMA_img)
    bot.send_photo(message.chat.id, EMA_img)    
    bot.send_photo(message.chat.id, Upper_img)
    bot.send_photo(message.chat.id, Lower_img)
    bot.send_photo(message.chat.id, Mounth_img)


def reg_country(messege):

    global country 
    country = messege.text
    print(messege.text)


bot.polling()