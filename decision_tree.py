# -*- coding:utf-8 -*-
"""
使用python机器学习语言完成数据挖掘：
把准备好的数据分为训练数据和测试数据，使用训练数据完成决策树，对测试数据进行分类

1.对老师提供的spoc成绩，进行处理，得到数据集；
2.将数据集中的数据，再次进行筛选，得到实验数据集；
3.使用sklearn进行决策树的建立，并实现数据训练，生成二叉树
4.分析二叉树
"""


def change_flag(data):
    score, nums, longs = -1, -1, -1
    if data[0] == '良好':
        score = 2
    elif data[0] == '及格':
        score = 1
    elif data[0] == '不及格':
        score = 0

    if data[1] == '多':
        nums = 1
    elif data[1] == '少':
        nums = 0

    if data[2] == '长':
        longs = 1
    elif data[2] == '短':
        longs = 0

    result = [score, nums, longs, data[-1]]
    return result


dataSet = []
with open('excel/datas', 'r') as file:
    for line in file:
        datas = line.strip().split('\t')
        dataSet.append(change_flag(datas))
labels = ['score', 'nums', 'longs']

from sklearn import tree
from sklearn.cross_validation import train_test_split

FeatureSet = []
Label = []
for i in dataSet:
    FeatureSet.append(i[:-1])
    Label.append(i[-1])
X_train, X_test, y_train, y_test = train_test_split(FeatureSet, Label, random_state=1)  # 将数据随机分成训练集和测试集
print X_train
print X_test
print y_train
print y_test


clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)                     # 训练二叉树

with open("result.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
import os
os.unlink('result.dot')
#
from sklearn.externals.six import StringIO
import pydot
dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph[0].write_pdf("result.pdf")

pre_labels = clf.predict(X_test)
print pre_labels




"""
输出内容为：
1.训练数据属性
[[0, 1, 1], [0, 1, 1], [1, 1, 1], [2, 0, 1], [0, 1, 0], [1, 1, 1], [1, 1, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 1, 1], [0, 0, 0], [1, 0, 0], [2, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 0], [2, 1, 1], [0, 0, 0], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [0, 0, 0], [1, 1, 1], [0, 1, 1], [0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [1, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 0], [0, 0, 0], [1, 1, 1], [1, 0, 1], [0, 0, 0], [1, 1, 1], [1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 1], [1, 1, 0], [1, 1, 0], [0, 0, 0], [2, 1, 1], [0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [0, 1, 0], [0, 1, 1], [2, 1, 1], [0, 1, 1], [1, 1, 1], [2, 1, 1], [2, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 0], [2, 1, 1], [2, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [1, 1, 1]]
2.测试数据属性
[[0, 1, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0], [2, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 0], [0, 0, 0], [1, 1, 0], [1, 0, 0], [1, 1, 1], [1, 1, 0], [0, 1, 0], [0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0], [0, 0, 0]]
3.训练数据分类
['C', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'A', 'C', 'C', 'B', 'A', 'A', 'C', 'C', 'A', 'C', 'C', 'B', 'C', 'C', 'A', 'C', 'C', 'B', 'B', 'C', 'C', 'C', 'B', 'B', 'B', 'C', 'A', 'C', 'C', 'A', 'A', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'A', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'C', 'C', 'B', 'B', 'C', 'A', 'C', 'A', 'C', 'C', 'B', 'C', 'C', 'A', 'C', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'C', 'A', 'C', 'C', 'B', 'B', 'C', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'A']
4.训练数据分类
['C', 'C', 'C', 'A', 'B', 'A', 'B', 'A', 'C', 'C', 'B', 'A', 'C', 'C', 'B', 'A', 'B', 'C', 'B', 'B', 'A', 'B', 'C', 'C', 'C', 'C', 'C', 'B', 'A', 'B', 'C', 'C', 'B', 'B', 'B', 'C']
5.用决策树对训练数据属性进行分类判别
['C' 'C' 'C' 'A' 'B' 'A' 'B' 'A' 'C' 'C' 'B' 'A' 'C' 'C' 'B' 'A' 'B' 'C' 'B' 'B' 'A' 'B' 'C' 'C' 'C' 'C' 'C' 'B' 'A' 'B' 'C' 'C' 'B' 'B' 'B' 'C']
"""