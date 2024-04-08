import pandas as pd

# from Code.Data import symbols
from Code.Random_walk import result


# 对每个样本特征列进行排序
sorted_df = result.iloc[:, 1:-1].apply(lambda x: x.rank(ascending=False, method='min'), axis=1)
sorted_df.columns = result.columns[1:-1]
# 创建新表格
binary_df = pd.DataFrame(index=result.index, columns=result.columns)
binary_df.iloc[:, 0] = result.iloc[:, 0]  # 指定第一列数据为原表格第一列的数据

# 遍历每一行数据，并根据特征数据是否在排名前80中，将新表格中的值置为1或0
for i in range(len(result)):
    indices = sorted_df.iloc[i, :].sort_values().argsort()[:80]
    binary_df.loc[i, indices.index] = 1
    binary_df.loc[i, binary_df.columns[1:-1].difference(indices.index)] = 0

# 删除全0的行和列
binary_df = binary_df.loc[:, (binary_df != 0).any(axis=0)]
binary_df = binary_df.loc[(binary_df != 0).any(axis=1), :]
# 指定最后一列数据为原表格最后一列的数据
binary_df.iloc[:, -1] = result.iloc[:, -1]
# 更新result中的特征数据
results1 = binary_df
column_name = binary_df.columns[1:-1]
# 将column_names转换为集合
column_name_set = set(column_name)

# # 将symbols的值转换为集合
# symbols_set = set(symbols)
# # 计算并集
# union = column_name_set | symbols_set
# # 交集
# intersection = symbols_set.intersection(column_name_set)

# 筛选出与symbols值重合的列
filtered_columns = [col for col in result.columns if col in column_name_set]
filtered_columns = [result.columns[0]] + filtered_columns + [result.columns[-1]]  # 保留第一列和最后一列
# 保留筛选后的列
results = result[filtered_columns]
print("第一次特征筛选结束")