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

This project aims to step into the monkey’s shoes, and find out how true Malkiel’s statement is in the modern investing environment.

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
Data was sourced from US Stock Data Kaggle dataset, which incorporates 7000+ US stocks and indices between 2015 and the current date. These stocks were subset between Jan 1st, 2015, and Aug 8th, 2022. Then stocks less than $2 and greater than $50 at the start of the dataset were excluded. Exclusion cut offs were set since stocks under $2 often have restricted trading, and stocks over $50 would potentially be difficult for a small-scale investor to purchase with a small bank allocation.

Stocks were then chosen at random and incorporated into a portfolio to be held for a set amount of time, then sold. The number of stocks chosen for a given portfolio was varied from 5 – 25 in increments of 5, and then in increments of 25 up to 150. Bank allocations were split evenly between stocks. Stocks were sold after either 180 days or 365 days. Each portfolio was initialized with random stocks of their given number and allowed to start at random anywhere within the data set. 2,000 portfolios for each condition were initialized as a baseline.

The random trader rules were then upgraded to include stop loss and limit orders at certain percentage thresholds from the purchase price. If the price hit a threshold, the trader would sell and replace the security at random. For these experiments portfolios were allotted 15 stocks and would sell the entire portfolio after 180 days. The baseline random trader was simulated 20,000 times for comparison, and each percentage threshold was simulated 7,500 times. See parms.csv for more information on thresholds.

For time considerations, the stop loss and limit order experiments were run on Amazon EC2 instances controlled from Amazon’s Cloud9 IDE. 


<!-- Results-->
## Results

![image](https://user-images.githubusercontent.com/67161057/187761224-afb1226a-70e0-442a-9010-fbc0ba96a01f.png)

![image](https://user-images.githubusercontent.com/67161057/187770046-8b832984-59c5-4666-901e-1ca3fa9ee3e3.png)

![image](https://user-images.githubusercontent.com/67161057/187770077-d2b7a5d7-9185-4314-86b4-4208d2f16fc0.png)


<!-- References-->
## References

* A Random Walk Down Wall Street
* https://www.kaggle.com/datasets/footballjoe789/us-stock-dataset
