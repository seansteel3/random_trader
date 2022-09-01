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

The stock market is arguably the first big data problem, and has drawn investors, academics, and novices alike for hundreds of years. Today it’s easier than ever before to both analyze the stock market and play your hand in it as an investor. However, despite the sheer number of minds and resources invested into “solving the stock market” its unclear if the efficient market hypothesis can ever truly be beaten in the long run.

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
Data was sourced from US Stock Data Kaggle dataset, which incorporates 7000+ US stocks, indices, mututal funds, bond funds, and ETFs between 2015 and the current date. These stocks were subset between Jan 1st, 2015, and Aug 8th, 2022. Then stocks less than $2 and greater than $50 at the start of the dataset were excluded. Exclusion cut offs were set since stocks under $2 often have restricted trading, and stocks over $50 would potentially be difficult for a small-scale retail investor to purchase with a small bank allocation.

Stocks were then chosen at random and incorporated into a portfolio to be held for a set amount of time, then sold. The number of stocks chosen for a given portfolio was varied from 5 – 25 in increments of 5, and then in increments of 25 up to 150. Bank allocations were split evenly between stocks. Stocks were sold after either 180 days or 365 days. Each portfolio was initialized with random stocks of their given number and allowed to start at random anywhere within the data set. 2,000 portfolios for each condition above were initialized as a baseline.

The random trader rules were then upgraded to include stop loss and limit orders at certain percentage thresholds from the purchase price. If the price hit a threshold, the trader would sell and replace the security at random. For these experiments portfolios were allotted 15 stocks and would sell the entire portfolio after 180 days. The baseline random trader was simulated 20,000 times for comparison, and each percentage threshold was simulated 7,500 times. See parms.csv for more information on thresholds.

For time considerations, the stop loss and limit order experiments were run on Amazon EC2 instances controlled from Amazon’s Cloud9 IDE running in a Python 3.10 environment.


<!-- Results-->
## Results
Given a bank allocation of $5000 dollars split evenly between securities, a trader buying stocks at random would maximize returns by holding between 10-15 securities. For portfolios larger than 20 securities, average returns drop steadily and portfolios larger than 50 have negative expected returns. 

A possible explanation for this phenomenon may be because smaller portfolios can ride on one or two “lucky” securities that do extremely well, despite the fact the majority tend to yield no returns or poor returns. However, larger portfolios spread the funds too thin, diluting the effect of “lucky” securities.

![image](https://user-images.githubusercontent.com/67161057/187779367-ec9ac866-cde5-4a5e-966f-b9c8d7a560b2.png)  ![image](https://user-images.githubusercontent.com/67161057/187806308-dd21ba7a-c18a-4049-a8c3-235d13923d6c.png)

The chance of a random portfolio having negative returns is directly tied to the average return. Meaning the general distribution and skew of the distribution remains the same regardless of the specific portfolio construction parameters. This fact is observed throughout all simulations during this project. 

![image](https://user-images.githubusercontent.com/67161057/187779531-a3fb9950-2960-4624-b499-eed319e45cc3.png)  ![image](https://user-images.githubusercontent.com/67161057/187806313-1772591d-626d-4b8a-9555-e48aeffd6b2a.png)

Returns after 180 days (5.5% average with 15 securities, annualized by formula to 11.3%, annualized by resampling to 10.7%) nearly match returns after 365 days (12.8% average with 15 securities). Further the rough distribution at 365 days is nearly, but imperfectly, recovered when randomly sampling from the 180 days distribution twice 5000 times. This imperfect recovery is not surprising since selling all owned stocks and replacing them 2x a year will undoubtably be different than holding them for a full year.

![image](https://user-images.githubusercontent.com/67161057/187808829-0a8fec28-7816-4853-be60-2d890b3e5058.png)     ![image](https://user-images.githubusercontent.com/67161057/187809467-43cc59bc-f9b8-4bbc-8c22-a641a876ab5d.png)

With base portfolio parameters roughly established, next portion of the project aimed to improve upon a truly random trader by setting commonly used stop loss and limit orders to sell and replace securities. To establish a create baseline for comparison, the basic random trader was simulated 20,000 times with the chosen parameters of 15 securities, split evenly across a $5000 allocation, and held for 180 days before being sold. 

Simulating this baseline random trader 20,000 times gave higher density coverage of the randomly chosen start dates, improving the coverage of any temporal variances in the dataset. Additionally, these additional simulations improved the confidence in the average, median, and chance of a negative return metrics.


![image](https://user-images.githubusercontent.com/67161057/187761224-afb1226a-70e0-442a-9010-fbc0ba96a01f.png)


<!-- References-->
## References

* A Random Walk Down Wall Street
* https://www.kaggle.com/datasets/footballjoe789/us-stock-dataset
