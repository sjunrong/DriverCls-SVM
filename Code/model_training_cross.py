import time

import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, adjusted_rand_score, confusion_matrix, roc_curve, \
    roc_auc_score, hamming_loss, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# 分离样本和标签
from Code.Random_walk import start_time
from Code.rank import results

X = results.iloc[:, 1:-1].values
Y = results.iloc[:, -1:].values

# 数据标准化
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 打乱数据顺序
num_samples, num_features = X.shape
shuffle_index = np.random.permutation(num_samples)
X = X[shuffle_index, :]
Y = Y[shuffle_index]

# 使用SMOTE进行过采样
smote = SMOTE()
X, Y = smote.fit_resample(X, Y.ravel())

# 构建模型，并设置L1正则化惩罚项, 通过Logistic 回归模型和 L1 正则化一起进行特征选择
model = LogisticRegression(penalty='l1', solver='liblinear')
# 使用SelectFromModel进行特征选择
selector = SelectFromModel(model)
X_new = selector.fit_transform(X, Y)

# 获取被选择的特征索引
selected_features = selector.get_support(indices=True)
X = X[:, selected_features]

# 划分数据集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

end_time = time.time()
duration = end_time - start_time
print("数据处理时间：", duration, "秒")

# , 'linear', 'poly', 'sigmoid'
# 定义模型并进行参数搜索
params = {'kernel': ['rbf'],
          'C': np.logspace(-1, 4, 6),
          'gamma': np.logspace(-5, 0, 6)}
svm_model = SVC(decision_function_shape='ovo')
grid_search = GridSearchCV(svm_model, param_grid=params, cv=5, n_jobs=1)
grid_search.fit(X, Y)
# 使用交叉验证评估模型
ovo_classif = SVC(decision_function_shape='ovo', **grid_search.best_params_)
scores = cross_val_score(ovo_classif, X, Y, cv=5)

# 计算准确率（平均值）
accuracy1 = scores.mean()
print("cross Accuracy:", accuracy1)

# 使用交叉验证预测Y值
Y_pred = cross_val_predict(ovo_classif, X, Y.ravel(), cv=5)

# 计算混淆矩阵
conf_matrix = confusion_matrix(Y, Y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# 计算ARI、Precision、Recall、F1score
ari = adjusted_rand_score(Y, Y_pred)
precision_macro = precision_score(Y, Y_pred, average='macro')
recall_macro = recall_score(Y, Y_pred, average='macro')
f1_macro = f1_score(Y, Y_pred, average='macro')

print("Adjusted Rand Index (ARI):", ari)
print("Macro-Averaged Precision:", precision_macro)
print("Macro-Averaged Recall:", recall_macro)
print("Macro-Averaged F1 Score:", f1_macro)
end_time1 = time.time()
duration1 = end_time1 - end_time
print("模型训练和测试时间：", duration1, "秒")
print("stop")
