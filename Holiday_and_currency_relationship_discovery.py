### Holiday and currency relationship discovery

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df1 = pd.read_csv("Projects/Seasonal signals project/BBD_GBP 2022-2024.csv", encoding='ISO-8859-1')
df1["Date"] = pd.to_datetime(df1["Date"], dayfirst=True)
df1 = df1.sort_values("Date")
df2 = pd.read_csv("Projects/Seasonal signals project/UK Tourist arrivals in Barbados 2022-2024.csv", encoding='ISO-8859-1')

plt.figure(0, figsize=(10,5))
plt.plot(df1["Date"], df1["Close"])
plt.xlabel("Date")
plt.ylabel("BBD/GBP")
plt.title("BBD/GBP 2022-2024")
plt.grid(True)
ax1 = plt.gca()
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() #plot of BBD/GBP over time

df1["Monthly return"] = df1["Close"].pct_change(periods=23)*100 #adding columns of monthly returns and comparison dates,
df1["Monthly return comparison date"] = df1["Date"].shift(23) #using monthly returns as we looked arrivals per month

bins_1 = []
i = np.ceil(df1["Monthly return"].min()-1)
while i < df1["Monthly return"].max()+1:
    bins_1.append(i)
    i += 1
plt.figure(1)
plt.hist(df1["Monthly return"],bins=bins_1,edgecolor="white")
plt.xlabel("Return")
plt.ylabel("Frequency")
plt.title("Monthly return histogram")
plt.show() #histogram of monthly returns and their frequency

high_monthly_return_dates = []
monthly_return_mean = df1["Monthly return"].mean()
monthly_return_std = df1["Monthly return"].std()
for (index, monthly_return) in df1["Monthly return"].items():
    if monthly_return >= monthly_return_mean + monthly_return_std:
        high_monthly_return_dates.append(df1.loc[index, "Date"])
    #identifies days with a monthly return at least one std above the mean (data is quite symmetric so mean is appropiate I believe)

df3 = pd.DataFrame({"Date":high_monthly_return_dates})
df3["Month number"] = df3["Date"].dt.month
df3["Month"] = df3["Date"].dt.strftime("%b")
month_count_1 = df3.groupby("Month number")["Month"].count()
month_count_1.index = [pd.to_datetime(str(m), format='%m').strftime('%b') for m in month_count_1.index]

plt.figure(2, figsize=(10,7))
month_count_1.plot(kind="bar")
plt.xlabel("Month")
plt.ylabel("Frequency")
plt.title("Number of days with a monthly return at least one standard deviation above the mean")
s_1 = f"Mean:{round(monthly_return_mean,4)}\nStd:{round(monthly_return_std,4)}\nMean+Std:{round(monthly_return_mean+monthly_return_std,4)}"
plt.text(x=0.8, y=0.9, s=s_1, fontsize=12, transform=plt.gca().transAxes)
plt.show() #plots a histogram with category of month and the frequency of days with a monthly return at least one std above the mean

#September, May and October have the most days in the 3 year period with a monthly return at least one std above the mean (28,19,17 respectively)
#
#This could imply that going long in August/September/April will be profitable (comparison is one month before the date)
#
#Note: The mini-budget was announced in September 2022 and resulted in a large spikes in GBP currency ratios

low_monthly_return_dates = []
for (index, monthly_return) in df1["Monthly return"].items():
    if monthly_return <= monthly_return_mean - monthly_return_std:
        low_monthly_return_dates.append(df1.loc[index, "Date"]) #identifies days with a monthly return at least one std below the mean 

df4 = pd.DataFrame({"Date":low_monthly_return_dates})
df4["Month number"] = df4["Date"].dt.month
df4["Month"] = df4["Date"].dt.strftime("%b")
month_count_2 = df4.groupby("Month number")["Month"].count()
month_count_2.index = [pd.to_datetime(str(m), format='%m').strftime('%b') for m in month_count_2.index]

plt.figure(3, figsize=(10,7))
month_count_2.plot(kind="bar")
plt.xlabel("Month")
plt.ylabel("Frequency")
plt.title("Number of days with a monthly return at most one standard deviation below the mean")
s_2 = f"Mean:{round(monthly_return_mean,4)}\nStd:{round(monthly_return_std,4)}\nMean-Std:{round(monthly_return_mean-monthly_return_std,4)}"
plt.text(x=0.4, y=0.9, s=s_2, fontsize=12, transform=plt.gca().transAxes)
plt.show() #plots a histogram with category of month and the frequency of days with a monthly return at least one std below the mean

#November, December, and April have the most days in the 3 year period with a monthly return at least one std below the mean (26,25,13 respectively)
#
#This could imply that going short in October/November/March will be profitable
#
#The results from the histograms may agree with thesis in that ratio begins to rise before holiday the season (August/September) 
# and begins to fall at the end/after holiday season (March)
#
#Can also indicate ratio falls after tourists arrive because they have already exchanged their GBP for BBD meaning demand decreases for BBD (November)
#
#However, BBD/USD is fixed (found this out way too late) so price movements due to UK holidaymakers may be restricted

df2["Month middle"] = pd.to_datetime(df2["Year"].astype(str) + "-" + (df2["Month number"]).astype(str) + "-15")
fig, ax1 = plt.subplots(figsize=(12,8))
ax1.plot(df1["Date"], df1["Monthly return"], color="blue")
ax1.set_ylabel("Monthly Return", color="blue")
ax2 = ax1.twinx()
ax2.plot(df2["Month middle"], df2["UK Tourist arrivals"], color="red", marker="o")
ax2.set_ylabel("Tourist Arrivals", color="red")
plt.title("Monthly Returns vs Monthly Tourist Arrivals")
plt.show()

#The sharpest increase in monthly tourist arrivals occurs between months October and November 
# and the sharpest decline in monthly tourist arrivals occur between months March and April
#
#Before sharp increases in monthly tourist arrivals, monthly returns are positive (September, October) 
# and after sharp declines in monthly tourist arrivals, monthly returns are negative (April)
#
#Could develop a profitable trading strategy based on this, signal is the time of year

 