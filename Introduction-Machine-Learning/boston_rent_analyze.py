import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("../datafiles/Boston.csv")

cha_cols = ["CRIME"]
num_cols = [c for c in df.columns if c not in cha_cols]

# 文字データダミー化
cha_pipe = Pipeline(steps=[("ohe", OneHotEncoder(drop="first", dtype=int))])
# 数値データ標準化、欠損値埋め
num_pipe = Pipeline(
    steps=[("na", SimpleImputer(strategy="mean")), ("sc", StandardScaler())]
)
preprocess = ColumnTransformer(
    transformers=[("num", num_pipe, num_cols), ("str", cha_pipe, cha_cols)]
)
df2 = preprocess.fit_transform(df)
feat_names = preprocess.get_feature_names_out()
df2 = pd.DataFrame(df2, columns=feat_names)

# 主成分分析
model = PCA(n_components=2, whiten=True)
new_df = model.fit_transform(df2)  # 新しい軸に当てはめる
print(model.components_[0], model.components_[1], sep="\n")  # 固有ベクトル
new_df1 = pd.DataFrame(new_df, columns=["PC1", "PC2"])
print(new_df1.head(3))  # 0が最適なデータ

# 主成分負荷量（＝相関係数）
df3 = pd.concat([df2, new_df1], axis=1)
df_corr = df3.corr().loc[:"str__CRIME_very_low", "PC1":]
print(df_corr["PC1"].sort_values(ascending=False))
print(df_corr["PC2"].sort_values(ascending=False))

# 次元削減後の列の散布図
new_df1.columns = ["Cityside", "Exclusive_residential"]
new_df1.plot(kind="scatter", x="Cityside", y="Exclusive_residential")
plt.savefig("chap14.png")
plt.show()

# 寄与率の確認　まず元データの全列数分、新規列を作る
model_all = PCA(whiten=True)
allnew_df = model_all.fit_transform(df2)
allnew_df1 = pd.DataFrame(allnew_df)
print(allnew_df1)
ratio = model_all.explained_variance_ratio_
print(ratio)

# 累積寄与率 -> 0.8を超えたい　※元データの8割を反映する
ratios = []
thred, cnt = 0.8, -10
done = False
for i in range(len(ratio)):
    accum = sum(ratio[0 : i + 1])
    ratios.append(accum)
    if accum >= thred and done == False:
        done = True
        cnt = i + 1
        print(f"{'over 0.8:':20}", i + 1)
pd.DataFrame(ratios, columns=["accum_ratio"]).plot(kind="line")
plt.show()

# 5軸で0.8を超える　-> モデル再構成
model_fin = PCA(n_components=5, whiten=True)
df_fin = model_fin.fit_transform(df2)
df_fin1 = pd.DataFrame(df_fin, columns=["PC1", "PC2", "PC3", "PC4", "PC5"])
# 主成分負荷量（＝相関係数）
df4 = pd.concat([df2, df_fin1], axis=1)
df_corr_fin = df4.corr().loc[:"str__CRIME_very_low", "PC1":]
print(df_corr_fin["PC1"].sort_values(ascending=False))
print(df_corr_fin["PC2"].sort_values(ascending=False))
print(df_corr_fin["PC3"].sort_values(ascending=False))
print(df_corr_fin["PC4"].sort_values(ascending=False))
print(df_corr_fin["PC5"].sort_values(ascending=False))

# 結果をCSV形式で保存
df_corr_fin.to_csv(
    "boston_pca.csv", index=True, header=["PC1", "PC2", "PC3", "PC4", "PC5"]
)
