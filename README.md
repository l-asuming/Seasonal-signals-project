# Seasonal-signals-project
Over the summer, I worked on a project in Excel and Python looking at whether holiday patterns could influence FX markets. I used Barbados as a case study, given its reliance on tourism and the large number of UK arrivals (though in hindsight, probably not the most optimal choice***), and tested whether holiday seasons is a signal that can be used for FX trading.

Approach
* Started in Excel, pulling UK arrival data from the Barbados Statistical Service and flagged peak travel periods from holiday agency sites
* Shifted into Python (pandas, NumPy, matplotlib) to build and backtest a simple seasonal strategy

Strategy tested
* Long BBD/GBP in Aug–Sep, Short BBD/GBP in Mar, Flat otherwise (2022–2024)
* Added a fixed stop-loss: pause trading if portfolio dropped by 0.375%+ in a week

Results
* The August–September longs produced positive returns in each year whereas the first short in March 2022 resulted in a loss
* Baseline seasonal strategy: annualised return ≈ 4.4%, Sharpe < 1
* With the stop-loss: annualised return ≈ 5.1%, Sharpe ≈ 1.2, smoother returns and smaller drawdowns

Caveats
* The BBD is pegged to the USD***, so any holiday-driven GBP/BBD moves fade quickly
* External shocks (e.g. Sept 2022 UK mini-budget) had large influence on results
* Assumed no trading costs and unlimited liquidity which was very unrealistic

I don’t consider this a tradable strategy for BBD/GBP, but I believe there could be other currency pairs where such an approach is more applicable. 

More importantly the process gave me useful experience in data handling, backtesting, and risk management in Python, skills I want to keep on developing throughout my journey into finance and tech. I would be happy to hear feedback/ideas, as I am keen to learn more about trading and research.
