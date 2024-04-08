import csv
from collections import Counter

from Code.Data import symbols
from Code.rank import results1

select_all_gene = {}
# 遍历每一行数据
for i, row in results1.iterrows():
    # 获取行名
    row_name = row.iloc[0]
    # 获取值为1的列名
    ones_col_names = results1.columns[1:-1][row.iloc[1:-1].astype(bool)]
    select_all_gene[i] = set(ones_col_names)
    # 初始化一个空的Counter对象
    gene_count = Counter()
    # 遍历字典中的每个样本和对应的基因集合
    for genes in select_all_gene.values():
        # 更新Counter对象，统计基因出现的次数
        gene_count.update(genes)

# 将基因名和对应的出现次数大于10的基因写入文件
with open('2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['gene', 'count'])  # 写入表头
    for gene, count in gene_count.items():
        if count > 10:
            writer.writerow([gene, count])

a = 80
# 求交集并输出结果--次数排名
intersect_genes = set(gene_count.keys()) & set(symbols)
intersect_genes_count = {gene: count for gene, count in gene_count.items()}
select_genes_count = dict(sorted(intersect_genes_count.items(), key=lambda x: x[1], reverse=True)[:a])
intersect_driver_genes = set(select_genes_count.keys()) & set(symbols)
print(f"所有样本中Count排名前{a}的基因:", select_genes_count)
print("Driver基因的个数：", len(intersect_driver_genes), intersect_driver_genes)
print(a)