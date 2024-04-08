import os

import numpy as np
import pandas as pd

data_dir = "../Data"
# 获取文件InfluenceGraph
influenceGrap_path = os.path.join(data_dir, "InfluenceGraph_Sig_Fls_inter_vstCNV.csv")
influenceGraph = pd.read_csv(influenceGrap_path, index_col=0)
Influ_index = influenceGraph.index
Influ_columns = influenceGraph.columns
# 获取文件MutMatrix
MutMatrix_path = os.path.join(data_dir, "MutMatrix_Sig_Fls_inter_vstCNV.csv")
MutMatrix = pd.read_csv(MutMatrix_path, index_col=0)
MutMatrix = MutMatrix.reindex(columns=Influ_index)
# 获取文件OutMatrix
OutMatrix_path = os.path.join(data_dir, "OutMatrix_Sig_Fls_inter_vstCNV.csv")
OutMatrix = pd.read_csv(OutMatrix_path, index_col=0)
OutMatrix = OutMatrix.reindex(columns=Influ_columns)

df2_path = os.path.join(data_dir, "THCA_histological_Subtype.csv")
df2 = pd.read_csv(df2_path, header=0)
df2 = df2.rename(columns={"histological_type": "Subtype"})
df2 = df2.dropna(subset=["Subtype"])
# 创建字典将类别映射为数字
mapping = {'Classical/usual': 1, 'Follicular (>= 99% follicular patterned)': 2, 'Tall Cell (>= 50% tall cell features)': 3, 'Other  specify': 4}   # thyroid cancer
# mapping = {'Normal': 1, 'LumA': 2, 'Her2': 3, 'LumB': 4, 'Basal': 5}  # breast cancer
# mapping = {'CIN': 1, 'Invasive': 2, 'MSI/CIMP': 3}  # colon cancer
# 将第二列数据进行映射转换
df2['Subtype'] = df2['Subtype'].map(mapping)

# 读入表格
data_dir = "../Origin_Data"
df_path = os.path.join(data_dir, 'NCG_cancerdrivers_annotation_supporting_evidence.tsv.csv')
df = pd.read_csv(df_path, sep=',')

# 筛选出cancer_type列中值为甲状腺癌的数据
df1 = df[(df['cancer_type'] == 'anaplastic_thyroid_carcinoma')| (df['cancer_type'] == 'papillary_thyroid_cancer')| (df['cancer_type'] == 'parathyroid_carcinoma') | (df['primary_site'] == 'multiple')]
# df1 = df[(df['cancer_type'] == 'breast_cancer') | (df['primary_site'] == 'multiple')]
# df1 = df[(df['cancer_type'] == 'colorectal_adenocarcinoma') | (df['primary_site'] == 'multiple')]
# 取出symbol列中的数据，并去重
symbols = df1['symbol'].unique()

kegg_driver = df[(df['cancer_type'] == 'anaplastic_thyroid_carcinoma')| (df['cancer_type'] == 'papillary_thyroid_cancer')| (df['cancer_type'] == 'parathyroid_carcinoma')]
# kegg_driver = df[(df['cancer_type'] == 'breast_cancer')]
# kegg_driver = df[(df['cancer_type'] == 'colorectal_adenocarcinoma')]
kegg_drivers = kegg_driver['symbol'].unique()
print("数据准备结束")