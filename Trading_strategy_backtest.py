### Trading strategy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Assumptions for all strategy backtests (to keep it simple for me):
#
#1. No transaction costs - We assume trading occurs without commissions or fees
#
#2. Perfect liquidity – Trades can be executed instantly at the daily closing price of the currency pair
#
#3. Exposure only – Strategies reflect exposure of current wealth to the market, 
#we are not considering partial staking or allocation of a separate money “pot” 

df1 = pd.read_csv("Projects/Seasonal signals project/BBD_GBP 2022-2024.csv", encoding='ISO-8859-1')
df1["Date"] = pd.to_datetime(df1["Date"], dayfirst=True)
df1 = df1.sort_values("Date")

### Strategy 1

#Take a short position in March, a long position in August and September, and a flat position in all the other months
   
def seasonal_signal_1(Date):
    month_number = Date.month
   
    if month_number == 3:
        return -1
    if 8 <= month_number <= 9 :
        return 1
    else:
        return 0
    #-1 results in a short position, 0 results in a flat position and 1 results in a long position (see below ***)
   
df1["Signal 1"] = df1["Date"].apply(seasonal_signal_1) #applies the signal based on the date
df1["Daily return"] = df1["Close"].pct_change()
df1["Strategy return 1"] = df1["Signal 1"]*df1["Daily return"] #***
df1["Cumulative wealth 1"] = (1+df1["Strategy return 1"]).cumprod() #calculates cumulative wealth of strategy 1

cagr_1 = ((df1["Cumulative wealth 1"].iloc[-1])**(1/3)) - 1
volatility_1 = df1["Strategy return 1"].std() * np.sqrt(252)
sharpe_1 = cagr_1/volatility_1
wins_1 = [x for x in df1["Strategy return 1"] if x>0]
trades_1 = [x for x in df1["Strategy return 1"] if x!=0]
win_rate_1 = len(wins_1)/len(trades_1)
df1["Rolling max 1"] = df1["Cumulative wealth 1"].cummax()
df1["Drawdown 1"] = ((df1["Cumulative wealth 1"]-df1["Rolling max 1"])/df1["Rolling max 1"])
max_drawdown_1 = df1["Drawdown 1"].min() #calculations of key metrics of the first strategy

metrics_text_1 = (
    f"CAGR: {cagr_1*100:.2f}%\n"
    f"Sharpe: {sharpe_1:.2f}\n"
    f"Max Drawdown: {max_drawdown_1*100:.2f}%\n"
    f"Volatility: {volatility_1*100:.2f}%\n"
    f"Win rate: {win_rate_1*100:.2f}%")

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6), gridspec_kw={'width_ratios': [3, 1]})
ax1.plot(df1["Date"], df1["Cumulative wealth 1"], label="Cumulative Wealth 1", color='blue')
ax1.set_xlabel("Date")
ax1.set_ylabel("Cumulative Wealth 1")
ax1.set_title("Cumulative Wealth 2022-2024 Strategy 1")
ax1.grid(True)
ax1.legend()
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax1.get_xticklabels(), rotation=45)
ax2.axis('off')  
ax2.text(0, 0.5, metrics_text_1, fontsize=12, verticalalignment='center')
ax2.set_title('Key Metrics', pad=20)
plt.tight_layout()
plt.show() #plots the performance of the first strategy

### Strategy 1 reflections:
#
#Sharpe is below 1 which is not good (the risk of the investment is greater than the award)
#
#CAGR of 4.38 which means returns is a good as that of a savings account (not amazing)
#
#We gained money in the first two longs and one of the shorts, what would happen if we went long-only? 

### Strategy 2
 
#Take a short position in March, and a flat position in all the other months

def seasonal_signal_2(Date):
    month_number = Date.month
   
    if 8 <= month_number <= 9 :
        return 1
    else:
        return 0

df1["Signal 2"] = df1["Date"].apply(seasonal_signal_2) #code below is similar to code above, just a different signal applied
df1["Strategy return 2"] = df1["Signal 2"]*df1["Daily return"]
df1["Cumulative wealth 2"] = (1+df1["Strategy return 2"]).cumprod()

cagr_2 = ((df1["Cumulative wealth 2"].iloc[-1])**(1/3)) - 1
volatility_2 = df1["Strategy return 2"].std() * np.sqrt(252)
sharpe_2 = cagr_2/volatility_2
wins_2 = [x for x in df1["Strategy return 2"] if x>0]
trades_2 = [x for x in df1["Strategy return 2"] if x!=0]
win_rate_2 = len(wins_2)/len(trades_2)
df1["Rolling max 2"] = df1["Cumulative wealth 2"].cummax()
df1["Drawdown 2"] = ((df1["Cumulative wealth 2"]-df1["Rolling max 2"])/df1["Rolling max 2"])
max_drawdown_2 = df1["Drawdown 2"].min()

metrics_text_2 = (
    f"CAGR: {cagr_2*100:.2f}%\n"
    f"Sharpe: {sharpe_2:.2f}\n"
    f"Max Drawdown: {max_drawdown_2*100:.2f}%\n"
    f"Volatility: {volatility_2*100:.2f}%\n"
    f"Win rate: {win_rate_2*100:.2f}%")

fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14,6), gridspec_kw={'width_ratios': [3, 1]})
ax3.plot(df1["Date"], df1["Cumulative wealth 2"], label="Cumulative Wealth 2", color='blue')
ax3.set_xlabel("Date")
ax3.set_ylabel("Cumulative Wealth 2")
ax3.set_title("Cumulative Wealth 2022-2024 Strategy 2")
ax3.grid(True)
ax3.legend()
ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax3.get_xticklabels(), rotation=45)
ax4.axis('off')  
ax4.text(0, 0.5, metrics_text_2, fontsize=12, verticalalignment='center')
ax4.set_title('Key Metrics', pad=20)
plt.tight_layout()
plt.show()

### Strategy 2 reflections:
#
#Sharpe is very close to 1 (a bit better as we basically have a 1:1 risk-reward ratio)
#
#CAGR has decreased (sigh)
#
#Will keep in shorts and add a stop loss for next strategy

### Strategy 3

#Take a short position in March, a long position in August and September, and a flat position in all the other months
#
#Trading stops when weekly change in the portfolio (when using strategy 1) is -0.375% 
#(gives max CAGR and sharpe based on values I've tested), is a fixed-percentage stop loss

threshold =  -0.00375

def stop_loss_signal_3(pct_change_portfolio):
    if pct_change_portfolio <= threshold:
        return 0
    else:
        return 1 #trading stops when this function returns a 0 (see below ***) 

df1["Weekly percentage change in portfolio"] = df1["Cumulative wealth 1"].pct_change(periods=5)#this strategy basically updates strategy 1   
df1["Stop loss signal 3"] = df1["Weekly percentage change in portfolio"].apply(stop_loss_signal_3)#based on stop loss which is enabled the
df1["Signal 3"] = (df1["Signal 1"]*(df1["Stop loss signal 3"].shift(1)))#next day if triggered
df1["Strategy return 3"] = df1["Signal 3"]*df1["Daily return"] 
df1["Cumulative wealth 3"] = (1+df1["Strategy return 3"]).cumprod()

cagr_3 = ((df1["Cumulative wealth 3"].iloc[-1])**(1/3)) - 1 #code is now similar to above cases
volatility_3 = df1["Strategy return 3"].std() * np.sqrt(252)
sharpe_3 = cagr_3/volatility_3
wins_3 = [x for x in df1["Strategy return 3"] if x>0]
trades_3 = [x for x in df1["Strategy return 3"] if x!=0]
win_rate_3 = len(wins_3)/len(trades_3)
df1["Rolling max 3"] = df1["Cumulative wealth 3"].cummax()
df1["Drawdown 3"] = ((df1["Cumulative wealth 3"]-df1["Rolling max 3"])/df1["Rolling max 3"])
max_drawdown_3 = df1["Drawdown 3"].min()

metrics_text_3 = (
    f"CAGR: {cagr_3*100:.2f}%\n"
    f"Sharpe: {sharpe_3:.2f}\n"
    f"Max Drawdown: {max_drawdown_3*100:.2f}%\n"
    f"Volatility: {volatility_3*100:.2f}%\n"
    f"Win rate: {win_rate_3*100:.2f}%")

fig3, (ax5, ax6) = plt.subplots(1, 2, figsize=(14,6), gridspec_kw={'width_ratios': [3, 1]})
ax5.plot(df1["Date"], df1["Cumulative wealth 3"], label="Cumulative Wealth 3", color='blue')
ax5.set_xlabel("Date")
ax5.set_ylabel("Cumulative Wealth 3")
ax5.set_title("Cumulative Wealth 2022-2024 Strategy 3")
ax5.grid(True)
ax5.legend()
ax5.xaxis.set_major_locator(mdates.MonthLocator())
ax5.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax5.get_xticklabels(), rotation=45)
ax6.axis('off')  
ax6.text(0, 0.5, metrics_text_3, fontsize=12, verticalalignment='center')
ax6.set_title('Key Metrics', pad=20)
plt.tight_layout()
plt.show()

### Strategy 3 reflections:
#
#Sharpe is 1.23 now meaning the stop loss has helped with risk managment
#
#CAGR has increased to 5.12% (still not great but is better than a lot of savings accounts lol)
#
#Max drawdown has fallen quite a bit meaning our portfolio protected quite well against falls in the years 2022-2024

### Conclusion

# Would I trade this strategy with BBD/GBP?
#
# Probably not, as a large proportion of the returns in the period would have been due 
# to the chaos Liz Truss caused with her mini-budget, which made the pound really weak 
# and hence BBD/GBP rose sharply in that period.
#
# BBD is also pegged to USD (I wish I had found this out earlier)
# so even though minor price movements can occur purely based on holidaymakers, they would 
# have minimal effect. Essentially, we are trading USD/GBP.
#
# Some of the assumptions made wouldn't hold as well, especially perfect liquidity, 
# as this pair would be low volume compared to GBP/EUR, meaning wider spreads and 
# less profitability.
#
# However, I do think there could be some merit to the idea. If there exists a country 
# that is heavily reliant on tourism from another country, has a floating exchange rate, 
# and is relatively small (so other economic factors are minimal), then their currency 
# ratio could have a large link to holiday season, and a good trading strategy could 
# potentially be developed.
