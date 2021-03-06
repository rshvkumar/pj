import pandas as pd
import numpy as np

# Intensity of Importance  /	Definition
# 1	Equal importance
# 3	Moderate importance
# 5	Strong importance
# 7	Very strong importance
# 9	Extreme importance
# 2, 4, 6, 8	Intermediate values
frac7 = 1/7
frac6 = 1/6

ahp = np.matrix([[1.0,7.0,5.0,2.0,frac6],
    [frac7,1.00,0.50,0.25,0.20],
    [0.20,2.0,1.0,0.2,0.2],
    [0.5,3.0,5.0,1.0,2.0],
    [6.0,5.0,5.0,0.5,1.0],])

ahpDf = pd.DataFrame(ahp, columns = ["Walkability", "ResidentialDensity", "DeliveryOrderVolume","CrimeIndex","WaitTime"])
ahpDf["normW"] = ahpDf['Walkability'] /  ahpDf['Walkability'].sum()
ahpDf["normRes"] = ahpDf['ResidentialDensity'] /  ahpDf['ResidentialDensity'].sum()
ahpDf["normDel"] = ahpDf['DeliveryOrderVolume'] /  ahpDf['DeliveryOrderVolume'].sum()
ahpDf["normC"] = ahpDf['CrimeIndex'] /  ahpDf['CrimeIndex'].sum()
ahpDf["normWait"] = ahpDf['WaitTime'] /  ahpDf['WaitTime'].sum()

ahpNormDf = ahpDf[["normW","normRes","normDel",'normC','normWait']]


ahpNormDf["Weights"] = ahpNormDf.mean(axis = 1)
#print(ahpNormDf.head())

#Analytic Hierarchy Process - weight calculations for MADM
weightWalkability = ahpNormDf["Weights"].iloc[0]
weightDensity = ahpNormDf["Weights"].iloc[1]
weightDelOrders = ahpNormDf["Weights"].iloc[2]
weightCrime = ahpNormDf["Weights"].iloc[3]
weightWait = ahpNormDf["Weights"].iloc[4]

#AHP analysis

ahpDf["weightedW"] = ahpDf['Walkability'] *  weightWalkability
ahpDf["weightedRes"] = ahpDf['ResidentialDensity'] * weightDensity
ahpDf["weightedVol"] = ahpDf['DeliveryOrderVolume'] * weightDelOrders
ahpDf["weightedCr"] = ahpDf['CrimeIndex'] * weightCrime
ahpDf["weightedWait"] = ahpDf['WaitTime'] * weightWait

weightedAHPDf = ahpDf[["weightedW","weightedRes","weightedVol","weightedCr","weightedWait"]]
weightedAHPDf["Weighted Row Sum"] = weightedAHPDf.sum(axis = 1)

lambdas = [weightedAHPDf["Weighted Row Sum"].iloc[0] / weightWalkability, weightedAHPDf["Weighted Row Sum"].iloc[1] / weightDensity, 
    weightedAHPDf["Weighted Row Sum"].iloc[2] / weightDelOrders, weightedAHPDf["Weighted Row Sum"].iloc[3] / weightCrime,
        weightedAHPDf["Weighted Row Sum"].iloc[4] / weightWait]
lambdaMax = sum(lambdas)/len(lambdas)

consistencyIndex = (lambdaMax - len(lambdas)) / (len(lambdas) - 1)

#Random index
#n	1	2	3	    4	5	    6	     7	     8	    9
#RI	0	0	0.58	0.9	1.12	1.24	1.32	1.41	1.45
consistencyRatio = consistencyIndex / 1.12
print(consistencyRatio)

#WSM
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


df["weightedNormDelOrders"] = df["normAvgWeeklyDelOrders"] * weightDelOrders
df["weightedNormWait"] = df["normAvgWeeklyDelWaitTime"] * weightWait
df["weightedNormDensity"] = df["normAvgResDensityByTract"] * weightDensity
df["weightedNormWalkability"] = df["normAvgWalkByTract"] * weightWalkability
df["weightedNormCrime"] = df["normCrimeIndex"] * weightCrime

#Weighted Sum Model
#https://www.youtube.com/watch?v=Kx8hpvhFm30
df["preferenceScore"] = df["weightedNormDelOrders"] + df["weightedNormWait"] + df["weightedNormDensity"] + df["weightedNormWalkability"] + df["weightedNormCrime"]
# df.to_excel("Iter3Ranking.xlsx")


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



