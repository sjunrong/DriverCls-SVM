import pandas as pd

from Code.Data import kegg_drivers
from Code.model_training_cross import selector, shuffle_index
from Code.rank import results

selected_features = selector.get_support(indices=True)
selected_feature_names = results.columns[1:-1][selected_features]
# 得到筛选后result的数据
selected_data = results.iloc[shuffle_index, 1:-1].iloc[:, selected_features]
selected_data.columns = selected_feature_names

# 保存SHAP可解释分析需要的数据
selected_data_index = results.iloc[shuffle_index, 0]
selected_data_subtype = results.iloc[shuffle_index, -1]
# 合并以上数据，获得最终筛选得到的数据，用于模型训练
combined_data = pd.concat([selected_data_index, selected_data, selected_data_subtype], axis=1)
combined_data.to_csv("THCA_shapdata.csv", index=False)

# 对筛选后的数据进行整体排序
overall = pd.DataFrame(selected_data.sum()).T
overall.columns = selected_data.columns
# 给DataFrame设置行名
overall.index = ['overall']
# 对result进行降序排序
sorted_overall = overall.sort_values(by='overall', axis=1, ascending=False)
# 对sorted_overall的列名和systems求交集
inter = set(sorted_overall.columns).intersection(set(kegg_drivers))
sorted_overall.loc['IsDriver'] = sorted_overall.columns.isin(kegg_drivers).astype(int)
sorted_overall.to_csv('THCA_second_select.csv', index=False)
print("stop")