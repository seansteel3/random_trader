# random_trader
Does Wall Street really do better than a small scale "investor" investing completely at random?


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Introduction](#introduction)
  * [Run With](#run-with)
* [Methods](#methods)
* [Results](#results)
* [References](#references)


<!-- Introduction -->
## Introduction

The stock market is arguably the first big data problem, and has drawn investors, academics, and novices alike for hundreds of years. Today it’s easier than ever before to both analyze the stock market and play your hand in it as an investor. However, despite the sheer number of minds and resources invested into “solving the market” its unclear if the efficient market hypothesis can ever truly be beaten in the long run.

A famous statement from economist Burton Malkiel’s book A Random Walk Down Wall Street states “A blindfolded monkey throwing darts at a newspaper could select a portfolio that would do just as well as one carefully selected by experts.” 

This project aims to step into the monkey’s shoes, and find out how true Malkiel’s statement is in the modern investing environment. More specifically, this phase of the project investigates if smaller scale “retail investor monkey” could compete with the Wall Street giants.  

<!-- Run With -->
### Run With

Python 3.9.7
* pandas
* numpy
* sklearn
* scipy
* Amazon EC2
* Amazon Cloud9 - Python 3.10

<!-- Methods-->
## Methods
Data was sourced from US Stock Data Kaggle dataset, which incorporates 7000+ US stocks, indices, mututal funds, bond funds, and ETFs between 2015 and the current date. These securities were subset between Jan 1st, 2015, and Aug 8th, 2022. Then securities less than $2 and greater than $50 at the start of the dataset were excluded. Exclusion cut offs were set since securities under $2 often have restricted trading, and securities over $50 would potentially be difficult for a small-scale retail investor to purchase with a small bank allocation.

Securities were randomly incorporated into a portfolio to be held for a set amount of time, then sold. The number of securities chosen for a given portfolio was varied from 5 – 25 in increments of 5, and then in increments of 25 up to 150. Porfolio bank allocations were split evenly. Securities were sold after either 180 days or 365 days. Each portfolio was initialized with random securities of their given number and allowed to start at random anywhere within the data set. 2,000 portfolios for each condition above were initialized as a baseline.

The random trader rules were then upgraded to include stop loss and limit orders at certain percentage thresholds from the purchase price. If the price hit a threshold, the trader would sell and replace the security at random. For these experiments portfolios were allotted 15 securities and would sell the entire portfolio after 180 days. The baseline random trader was simulated 20,000 times for comparison, and each percentage threshold was simulated 7,500 times. See parms.csv for more information on thresholds.

For time considerations, the stop loss and limit order experiments were run on Amazon EC2 instances controlled from Amazon’s Cloud9 IDE running in a Python 3.10 environment.


<!-- Results-->
## Results
Given a bank allocation of $5000 dollars split evenly between securities, a trader buying securities at random would maximize returns by holding between 10-15 securities. For portfolios larger than 20 securities, average returns drop steadily and portfolios larger than 50 have negative expected returns.  

A possible explanation for this phenomenon may be because smaller portfolios can ride on one or two “lucky” securities that do extremely well, despite the fact the majority tend to yield no returns or poor returns. However, larger portfolios spread the funds too thin, diluting the effect of “lucky” securities.

* It should be noted that all metrics were calculated after removing returns greater than 100%, since returns of this magnitude greatly bias the average metrics and only make up less than 0.5% of simulations. 

![image](https://user-images.githubusercontent.com/67161057/187779367-ec9ac866-cde5-4a5e-966f-b9c8d7a560b2.png)  ![image](https://user-images.githubusercontent.com/67161057/187806308-dd21ba7a-c18a-4049-a8c3-235d13923d6c.png)

The chance of a random portfolio having negative returns is inversely proportional to the size of the portfolio. Additionally, across all portfolio construction parameters, the general return distribution and skew of the distribution remained the same. This fact is observed throughout all simulations during this project. 

![image](https://user-images.githubusercontent.com/67161057/187779531-a3fb9950-2960-4624-b499-eed319e45cc3.png)  ![image](https://user-images.githubusercontent.com/67161057/187806313-1772591d-626d-4b8a-9555-e48aeffd6b2a.png)

Returns after 180 days (5.5% average with 15 securities, annualized by formula to 11.3%, annualized by resampling to 10.7%) nearly match returns after 365 days (12.8% average with 15 securities). Further the rough distribution at 365 days is nearly, but imperfectly, recovered when randomly sampling from the 180 days distribution twice 5000 times. This imperfect recovery is not surprising since selling all owned stocks and replacing them 2x a year will undoubtably be somewhat different than holding them for a full year. Its more surprising how close the recovered and actual distributions are, potentially implying that the amount of time holding a security may be less important when trading at random.

![image](https://user-images.githubusercontent.com/67161057/187808829-0a8fec28-7816-4853-be60-2d890b3e5058.png)     ![image](https://user-images.githubusercontent.com/67161057/187809467-43cc59bc-f9b8-4bbc-8c22-a641a876ab5d.png)

With base portfolio parameters roughly established, next portion of the project aimed to improve upon a truly random trader by setting commonly used stop loss and limit orders to sell and replace securities. To establish a baseline for comparison, the basic random trader was simulated 20,000 times with the chosen parameters of 15 securities, split evenly across a $5000 allocation, and held for 180 days before being sold. 

Simulating this baseline random trader 20,000 times gave higher density coverage of the randomly chosen start dates, improving the coverage of any temporal variances in the dataset. Additionally, these simulations improved the confidence in the average, median, and chance of a negative return metrics, since all these metrics asymptotically approach their true values. On average, a random trader is expected to make 5.5% returns and has a roughly 40.4% chance of negative returns after 180 days. Sampling from this distrobution after 1 year, the expected returns are about 13% and the chance of negative return reduces to about 33%, while after 5 years expected returns are about 84% and the chance of negative returns reduces to about 18%.

![image](https://user-images.githubusercontent.com/67161057/187761224-afb1226a-70e0-442a-9010-fbc0ba96a01f.png)

![image](https://user-images.githubusercontent.com/67161057/188166957-e97d8be4-a64d-4512-8f84-d9a5f8b0a289.png)

![image](https://user-images.githubusercontent.com/67161057/188166995-6787be40-82fe-4a62-aeec-34c281e683e1.png)

To assess the impact of setting various stop loss and limit order thresholds, 81 conditions (detailed in the parms.csv file; note thresholds set to 60 equate to no stop loss or limit order) were each simulated 7,500 times. To save time, the 81 conditions and simulations were split between two Amazon EC2 instances running C5.4xLarge machines totaling 32 parallel CPUs. Instances were controlled from a Cloud9 IDE python 3.10 environment. 

Setting no upper threshold for a sell limit order (ie: no selling when the security increases in price), has no effect on average returns until the threshold is set to greater than 25%. Then there is a roughly linear decrease in average return and increase negative return probability. Further investigation is required, but this suggests that securities may tend to rebound from drops as much as 25%. Alternatively, it may suggest that a few “lucky” securities are able to mitigate taking losses on losers by up to 25%. However, these suggestions should be taken with caution, since the number of securities that drop by greater than 30% within 180 days is small (~10%).

![image](https://user-images.githubusercontent.com/67161057/187971650-d64b6ecd-bb8e-4e2f-b948-c0aa160eb820.png)  ![image](https://user-images.githubusercontent.com/67161057/187971866-7d6aa135-1f4b-4bd8-95f0-db36bc9bef01.png)

On the other hand, setting no lower threshold for a stop loss order (ie: No selling when securities decrease in price) has a sharp decline in average returns initially, that nearly level off around a 10% threshold. However, the probability of negative returns increases nearly linearly as the threshold increases. This possibly suggests that securities tend to frequently increases in price by about 2%, and selling and replacing them frequently may both mitigate losses and increase profit potential. This is further emphasized by the roughly linear increase in negative returns, further suggesting that securities may not increase in price about 4% enough to prevent overall losses elsewhere.

![image](https://user-images.githubusercontent.com/67161057/187971699-def61abb-8e4a-4794-b0c8-5d8995e827d7.png) ![image](https://user-images.githubusercontent.com/67161057/187971915-bae54d64-41e5-439c-8def-f2f35f43937c.png)

When holding upper thresholds for limit orders constant, in general, the average returns tend to increase logarithmically, while the chance of negative returns are roughly constant. These observations imply that taking losses on securities may not be ideal, especially since the maximum expected returns tend to be higher when the trader is instructed to simply not sell when securities drop (1.0 on the AXIS of the charts represent no selling). 

Additionally, the trend observed above holds true across all lower threshold conditions. The cyan 1.0 line is the same “no limit order” line from the charts above, and at nearly every point it under performs other stop loss threshold conditions. This observation further reinforces the idea that taking profits when they arise will yield better returns, while taking losses tends to be only mildly beneficial or not beneficial.

![image](https://user-images.githubusercontent.com/67161057/187977775-5cb59c09-f0a3-4bb5-a7f8-b1afba3111a2.png) ![image](https://user-images.githubusercontent.com/67161057/187978138-c7c12021-a34b-41cf-9006-1cb52777cd9a.png)

When holding lower thresholds for stop loss orders constant, in general, the average returns and chance of negative returns tend to decrease logarithmically and increase linearly respectively. These observations reinforce the idea that taking frequent gains when they arise is more beneficial than waiting for the security to increase in value. This may also imply that securities tend to either fluctuate or increase in value in smaller increments, rather than make larger positive price changes. 

![image](https://user-images.githubusercontent.com/67161057/187977596-52d25839-ad8a-493f-912b-5ea5521a2f60.png) ![image](https://user-images.githubusercontent.com/67161057/187979964-50fd798d-b54d-48d6-9575-c6078d48be15.png)

The cyan lines across these charts (no limit or no stop loss orders) all point to the same conclusion: in general, its best to sell when securities go up and hold when securities go down. 

Interestingly, across all the conditions tested, selling securities at any limit or stop loss threshold outperforms a true random trader. This indicates that replacing “losing” securities in hopes of finding a “winner” does tend to find such winners. However, this, coupled with the fact that taking frequent small gains yields better returns, also indicates that there may not be many largescale “winners” in the market. But rather that the market in general tends to incrementally increase in value, even if individual securities may decrease.

To assess long term expected returns, the best limit and stop loss thresholds were randomly sampled 12,500 times over multiple periods. However, our hypothetical small scale “monkey retail investor” may not be able to closely monitor and sell securities, which frequently fluctuate by 2-4% within a day or less. In fact, many trading platforms actively discourage or even restrict selling securities within one day.

To give this hypothetical “monkey retail investor” some “breathing room,” threshold conditions were set to be no lower than 8%. With this breathing room, the highest average returns and lowest negative return chance is unsurprisingly set at an 8% upper threshold for limit orders, and no stop loss orders. Following these rules, one can expect returns of 9.7% and a 26.4% chance of negative return in any single 180 day trading period.

The 1-, 3-, and 5-year returns and respective chance of negative returns were estimated from 12,500 simulations, sampling the single 180 day trading period 2, 6 and 10 times respectively.

Between January 2015 and August 2022, giving a random small scale “monkey retail investor” $5000 split between 15 securities and selling them all after 6 months, or if they rise above 8%, after 1 year, the expected return is equal to about 21% and negative return chance equal to about 20%. While after 5 years, the expected return exceeded 160% with only a 4% chance of a negative return. Nearly double the returns of the baseline random trader.

While these distributions are increasingly left skewed as time marches on, they make it evident that a random trader, following a small list of rules can indeed be successful in the stock market in the long run. In fact, its unlikely that an investor would lose in the stock market in the long run following these simple rules. 

![image](https://user-images.githubusercontent.com/67161057/188001552-4c905dde-a7e6-4b66-a278-22637c7082ad.png)

![image](https://user-images.githubusercontent.com/67161057/188001597-5c51bc2f-8532-4455-9de7-0028fb6eb1fa.png)

![image](https://user-images.githubusercontent.com/67161057/188001648-ae006a77-f9e4-4e9d-a46a-e78b12086ec8.png)

More impressively, these simple random trading rules beat the S&P 500’s annualized returns (7.62%) during the same time frame. 

Considering the expected performance of our hypothetical “monkey retail investor”, the Wall Street hedge funds no longer seem as impressive. Over the last 3 years, largest hedge fund, Bridgewater Associates, has consistently failed to match even the S&P with annualized returns of less than 2.5%. Other hedge funds, such as Berkshire Hathaway manage to narrowly beat the market over the last 3 years with annualized returns of 15%, while others like Citadel Advisors and Point72 don’t even hit 10% annualized returns.

Of course, certain funds such as Renaissance Technologies’s Medallion fund have managed an annualized return of 66% since 1988. However, funds like these are very much the exception rather than the norm. 

While the few funds like the Medallion Fund certainly challenge the Efficient Market Hypothesis, it is not clear that Wall Street truly does better than our “monkey retail investor.” What’s even more damming to the Wall Street hedge funds is the fact that if we return to our baseline random “monkey retail investor” with no stop loss and limit orders, but allow it to trade any securities over $2, the average returns after 1 year increase to 17% with only a 12% chance of negative returns. After five years the average returns increase from about 84% to over 120% with less than 0.5% chance of negative returns. Meanwhile, over the same time period hundreds of hedge funds have negative 5 year returns.

![image](https://user-images.githubusercontent.com/67161057/188175613-884654ed-e0ea-4399-a926-fc71eac9b83a.png)

![image](https://user-images.githubusercontent.com/67161057/188175640-f9e11953-1bc6-4662-9c87-0ac49fafb1ec.png)


However, an important caveat should be noted. All the data used to construct these distributions occur between January 1st, 2015, and August 8th, 2022. Therefore, to extrapolate these results to any other time window, one must assume the general stock market and any other relevant economic trends are the same as this window. For example, during this time window the Federal Funds Rate was at an all-time low, a pandemic related economic collapse and subsequent recovery occurred. These likely had a large impact on the expected returns. Further, all data used for trading in these simulations was security closing price. Applying these rules to buying and selling at other timepoints may yeild vastly different results, and could even possibly explain why hedge funds in general seem to do substantially worse than this random trader.

Next directions of this project include obtaining a wider date range of data, as well as incorporating a series of temporal cross validation tests to assess the issues mentioned in the previous paragraph. Additionally, this project mainly looked at a small scale “retail investor monkey,” the next steps include looking into how an “institutional investor monkey” may perform, as well as a more detailed analysis of hedge fund performance.

<!-- References-->
## References

* A Random Walk Down Wall Street
* https://www.kaggle.com/datasets/footballjoe789/us-stock-dataset
* https://www.officialdata.org/us/stocks/s-p-500/2015
* https://hedgefollow.com/funds/Bridgewater+Associates/Performance-History
