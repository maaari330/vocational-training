import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

df = pd.read_csv("../datafiles/KvsT.csv")

# 欠損値の有無を確認
df2 = df.copy()
is_null = df2.isnull().any(axis=0)
print(is_null)

# モデルの作成
xcol = [c for c in df2.columns if c != "派閥"]
x = df2.loc[:, xcol]
t = df2.loc[:, "派閥"]
# 深さを変更して正解率を確認
for i in range(1, 20):
    clf = DecisionTreeClassifier(max_depth=i, random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(
        x, t, test_size=0.3, random_state=0
    )
    clf.fit(x_train, y_train)

clf = DecisionTreeClassifier(max_depth=2, random_state=0)
x_train, x_test, y_train, y_test = train_test_split(x, t, test_size=0.3, random_state=0)
clf.fit(x_train, y_train)

# plot_tree関数で決定木を描画
x_train.columns = ["length", "weight", "age"]
plot_tree(clf, feature_names=x_train.columns, filled=True)
plt.show()

# clf.tree_のアトリビュート
n_nodes = clf.tree_.node_count
children_left = clf.tree_.children_left
children_right = clf.tree_.children_right
feature = clf.tree_.feature
threshold = clf.tree_.threshold
# tree_values = clf.tree_.value
# clf.tree.value は比率になっているのでサンプル数に変換する
tree_values = clf.tree_.value * clf.tree_.n_node_samples.reshape(-1, 1, 1)
print(f'{"node_count":20}: {n_nodes}')
print(f'{"children_left":20}: {children_left}')
print(f'{"children_right":20}: {children_right}')
print(f'{"feature":20}: {feature}')
print(f'{"threshold":20}: {threshold}')
print(f'{"tree_values":20}: {tree_values}')


# アトリビュートを活用したクラス予測
def node_search(node_id, x):
    while children_left[node_id] != children_right[node_id]:
        node_id = (
            children_left[node_id]
            if x[feature[node_id]] <= threshold[node_id]
            else children_right[node_id]
        )

    idx = np.argmax(tree_values[node_id])
    return idx


x = x_test.values[1]
result = node_search(0, x)
print(result, clf.classes_[result], sep="\t")

# テストデータxにおける、正解データの分類ごとの予測確率
class_possi = pd.DataFrame(clf.predict_proba(x_test.iloc[[1], :]), columns=clf.classes_)
print(class_possi)
