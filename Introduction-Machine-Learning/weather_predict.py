import matplotlib.pyplot as plt
import pandas as pd
from sklearn.covariance import MinCovDet

# 使用するファイル
df = pd.read_csv("../datafiles/bike.tsv", sep="\t")  # "\t"=tab
df2 = pd.read_csv(
    "../datafiles/weather.csv", encoding="shift_jis"
)  # 開くファイルの文字コードは、入力して解読できるかを確かめるのが早い
print(df2.head(2))
df3 = pd.read_json("../datafiles/temp.json").T

# 内部結合
null_cnt = df["weather_id"].isnull().sum()  # whether key has null or not
print(null_cnt)
df = df.merge(df2, how="inner", on="weather_id")  # 天気の文字データを結合
df = df.sort_values(axis=0, by="dteday")
gp1 = df.groupby(by="weather")["cnt"].mean(numeric_only=True)  # 天気ごとの利用者平均数
print(gp1)

# 外部結合
print(
    df3.shape, df.shape, sep="\n"
)  # ファイル内のデータ数が異なるため、キー値としてdtedayを使った内部結合はNG
df = df.merge(df3, how="left", on="dteday")
print(df.loc[(df["dteday"] == "2011-07-20"), :])  # 　dfにはあるけど、df3にはない値

# 時系列がある値の欠損確認
null_idx = df.loc[df["atemp"].isnull()].index
print(null_idx)
df.loc[150:250, "atemp"].plot(kind="line")
plt.show()

# 線形補完
print(df["atemp"].dtype)
df["atemp"] = df["atemp"].astype("float")
df["atemp"] = df["atemp"].interpolate()
df.loc[150:250, "atemp"].plot(kind="line")  # 欠損していた200,202が補完されている
plt.show()

# マハラビラス距離の計算
df4 = df.loc[:, "atemp":"windspeed"]
df4 = df4.dropna()
mcd = MinCovDet(random_state=0, support_fraction=0.7)
mcd.fit(df4)
distance = mcd.mahalanobis(df4)
print(distance)

# マハラノビス距離から外れ値を確認（箱ひげ）
distance2 = pd.DataFrame(distance, columns=["mahalanobis"], index=df4.index)
print(distance2)
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
distance2.plot(kind="box", ax=ax)
plt.savefig("box1.png")  # figureを画像として保存
plt.show()

# 外れ値の特定
df5 = pd.concat([df, distance2], axis=1)
desc = df5["mahalanobis"].describe()  # 基本統計量が表示される
print(desc)
iqr = desc.loc["75%"] - desc.loc["25%"]
upper = desc.loc["75%"] + iqr * 1.5
lower = desc.loc["25%"] - iqr * 1.5
num_cols = ["temp", "hum", "windspeed", "atemp"]
for c in num_cols:
    df5[c] = pd.to_numeric(df5[c], errors="coerce")
outlier = df5.loc[(df5["mahalanobis"] > upper) | (df5["mahalanobis"] < lower), :]
print(outlier)
Hazure = distance2[distance2["mahalanobis"] > 1750].index

# 3次元で表示
df6 = df5.drop(outlier.index, axis=0).dropna()
dfHazure = df5.loc[Hazure, :].dropna()
fig2 = plt.figure(figsize=(8, 8))
ax1 = fig2.add_subplot(111, projection="3d")
ax1.scatter(df6["temp"], df6["hum"], df6["windspeed"], s=5, c="blue", label="In Range")
ax1.scatter(
    outlier["temp"],
    outlier["hum"],
    outlier["windspeed"],
    s=5,
    c="green",
    label="Out of Range",
)
ax1.scatter(
    dfHazure["temp"],
    dfHazure["hum"],
    dfHazure["windspeed"],
    s=100,
    c="red",
    label="Hazure",
)
ax1.legend(loc="upper left")
ax1.set_xlabel("temp")
ax1.set_ylabel("hum")
ax1.set_zlabel("windspeed")
plt.show()
