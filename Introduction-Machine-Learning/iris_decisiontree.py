# 分類：決定木モデル
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# 欠損値を埋める
df = pd.read_csv("../datafiles/iris.csv")
category = df["種類"].unique()
cnt = df["種類"].value_counts()  # 重複なしでdf["種類"]ごとの種類数をカウント
nan = df.isnull()  # 　欠損値を調べる
nanany = df.isnull().any(axis="index")  # 列単位で欠損値があるか調べる
nansum = df.isnull().sum(axis=0)
print(df.head(3), category, cnt, df.tail(3), nan, nanany, nansum, sep="\n")
# 欠損値以外の値で重回帰モデル作成　→　モデルの予測値で埋める
xcols = ["がく片長さ", "がく片幅", "花弁長さ", "花弁幅"]
for col_null in xcols:
    condition_cols = [c for c in xcols if c != col_null]
    df2 = df.dropna(how="any", inplace=False, axis="index")
    x = df2.loc[:, condition_cols]
    t = df2[col_null]
    model = LinearRegression()
    model.fit(x, t)
    fill_target = df.loc[(df[col_null].isnull()), condition_cols]
    pred = model.predict(fill_target)
    df.loc[(df[col_null].isnull()), col_null] = pred

nansum = df.isnull().sum(axis=0)
print(nansum)
# # 箱ひげ図で外れ値を確認
# df[[c for c in df.columns if c != "種類"]].plot(kind="box", rot=45)
# plt.show()
# # 外れ値があまりないから種類ごとの平均値で埋める
# for col in [c for c in df.columns if c != "種類"]:
#     df[col] = df[col].fillna(df.groupby("種類")[col].transform("mean"))
# print(df.isnull().sum())

# std
st = df.std(numeric_only=True)  # 標準偏差
print(st)
# 列ごとの平均値で埋める
# df3 = pd.read_csv("../datafiles/iris.csv")
# ave = df3.mean(numeric_only=True)  # 列ごとの平均値
# df3 = df3.fillna(
#     ave
# )  # fillna に 引数でSeries を渡すと、普通は列側（columns）に合わせる
# print(df3.isnull().any(axis="index"))


# モデル学習
x = df[xcols]
t = df["種類"]
model = DecisionTreeClassifier(max_depth=2, random_state=0)
x_train, x_test, y_train, y_test = train_test_split(
    x, t, test_size=0.3, random_state=0
)  # random_stateを設定することで常に同じデータが作成される
print(x_train, x_train.shape, sep="\n")

# モデル評価
model.fit(x_train, y_train)
res = model.score(x_test, y_test)  # テストデータと予測結果の比較
print(res)

# モデルの保存
with open("irismodel.pkl", mode="wb") as f:
    pickle.dump(model, f)


# モデルの読み込み
with open("irismodel.pkl", mode="rb") as f:
    model = pickle.load(f)

# feature, threshhold
column_num = model.tree_.feature  # 分岐に使われた特徴量
condition = model.tree_.threshold  # 分岐条件
print(column_num, condition, sep="\n")

# tree_.value, classes
length = model.tree_.node_count
for i in range(length):
    node = model.tree_.value[i]  # ノード i に到達した“学習データ”のクラス別の比率
    print(node)
leafs = model.classes_  # リーフごとの分類クラス（今回だとcolumsが該当）
print(leafs)

# node_samples
tree_values = model.tree_.value * model.tree_.n_node_samples.reshape(-1, 1, 1)
for i in range(length):
    node = tree_values[i]  # ノード i に到達した“学習データ”のクラス別の比率
    print(node)

# plot_tree
rcParams["font.family"] = "Meiryo"
rcParams["axes.unicode_minus"] = False
fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)  # figsize は Figure 全体の大きさ
feature_names = ["がく片長さ", "がく片幅", "花弁長さ", "花弁幅"]
tr = tree.plot_tree(
    model,
    feature_names=feature_names,
    class_names=model.classes_,
    rounded=True,
    filled=True,  # 純度の高さで濃淡
    ax=ax1,  # 1つの描画領域
)
fig.tight_layout()  # 余白を自動調整
plt.show()

# 不純度gini について
# # 真のクラスが k (確率 pk​) & 予測も k (確率 pk​) だとすると、
# # ​pk​×pkが正しい値。1-​ ​pk​×pk は誤った値。（＝不純度）
# 今回のケースだと1-((34/105)**2+(32/105)**2+(39/105)**2)　※105がx_trainのサンプル数、34,32,39​​が内訳
