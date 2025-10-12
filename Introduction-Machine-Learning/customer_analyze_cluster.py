import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("../datafiles/Wholesale.csv")

# 欠損値なし
isnull = df.isnull().sum()
print(isnull)

# ダミー変数化、標準化
cha_cols = ["Channel", "Region"]
num_cols = [c for c in df.columns if c not in cha_cols]
cha_pipe = Pipeline(steps=[("dummy", OneHotEncoder())])
num_pipe = Pipeline(steps=[("sc", StandardScaler())])
preprocess = ColumnTransformer(
    transformers=[("cha", cha_pipe, cha_cols), ("num", num_pipe, num_cols)]
)
new = preprocess.fit_transform(df)
print(preprocess.get_feature_names_out())
new_df = pd.DataFrame(new, columns=preprocess.get_feature_names_out())

# kmeansモデル
model = KMeans(n_clusters=3, random_state=0)
model.fit_transform(new)
cluster_num = model.labels_
print(cluster_num)  # 各データのクラスタ番号
cluster_num_df = pd.DataFrame(cluster_num, columns=["cluster_num"])
new_df = pd.concat([new_df, cluster_num_df], axis=1)

# クラスタ分析
g1 = new_df.groupby("cluster_num").mean()  # クラスタごとにグループ化して集計
print(g1)
g1.plot(kind="bar")
plt.show()
# クラスタ0: あまり購入しない
# クラスタ1: 多く購入する
# クラスタ2: 平均的に購入

# エルボー法での最適なクラスタ数考察 -> 折れ線グラフから4が最適と予測
sses = []
for i in range(2, 31):
    tmp_model = KMeans(n_clusters=i, random_state=0)
    tmp_model.fit(new)
    sses.append(tmp_model.inertia_)
pd.DataFrame(sses).plot(kind="line")
plt.show()

# クラスタ数4で、各データごとのクラスタ番号を更新
model_fin = KMeans(n_clusters=4, random_state=0)
model_fin.fit(new)
new_df["cluster_num"] = model_fin.labels_
print(new_df.head(3))
new_df.to_csv("customer_analyze.csv", index=False)
