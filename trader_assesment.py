# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 15:35:38 2022
Data closest to laplace distrobution... work with later
@author: SeanSteele
"""

import os
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler
import tqdm
from datetime import timedelta, date

os.chdir('C:\\Users\\SeanSteele\\Desktop\\Random Trader\\simulation_results')

'''
Data extraction
'''
#%% 
#extract list of all stock names
os.chdir('C:\\Users\\SeanSteele\\Desktop\\Random Trader')

stock_names = pd.read_csv('Stock_List.csv')


#generate dataframe to hold stock cloes
def daterange_generate(start_date, end_date, form):
    dates_list = []
    for i in range(int ((end_date - start_date).days)+1):
        date_time = start_date + timedelta(i)
        dates_list.append(date_time.strftime(form))
    return dates_list

start = date(2015, 12, 20)
end = date(2022, 8, 11)

dates = daterange_generate(start, end, "%Y-%m-%d")

stock_data = pd.DataFrame(dates, columns=['Date'])

#loop through all stock data files
path = 'C:\\Users\\SeanSteele\\Desktop\\Random Trader\\StockHistory'
directory = os.listdir(path)

os.chdir(path)

for file in tqdm(directory):
    #extract file temporarily
    temp = pd.read_csv(file)
    #extract name of file
    sep = '.'
    name = file.split(sep,1)[0]
    #merge file to stock data
    stock_data = pd.merge(stock_data, temp[['Date', 'Close']], on = 'Date', how = 'left')
    stock_data = stock_data.rename(columns={stock_data.columns[-1]: name})


stock_data2 = stock_data
#drop non-trading days (first column has full data coverage)
stock_indexes = stock_data[['Date','A']]
#merge the rest of stock data to indexes
stock_data2.reset_index(inplace = True)
stock_indexes.reset_index(inplace = True)

stock_data3 = pd.merge(stock_indexes, stock_data, on = 'index', how = 'left')

stock_data3.to_csv("C:\\Users\\SeanSteele\\Desktop\\Random Trader\\all_stock_close.csv")

# data prep for testing 
data = pd.read_csv('all_stock_close.csv')
#Drop all who don't have full data coverage
dat = data.iloc[0:1670,:]
dat = dat.dropna(axis = 1)
#Drop stocks < $2 and > $50 on both the start and end of data set
new_dat = dat['Date'].to_frame()
for i in range(1,dat.shape[1]):
    if (dat.iloc[0,i] < 50 and dat.iloc[0,i] > 2) and (dat.iloc[1013,i] < 50 and dat.iloc[1013,i] > 2):
        new_dat = pd.concat([new_dat,dat.iloc[:,i]], axis = 1)
        
new_dat.to_csv("C:\\Users\\SeanSteele\\Desktop\\Random Trader\\train_data.csv")     

#%%
'''
Assess Random Trader
'''
#%%
def extractor(string, delim1= 'upper_', delim2 = '_lower_', delim3 = '.csv'):
    string_start = string
    #split inital file string at markers
    string1 = string_start.split(delim1)
    string2 = string1[1].split(delim2)
    string3 = string2[1].split(delim3)
    #save wanted portions
    upper = string2[0]
    lower = string3[0]
    return upper, lower

#use glb package to get all csvs in a folder
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
  
#loop over files
def read_multi_csv(csv_files):
    df_list = []
    for file in csv_files:
        df = pd.read_csv(file)
        df_list.append(df)
    return df_list

df_list = read_multi_csv(csv_files)

#extract mean, std, and percentage over and under markers
means = []
per_under = []
per_under_25 = []
per_over_25 = []
st_dev = []
uppers = []
lowers = []
hist_frames = []

for i in range(1,len(df_list)):
    #extract upper and lower values of paramters
    upper_, lower_ = extractor(csv_files[i])
    uppers.append(float(upper_))
    lowers.append(float(lower_))
    #remove outliers and extract metrics
    df = df_list[i]
    df.drop(columns = df.columns[0], axis = 1, inplace = True)
    df_clean = df[df['per_returns'] < 1]
    means.append(df_clean['per_returns'].mean())
    st_dev.append(df_clean['per_returns'].std())
    per_under_zero = df_clean[df_clean['per_returns'] < 0].count(axis = 1).sum()/len(df_clean)
    per_under.append(per_under_zero)
    per_under_25_ = df_clean[df_clean['per_returns'] < -0.25].count(axis = 1).sum()/len(df_clean)
    per_under_25.append(per_under_25_)
    per_over_25_ = df_clean[df_clean['per_returns'] > 0.25].count(axis = 1).sum()/len(df_clean)
    per_over_25.append(per_over_25_)
    #build probability densities
    counts, bins = np.histogram(df_clean[df_clean['per_returns'] < 1], bins = 100)
    bins = bins[1:]
    hist_frame = pd.DataFrame({'counts' : counts,'bins' : bins})
    total = hist_frame['counts'].sum()
    #calculate probsbalities
    hist_frame['prob'] = hist_frame['counts']/total
    hist_frames.append(hist_frame)
#turn lists into one dataframe for assessment
ass_frame = pd.DataFrame({'upper' : uppers,
                          'lower' : lowers,
                          'mean' : means,
                          'std' : st_dev,
                          'neg_chance' : per_under,
                          'neg_25' : per_under_25,
                          'pos_25' : per_over_25})
scaler_mean = MinMaxScaler()
scaler_neg = MinMaxScaler()

scaler_mean.fit(ass_frame['mean'].to_numpy().reshape(-1,1))
scaler_neg.fit(ass_frame['neg_chance'].to_numpy().reshape(-1,1))

ass_frame['scaled_return'] = scaler_mean.transform(ass_frame['mean'].to_numpy().reshape(-1,1))
ass_frame['scaled_neg_chance'] = scaler_neg.transform(ass_frame['neg_chance'].to_numpy().reshape(-1,1))
ass_frame['goal'] = -ass_frame['scaled_return'] + ass_frame['scaled_neg_chance']


def plotter(df_list, index, ass_frame, density = True, annualize = True, color = 'g'):
    #extract clean dataframe
    df = df_list[index]
    df_clean = df[df['per_returns'] < 1]
    #plot histogram
    df_clean.hist(bins = 100, density = True)
    #calc formatting metrics
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    y_space = ymax * 0.1
    x_space = xmax * 0.1
    #calc plot values
    mean_returns = ass_frame['mean'].iloc[index]
    neg_chance = ass_frame['neg_chance'].iloc[index]
    ann_return = ((1+mean_returns)**2) - 1
    #plot values
    plt.text((mean_returns + x_space), (ymax - y_space), "Mean return " + str(round(mean_returns * 100,1)) +'%', ha='left')
    plt.text((mean_returns + x_space), (ymax - 2*y_space), "Negative return " + str(round(neg_chance * 100,1)) +'% chance', ha='left')
    plt.axvline(mean_returns, color=color)
    plt.grid(False)
    plt.xlabel('Percent Returns')
    plt.ylabel('Probability of Each Bin')
    plt.title('Histogram of 100 bins ' + str(index))
    if annualize == True:  
        plt.text((mean_returns + x_space), (ymax - 3*y_space), "Annual return " + str(round(ann_return * 100,1)) +'%', ha='left')
    plt.show()


#scan through hist frames to simulate trading periods

def iterated_returns(hist_frames, n_years, density = 10000, bank_init = 5000):
    ann_returns = []
    returns_distrobution = []
    avg_returns = []
    #loop over each distrobution
    for k in range(len(hist_frames)):
        data = hist_frames[k]
        #randomly sample returns (bins) over a period of 10 years (20 draws) m times
        samples = []
        #run m number samples from that density
        print(k)
        for j in tqdm.tqdm(range(density)):
            bank = bank_init
            for i in range(n_years * 2):
                sample = data.sample(n=1, replace = True, weights = 'prob', axis = 0)
                sample_return = sample['bins'].values[0] + 1
                bank = sample_return * bank
            samples.append(bank)
        
        #save the average returns
        samples_frame = pd.DataFrame(samples)
        average_return = samples_frame.mean()/5000
        ann_return = (1+average_return.values[0])**(1/10) - 1
        ann_returns.append(ann_return)
        returns_distrobution.append(samples_frame)
        avg_returns.append(average_return.values[0])
    return ann_returns, avg_returns, returns_distrobution

ann_oneyear_returns, oneyear_returns, oneyear_distros = iterated_returns(hist_frames, 1, 5000)
ann_threeyear_returns, threeyear_returns, threeyear_distros = iterated_returns(hist_frames, 3, 5000)
ann_fiveyear_returns, fiveyear_returns, fiveyear_distros = iterated_returns(hist_frames, 5, 5000)



five_year_min = []
five_year_max = []
per_under_5 = []
for i in range(len(fiveyear_distros)):
    five_year_min.append(fiveyear_distros[i].min().values[0])
    five_year_max.append(fiveyear_distros[i].max().values[0])
    under_zero = fiveyear_distros[i][fiveyear_distros[i].iloc[:,0] < 5000].count(axis = 1).sum()/5000
    per_under_5.append(under_zero)


ass_frame['min_5year'] = five_year_min
ass_frame['max_5year'] = five_year_max
ass_frame['under_0_5year'] = per_under_5


ass_frame['year_return'] = oneyear_returns
ass_frame['3year_return'] = threeyear_returns
ass_frame['5year_return'] = fiveyear_returns

frame1 = ass_frame[ass_frame['upper'] == 60]
frame2 = ass_frame[ass_frame['lower'] == 60]
frame3 = ass_frame[ass_frame['upper'] < 60]
frame3 = frame3[frame3['lower'] < 60]

frame3 = frame3[frame3['upper'] > 0.04]

frame4 = frame3.set_index('lower')
frame4.groupby('upper')['under_0_3year'].plot(legend = True)



#subset to comfortable realistic
comfy = ass_frame[ass_frame['3year_return'] > 1.73]
comfy = comfy[comfy['upper'] > 0.07]
comfy = comfy[comfy['lower'] > 0.1]
#plot all
for i in range(len(df_list)):
    plotter(df_list, i, ass_frame)

scatter_dat = ass_frame[ass_frame['upper'] < 1]

plt.scatter(scatter_dat['lower'], scatter_dat['mean'])


##
scat = scatter_dat[scatter_dat['upper'] == 0.02]
plt.scatter(scat['lower'], scat['mean'])


fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
plot = ax.scatter(scatter_dat['upper'], scatter_dat['lower'], scatter_dat['mean'])
ax.set_xlabel('upper')
ax.set_ylabel('lower')
ax.set_zlabel('return')
plt.show()





(threeyear_distros[0].mean() - 5000)/ 5000

man = threeyear_distros[0]

for i in range(len(fiveyear_distros)):
    data = fiveyear_distros[i][fiveyear_distros[i] < 30000]
    data.hist(bins = 100)
    plt.axvline(5000, color='red')
    plt.title(i)
    plt.show()




#fit laplace distrobution... its ok, but the bootstrapped simulations likely as good/better
data1 = df_list[38]
data1 = data1[data1['per_returns'] < 1]
ae, loce = stats.laplace.fit(data1['per_returns'])
  
# Plot the histogram.
plt.hist(data1['per_returns'], bins=100, density=True, alpha=0.6, color='b')
  
# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.laplace.pdf(x,ae, loce)
  
plt.plot(x, p, 'k', linewidth=2)
  
plt.show()





