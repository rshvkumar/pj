import pandas as pd
import numpy as np


exNames = ['storeNumber','avgWeeklyDelOrders','avgWeeklyDelWaitTime','avgResDensityByTract','avgWalkByTract']
df = pd.read_excel("paredDownMergedDataSetCensusAndPJ.xlsx",0,0,names=exNames)

meanWait = df['avgWeeklyDelWaitTime'].mean()
df['avgWeeklyDelWaitTime'].fillna(value=meanWait,inplace=True)

sumDelOrders = df['avgWeeklyDelOrders'].sum()
sumWait = df['avgWeeklyDelWaitTime'].sum()
sumDensity = df['avgResDensityByTract'].sum()
sumWalkability = df['avgWalkByTract'].sum()

df["normAvgWeeklyDelOrders"] = df["avgWeeklyDelOrders"] / sumDelOrders
df["normAvgWeeklyDelWaitTime"] = df["avgWeeklyDelWaitTime"] / sumWait
df["normAvgResDensityByTract"] = df["avgResDensityByTract"] / sumDensity
df["normAvgWalkByTract"] = df["avgWalkByTract"] / sumWalkability

#Analytic Hierarchy Process - weight calculations for MADM
    #Weekly delivery orders - 0.093797
    #Delivery wait time - 0.555884
    #Residential density - 0.064315
    #Walkability - 0.286005

weightDelOrders = 0.093797
weightWait = 0.555884
weightDensity = 0.064315
weightWalkability = 0.286005

df["weightedNormDelOrders"] = df["normAvgWeeklyDelOrders"] * weightDelOrders
df["weightedNormWait"] = df["normAvgWeeklyDelWaitTime"] * weightWait
df["weightedNormDensity"] = df["normAvgResDensityByTract"] * weightDensity
df["weightedNormWalkability"] = df["normAvgWalkByTract"] * weightWalkability

df["preferenceScore"] = df["weightedNormDelOrders"] + df["weightedNormWait"] + df["weightedNormDensity"] + df["weightedNormWalkability"] 
#df["Ranking"] = df.groupby("storeNumber")["preferenceScore"].rank(ascending=False)
df.to_excel("Iter1Ranking.xlsx")

# df = df.dropna()

# from skcriteria.madm import simple
# #https://scikit-criteria.readthedocs.io/en/latest/_modules/skcriteria/madm/simple.html#WeightedProductModel
#https://readthedocs.org/projects/scikit-criteria/downloads/pdf/latest/
# dm = simple.WeightedProductModel()
# dec = dm._evaluate_data(df, [2,5,2.5,4.5],[max, max, max, max])

# rank = dec[0] #ndarray
# dfRank = pd.DataFrame(rank)
# dfRank.to_excel("FILERank.xlsx")
# scores = dec[1] #dictionary
# dfScore = pd.DataFrame(scores)
# dfScore.to_excel("FILEScore.xlsx")



