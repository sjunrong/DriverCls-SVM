import os
import time
import numpy as np
import pandas as pd

from Code.Data import MutMatrix, OutMatrix, influenceGraph, df2

start_time = time.time()

a = 0.9
numinstance, numgene = MutMatrix.shape
influenceGraph = influenceGraph * 1.0

new_M = a * MutMatrix + (1-a) * np.dot(OutMatrix, influenceGraph.T)

new_O = a * OutMatrix + (1-a) * np.dot(new_M, influenceGraph)

new_M1 = a * MutMatrix + (1-a) * np.dot(new_O, influenceGraph.T)

# 对两个数据框的第一列进行交集操作, 获取交集数据
common_idx = pd.Index(new_M1.index).intersection(pd.Index(df2.iloc[:, 0]))
df1_common = new_M1.loc[new_M1.index.isin(common_idx)]
df1_common.insert(0, 'pan.samplesID', df1_common.index)
df1_common = df1_common.reset_index(drop=True)
df2_common = df2.loc[df2.iloc[:, 0].isin(common_idx)]
# 将列名一致
# df1_common = df1_common.rename(columns={'Unnamed: 0': '0'})
df2_common = df2_common.rename(columns={'Unnamed: 0': 'pan.samplesID'})
# 将两个交集数据框拼接起来生成一个新的数据框
result = pd.merge(df1_common, df2_common, on=df1_common.columns[0], how='inner')
print("随机游走结束")