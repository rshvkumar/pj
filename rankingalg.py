import pandas as pd
import numpy as np


#exNames = ['StoreNumber','AvgWeeklyDeliveryVolume','AvgWeeklyWaitTime','AvgResidentialDensity','AvgWalkability','CrimeIndex']
df = pd.read_excel("slimMergedDataSetCensusAndPJ.xlsx",0,header = 0)
#print(df.head())
#Correlation delivery time to delivery volume = 0.11

maxDel = df["AvgWeeklyDeliveryVolume"].max()
maxWait = df["AvgWeeklyWaitTime"].max()
maxRes = df["AvgResidentialDensity"].max()
maxWalk = df["AvgWalkability"].max()
minCrime = df["CrimeIndex"].min()

meanWait = df['AvgWeeklyWaitTime'].mean()
df['AvgWeeklyWaitTime'].fillna(value=meanWait,inplace=True)

df["normAvgWeeklyDelOrders"] = df["AvgWeeklyDeliveryVolume"] / maxDel
df["normAvgWeeklyDelWaitTime"] = df["AvgWeeklyWaitTime"] / maxWait
df["normAvgResDensityByTract"] = df["AvgResidentialDensity"] / maxRes
df["normAvgWalkByTract"] = df["AvgWalkability"] / maxWalk
df["normCrimeIndex"] = minCrime * (1 / df["CrimeIndex"]) 

#Analytic Hierarchy Process - weight calculations for MADM
weightDelOrders = 0.060785
weightWait = 0.350558
weightDensity = 0.044688
weightWalkability = 0.274496
weightCrime = 0.269472

df["weightedNormDelOrders"] = df["normAvgWeeklyDelOrders"] * weightDelOrders
df["weightedNormWait"] = df["normAvgWeeklyDelWaitTime"] * weightWait
df["weightedNormDensity"] = df["normAvgResDensityByTract"] * weightDensity
df["weightedNormWalkability"] = df["normAvgWalkByTract"] * weightWalkability
df["weightedNormCrime"] = df["normCrimeIndex"] * weightCrime

#Weighted Sum Model
#https://www.youtube.com/watch?v=Kx8hpvhFm30
df["preferenceScore"] = df["weightedNormDelOrders"] + df["weightedNormWait"] + df["weightedNormDensity"] + df["weightedNormWalkability"] + df["weightedNormCrime"]
df.to_excel("Iter3Ranking.xlsx")



#df["Ranking"] = df.groupby("storeNumber")["preferenceScore"].rank(ascending=False)

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



