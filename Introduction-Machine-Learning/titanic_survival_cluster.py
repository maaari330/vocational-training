import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.covariance import MinCovDet
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 前処理
df = pd.read_csv("../datafiles/Survived.csv")
df = df.drop(columns=["PassengerId", "Ticket", "Cabin", "Embarked"])
cha_cols = ["Sex"]
num_cols = [c for c in df.columns if c not in cha_cols]
cha_pipe = Pipeline(steps=[("dummy", OneHotEncoder())])
num_pipe = Pipeline(
    steps=[("na", SimpleImputer(strategy="mean")), ("sc", StandardScaler())]
)
preprocess = ColumnTransformer(
    [
        ("cha", cha_pipe, cha_cols),
        ("num", num_pipe, num_cols),
    ]
)
new = preprocess.fit_transform(df)
new_df = pd.DataFrame(new, index=df.index, columns=preprocess.get_feature_names_out())
# マハラノビス距離から外れ値を削除
mcd = MinCovDet(random_state=0).fit(new)
distance = pd.Series(mcd.mahalanobis(new))
distance.plot(kind="box")
plt.show()
outlier = distance[(distance > 1000)].index
print(new_df.shape)
new_df = new_df.drop(index=outlier)
print(new_df.shape)

# クラスタリング
model = KMeans(n_clusters=2, random_state=0)
model.fit(new_df)
new_df["cluster_num"] = pd.Series(model.labels_)

# クラスタリング分析
mean = new_df.groupby("cluster_num").mean()
mean.plot(kind="bar")
plt.show()

# 分析結果
# クラスタ1: 亡くなった人（高齢、男性多い）
# クラスタ2: 助かった人（若い、1等チケット）
