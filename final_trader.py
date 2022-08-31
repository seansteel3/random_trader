"""
Created on Sun Aug 21 16:14:08 2022

AWS Code Random Trader

@author: SeanSteele
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from tqdm import tqdm
import math
import os
import matplotlib.pyplot as plt

os.chdir('C:\\Users\\SeanSteele\\Desktop\\Random Trader')

#import functions
def buy_bank(stock_name, data, date, bank, shares = 1):
    #subset to the date
    data2 = data[data['Date'] == date]
    #extract price of stock
    price = data2[stock_name] * shares
    #update bank
    new_bank = bank - price
    return new_bank.values[0]

def sell_bank(stock_name, data, date, bank, shares = 1):
    #subset to the date
    data2 = data[data['Date'] == date]
    #extract price of stock
    price = data2[stock_name].values[0] * shares
    #update bank
    new_bank = bank + price
    return new_bank.values[0]

def sell_all(data, date, bank, owned, shares = 1):
    for i in range(len(owned)- 1):
        bank = sell_bank(owned[i], data, date, bank, shares = shares)
    return bank

def uni_money_split(total, n_stocks):
    uni_split = total/n_stocks
    return uni_split

def uni_share_num(money_splt, stock_price):
    num_share = money_splt/stock_price
    return math.floor(num_share)
    
def share_price(data, stock, date):
    data2 = data[data['Date'] == date]
    return data2[stock].values[0]

def random_portfolio(data, start_amt, start_date, n_stocks, stock_list):
    n_stocks = n_stocks
    money_split = uni_money_split(start_amt, n_stocks)
    bank = start_amt
    #init owned list
    owned = []
    num_shares = []
    start_price = []
    #buy 10 stocks at random
    for i in range(0,n_stocks):
        #save name
        rand = random.randint(0, len(stock_list) - 1)
        name = stock_list.iloc[rand].values[0]
        owned.append(name)
        #reduce bank amount - if money available, else end
        share_cost = share_price(data, name, start_date)
        start_price.append(share_cost)
        share_num = uni_share_num(money_split, share_cost)
        num_shares.append(share_num)
        bank = buy_bank(name, data, start_date, bank, share_num)
        #save in a data frame
    portfolio = pd.DataFrame({'stock': owned,
                              'share_number': num_shares,
                              'start_price': start_price})
    portfolio['inital_investment'] = portfolio['share_number'] * portfolio['start_price']
    portfolio['start_date'] = start_date
    return portfolio, bank

def portfolio_prep(portfolio, upper_thresh, lower_thresh, n_days_hold):
    #calculate upper and lower bounds to sell at
    portfolio['upper'] = portfolio['start_price'] * (1 + upper_thresh)
    portfolio['lower'] = portfolio['start_price'] * (1 - lower_thresh)
    #calculate the nearest trading day after the end date
    portfolio['start_datetime'] = pd.to_datetime(portfolio['start_date'])
    portfolio['end_datetime'] = portfolio['start_datetime'] + timedelta(days = n_days_hold)
    portfolio['end_date'] = portfolio['end_datetime'].dt.strftime('%m/%d/%Y')
    return portfolio

def random_hold_v2(start_amt, start_date, n_stocks, n_days_hold, data, stock_list):
    #build a random portfolio of stocks
    portfolio, discard = random_portfolio(data = data, start_amt = start_amt, start_date = start_date, n_stocks = n_stocks, stock_list = stock_list)
    #calculate the nearest trading day after the end date
    portfolio['start_datetime'] = pd.to_datetime(portfolio['start_date'])
    portfolio['end_datetime'] = portfolio['start_datetime'] + timedelta(days = n_days_hold)
    portfolio['end_date'] = portfolio['end_datetime'].dt.strftime('%m/%d/%Y')
    #subset data to end date
    end_date = data[pd.to_datetime(data['Date']) > pd.to_datetime(portfolio['end_date'].iloc[0])]
    end_date = end_date.iloc[0,0]
    end_data = data[data['Date'] == end_date]
    #init holder for end prices and find end prices
    end_price = []
    for i in range(len(portfolio)):
        stock_name = portfolio['stock'].iloc[i]
        end_price.append(end_data[stock_name].values[0])
    #return dataframe with end prices and values for each stock
    portfolio['end_price'] = end_price
    portfolio['end_value'] = portfolio['end_price'] * portfolio['share_number']
    return portfolio

def random_hold_v3_1(start_amt, start_date, n_stocks, n_days_hold, upper_thresh, lower_thresh, data):
    #init a random portfolio
    portfolio, bank = random_portfolio(data = data, start_amt = start_amt, start_date = start_date, n_stocks = n_stocks, stock_list = stocks)
    #calculate upper and lower bounds
    portfolio = portfolio_prep(portfolio, upper_thresh, lower_thresh, n_days_hold)
    #sort by datetime after subsetting data to after start time
    data['date_time'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by = 'date_time', axis = 0)
    #subset data to only after start time and before end
    data2 = data[data['date_time'] > portfolio['start_datetime'].iloc[0]]
    data2 = data2[data2['date_time'] < portfolio['end_datetime'].iloc[0]]
    #loop through each day for each stock, if its at a threshold sell and replace
    for j in range(len(data2)):
        #subset data to current stocks
        current_stocks = portfolio['stock'].to_list()
        current_stocks.append('Date')
        current_stocks.append('date_time')
        data3 = data2[current_stocks]
        #subset to each day, then check each stock
        day = data3['date_time'].iloc[j]
        data4 = data3[data3['date_time'] == day]
        temp_portfolio = pd.DataFrame(columns = ['stock', 'share_number', 'start_price',
                                                 'inital_investment','start_date'])
        stock_drop = []
        for i in range(len(current_stocks) - 2):
            #is the value of the stock past a threshold
            stock_consider = current_stocks[i]
            porfolio_consider = portfolio[portfolio['stock'] == stock_consider]
            current_value = data4[stock_consider].values[0]
            check = (current_value > porfolio_consider['upper']).values[0] or (current_value < porfolio_consider['lower']).values[0]
            
            if check == True: #if the value is, sell at this price and add to a temp portfolio
                bank = sell_bank(stock_consider, data4, data4['Date'], bank, porfolio_consider['share_number'])
                #buy new random stock
                new_stock, bank = random_portfolio(data2, bank, 
                                                        data4['Date'].values[0], 
                                                        n_stocks = 1, stock_list = stocks)
                temp_portfolio = pd.concat([temp_portfolio,new_stock])
                stock_drop.append(stock_consider)
        if len(temp_portfolio) > 0: #if new stocks added, add to main portfolio and drop old stock
            temp_portfolio = portfolio_prep(temp_portfolio, upper_thresh, lower_thresh, n_days_hold)
            portfolio = pd.concat([portfolio, temp_portfolio])
            portfolio.reset_index(inplace = True, drop = True)
            portfolio.drop(portfolio[portfolio['stock'].isin(stock_drop)].index, inplace = True)
            portfolio.reset_index(inplace = True, drop = True)
    #bring in final date data
    final_data = data2[data2['Date'] == data3['Date'].iloc[-1]]
    final_stocks = portfolio['stock'].to_list()
    final_data = final_data[final_stocks]
    final_data = final_data.transpose().reset_index()
    final_data.columns =  ['stock', 'final_price']
    portfolio = pd.merge(portfolio, final_data, how = 'left', on = 'stock')
    return portfolio, bank


#import data
data = pd.read_csv('train_data.csv')
parm_df = pd.read_csv('parms.csv')
stocks = data.columns.to_frame()
stocks.columns = ['stock']
stocks = stocks.iloc[1:,:]

#import paramter dataframe
parm_df = pd.read_csv('parms.csv')

#loop through whole parms dataframe with V3 random hold
iteration_num = 7500

start_amt = 5000
stock_number = 15
n_days_hold = 180 
rand_days_cap = len(data) - n_days_hold - 5

returns_final = []
for j in range(10,11):
    dataframe_holder = []
    bank_holder = []
    for i in tqdm(range(0,iteration_num)):
        rand = random.randint(0,rand_days_cap)
        start = data['Date'].iloc[rand]
        portfolio, bank = random_hold_v3_1(start_amt, start, stock_number, n_days_hold,
                                       parm_df['upper_thresh'].iloc[j], parm_df['lower_thresh'].iloc[j], data)
        dataframe_holder.append(portfolio)
        bank_holder.append(bank)
    #build returns df for histogram of returns
    per_returns = []
    for i in range(len(dataframe_holder)):
        per_return = ((0 + 
                       (dataframe_holder[i]['final_price'] * dataframe_holder[i]['share_number']).sum() 
                       - start_amt))/start_amt
        per_returns.append(per_return)
    
    per_returns_df =pd.DataFrame(per_returns, columns = ['per_returns'])
    #store dataframe as list, add column to parms_df as final return
    returns_final.append(per_returns_df)
    #store results
    file_name = 'upper_' + str(parm_df['upper_thresh'].iloc[j]) + '_lower_' + str(parm_df['lower_thresh'].iloc[j]) + '.csv'
    returns_final[0].to_csv(file_name)
    
    
#other testing with V2 Random Hold - stock number optimization shown
iteration_num = 2000
start_amt = 5000
stock_number = [5, 10, 15, 20, 25, 50, 75, 100, 125, 150]
n_days_hold = 180 
rand_days_cap = len(data) - n_days_hold - 5

average_holder = []
std_holder = []
under0_holder = []
median_holder = []
for j in range(len(stock_number)):
    bank_holder = []
    for i in tqdm(range(0,iteration_num)):
        rand = random.randint(0,rand_days_cap)
        start = data['Date'].iloc[rand]
        portfolio = random_hold_v2(start_amt, start, stock_number[j], n_days_hold, data, stocks)
        bank_holder.append(portfolio)
    #build returns df for histogram of returns
    per_returns = []
    for i in range(len(bank_holder)):
        end_value = bank_holder[i]['end_value'].sum()
        per_return = ((end_value - start_amt))/start_amt
        per_returns.append(per_return)
    returns_df = pd.DataFrame(per_returns, columns = [['per_returns']])
    returns_df2 = returns_df[returns_df['per_returns'] < 1.0001]
    #compute average returns, returns under 0, and returns st dev
    average_holder.append(returns_df2.mean().values[0])
    std_holder.append(returns_df2.std().values[0])
    under_zero = returns_df2[returns_df2['per_returns'] < 0]
    under_zero.dropna(inplace = True)
    per_under = round(len(under_zero)/iteration_num, 3)
    under0_holder.append(per_under)
    median_holder.append(round(returns_df2['per_returns'].median(), 3))

plt.plot(stock_number, average_holder)
