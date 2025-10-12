import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../datafiles/Boston.csv")
print(df.head(3), df.shape, sep="\n")

# 文字データのダミー変数化
crime_count = df.value_counts(subset="CRIME")
print(crime_count)
dum1 = pd.get_dummies(data=df["CRIME"], prefix="cri", drop_first=True, dtype=int)
df = pd.concat([df, dum1], axis=1)
df = df.drop(labels="CRIME", axis=1)

# （訓練・検証）用 / テスト用データに分割
train_val, test = train_test_split(df, test_size=0.2, random_state=0)

# 欠損値 -> 平均値で埋める
conf_null = train_val.isnull().sum()
train_val = train_val.fillna(train_val.mean(), axis=0)

print(train_val.columns)

# 外れ値の確認
fig, ax = plt.subplots(5, 3, figsize=(15, 25), dpi=120)
cols_temp = [col for col in train_val.columns if col != "PRICE"]
for i, col in enumerate(cols_temp):
    train_val.plot(kind="scatter", x=col, y="PRICE", ax=ax[i // 3, i % 3])
plt.show()

# 散布図から相関がありそうな列を抽出
cols = ["INDUS", "NOX", "RM", "PTRATIO", "LSTAT", "PRICE"]
ind1 = train_val[(train_val["PRICE"] >= 40) & (train_val["RM"] <= 6)].index
ind2 = train_val[(train_val["PTRATIO"] >= 20) & (train_val["PRICE"] >= 40)].index
inds = ind1.union(ind2)
train_val = train_val.drop(index=inds)
train_val = train_val[cols]

# 相関係数の強弱でさらに列を絞る
print(
    train_val.corr()["PRICE"].abs().sort_values(ascending=False)
)  # 絶対値により正負かかわらず大きい値順にソートされる
cols = ["RM", "LSTAT", "PTRATIO"]

# 訓練、検証用データへの分割
x = train_val[cols]
t = train_val[["PRICE"]]
x_train, x_val, y_train, y_val = train_test_split(x, t, test_size=0.2, random_state=0)

# 標準化    ※訓練用データ
model_x = StandardScaler()
model_x.fit(x_train)  # 各列ごとに平均値、標準偏差を格納
sc_x = model_x.transform(x_train)
print(sc_x)  # データ数＊特徴量ごとの標準値一覧 array型
tmp_df = pd.DataFrame(sc_x, columns=x_train.columns)
mean_df = tmp_df.mean()
std_df = tmp_df.std()
print(tmp_df, mean_df, std_df, sep="\n")

# 正解データの標準化
print(t, df["PRICE"], sep="\n")  # tはDataFrame型でないとエラー
model_y = StandardScaler()
model_y.fit(y_train)
sc_y = model_y.transform(y_train)

# 標準化した訓練データでのモデル作成
model = LinearRegression()
model.fit(sc_x, sc_y)

# モデル評価
sc_val_x = model_x.transform(x_val)  # 必ず訓練データの平均、標準偏差を使って標準化する
sc_val_y = model_y.transform(y_val)
res = model.score(sc_val_x, sc_val_y)
print(res)


# チューニング　※検証が0.85以上、テストが0.7以上（決定係数score）が目標
def learn(x, t):
    x_train, x_val, y_train, y_val = train_test_split(
        x, t, test_size=0.2, random_state=0
    )
    # 訓練データの標準化
    model_x = StandardScaler()
    model_y = StandardScaler()
    model_x.fit(x_train)
    sc_x = model_x.transform(x_train)
    model_y.fit(y_train)
    sc_y = model_y.transform(y_train)

    # モデル学習
    model = LinearRegression()
    model.fit(sc_x, sc_y)

    # 検証データの標準化
    sc_val_x = model_x.transform(x_val)
    sc_val_y = model_y.transform(y_val)

    # 訓練＆検証データの決定係数
    train_score = model.score(sc_x, sc_y)
    val_score = model.score(sc_val_x, sc_val_y)
    return train_score, val_score


x = train_val.loc[:, ["RM", "LSTAT", "PTRATIO"]]  # train_val=訓練＆検証データ
t = train_val[["PRICE"]]
s1, s2 = learn(x, t)
print(s1, s2)

# 特徴量エンジニアリング
x["RM2"] = x["RM"] ** 2
x["LSTAT2"] = x["LSTAT"] ** 2
x["PTRATIO2"] = x["PTRATIO"] ** 2
s1, s2 = learn(x, t)
print(s1, s2)

# 交互作用特徴量
x["RM*LSTAT"] = x["RM"] * x["LSTAT"]
s1, s2 = learn(x, t)
print(s1, s2)

# 再学習
model_x2 = StandardScaler()
model_t2 = StandardScaler()
model_x2.fit(x)
sc_x = model_x2.transform(x)
model_t2.fit(t)
sc_y = model_t2.transform(t)
model = LinearRegression()
model.fit(sc_x, sc_y)


# テストデータの前処理　（訓練・検証データと同じ処理）
test = test.fillna(
    train_val.mean(), axis=0
)  # 欠損値は平均値で　→　標準化をするから、訓練・検証出たと同じ平均、標準偏差を使う必要がある
x_test = test.loc[:, ["RM", "LSTAT", "PTRATIO"]]
y_test = test[["PRICE"]]
x_test["RM2"] = x_test["RM"] ** 2  # 特徴量エンジニアリング
x_test["LSTAT2"] = x_test["LSTAT"] ** 2
x_test["PTRATIO2"] = x_test["PTRATIO"] ** 2
x_test["RM*LSTAT"] = x_test["RM"] * x_test["LSTAT"]  # 交互作用特徴量
sc_x_test = model_x2.transform(
    x_test
)  # 訓練・検証データと同じモデル（平均、標準偏差）を使う必要がある
sc_y_test = model_t2.transform(y_test)
res = model.score(sc_x_test, sc_y_test)
print(res)

# モデルの保存
with open("boston.pkl", mode="wb") as f:
    pickle.dump(model, f)
with open("boston_scx.pkl", mode="wb") as f:
    pickle.dump(
        model_x2, f
    )  # 将来の予測では未知のデータを標準化してから、model.score()をやるため必要
with open("boston_scy.pkl", mode="wb") as f:
    pickle.dump(model_t2, f)

# 相関図の作成
pred_tmp = model.predict(sc_x_test)
pred = pd.DataFrame(model_t2.inverse_transform(pred_tmp), columns=["predicted"])
grand_truth = pd.DataFrame(
    model_t2.inverse_transform(sc_y_test), columns=["grand_truth"]
)
df_concat = pd.concat([pred, grand_truth], axis=1)
# df_concat.plot(x="predicted", y="grand_truth", kind="scatter")
fig, ax = plt.subplots()
plt.scatter(x=pred, y=grand_truth)
ax.set(xlabel="predicted", ylabel="grand_truth")
scorestr = r"R$^2$ = {:.3f}".format(model.score(sc_x_test, sc_y_test))
plt.text(15, 50, scorestr)
plt.plot([-10, 100], [-10, 100], color="orange", linestyle="dashed")
plt.show()
