import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../datafiles/cinema.csv").drop(["cinema_id"], axis=1)

# 前処理
preprocess = Pipeline(
    steps=[("na", SimpleImputer(strategy="mean")), ("sc", StandardScaler())]
)
df2 = preprocess.fit_transform(df)
col = preprocess.get_feature_names_out()
df3 = pd.DataFrame(df2, columns=col, index=df.index)

# 主成分モデル作成、変換
model = PCA(whiten=True)
tmp_new = model.fit_transform(df3)
ratios = model.explained_variance_ratio_  # 新しい列ごとの寄与率
df_new = pd.DataFrame(
    tmp_new, columns=["PC1", "PC2", "PC3", "PC4", "PC5"]
)  # 新しい列上での位置
print(df_new.head(3))
print(ratios)

# 累積寄与率の最適化
thred = 0.85
cnt = 0
for i in range(len(ratios)):
    tmp_ratio = sum(ratios[0 : i + 1])
    if tmp_ratio >= 0.85:
        cnt = i + 1
        break
model1 = PCA(n_components=cnt, whiten=True)

# モデルの再作成
model2 = PCA(whiten=True, n_components=cnt)
tmp_new2 = model2.fit_transform(df3)
df_new2 = pd.DataFrame(tmp_new2, columns=["PC1", "PC2", "PC3"])

# 主成分負荷量の確認
df_new2_corr = pd.concat([df3, df_new2], axis=1)
corr = df_new2_corr.corr()
print(corr.loc[:"sales", "PC1"].sort_values(ascending=False))  # 人気度を指している列か
print(corr.loc[:"sales", "PC2"].sort_values(ascending=False))  # 原作の影響度か
print(
    corr.loc[:"sales", "PC3"].sort_values(ascending=False)
)  # # SNS2＞SNS1よりSNSの影響度
