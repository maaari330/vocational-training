# 回帰：重回帰モデル

import math
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.tree import DecisionTreeRegressor

# read_csv
df = pd.read_csv("../datafiles/cinema.csv")
# sampling
print(df.sample(n=2, random_state=100))

# null
exist_null = df.isnull().any(axis="index")
# mean
df2 = df.fillna(df.mean(axis=0))
exist_null2 = df2.isnull().any(axis="index")
# plot scatter by matplotlib
xcols = [c for c in df2.columns if c != "cinema_id" and c != "sales"]
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
for ax, col in zip(ax.ravel(), xcols):
    df2.plot(kind="scatter", x=col, y="sales", ax=ax)
plt.show()
# delete outlier
no = df2[(df2["SNS2"] > 1000) & (df2["sales"] < 8500)]
noIndex = no.index
print(no, noIndex, df2.shape, sep="\n")
df2 = df2.drop(index=30, axis=0)
print(df2.shape)
print(list(df2.columns))
# 特徴量、正解データ
x = df2.loc[:, "SNS1":"original"]  # DataFrame[引数]；引数は1つ
t = df2["sales"]


def learn(model, test=None):
    x_train, x_test, y_train, y_test = train_test_split(
        x, t, test_size=0.2, random_state=0
    )
    model.fit(x_train, y_train)
    test_score = model.score(x_test, y_test)
    if test == "y":
        return test_score, model, x_test, y_test
    return test_score, model


# LinearRegression
test_score, linerModel, x_test, y_test = learn(LinearRegression(), test="y")
print("liner regression score:", test_score)
# predict
new_data = pd.DataFrame([[150, 700, 300, 0]], columns=x.columns)  # 1行4列
revenue = linerModel.predict(new_data)
# 正解との誤差　MAE（平均絶対誤差）、MSE（平均２乗誤差）、RMSE
pred = linerModel.predict(x_test)
mae = mean_absolute_error(y_pred=pred, y_true=y_test)  # 予測、実際の値の誤差の平均
mse = mean_squared_error(y_pred=pred, y_true=y_test)
rmse = math.sqrt(mse)
print(f"{'mean_absolute_error:':20}", mae)
print(f"{'mean_squared_error:':20}", mse)
print(f"{'root_mean_squared_error:':20}", rmse)

# 保存
with open("cinema.pkl", mode="wb") as f:
    pickle.dump(linerModel, f)


# もう一度開く
with open("cinema.pkl", mode="rb") as f:
    linerModel = pickle.load(f)
# LinearRegression 係数、切片
coef_df = pd.DataFrame(linerModel.coef_, index=x.columns)
print(coef_df, f"intercept: {linerModel.intercept_}", sep="\n")

# 新しいデータで行列計算
# 予測値が一致することを確認
new = pd.DataFrame([[150, 700, 300, 0]], columns=x.columns)
print(f"{'new * coef(@)':20}:", new.values @ linerModel.coef_ + linerModel.intercept_)
print(
    f"{'new * coef(dot)':20}:", new.values.dot(linerModel.coef_) + linerModel.intercept_
)
print(f"{'predict':20}:", linerModel.predict(new))

# ランダムフォレスト回帰木
test_score, randforeModel = learn(
    RandomForestRegressor(random_state=0, n_estimators=100)
)
print("random forest regressor score:", test_score)

# アダブースト回帰木
base_model = DecisionTreeRegressor(random_state=0, max_depth=3)
test_score, adabregModel = learn(
    AdaBoostRegressor(estimator=base_model, n_estimators=100, random_state=0)
)
print("adaboost regressor score:", test_score)

# K分割法
kf = KFold(n_splits=3, shuffle=True, random_state=0)
model_beforefit = LinearRegression()
score_dict = cross_validate(
    model_beforefit, x, t, scoring="r2", cv=kf, return_train_score=True
)
score_df = pd.DataFrame(score_dict)
print(score_df)
# K分割法採用後の決定係数
score_kf = sum(score_df["test_score"]) / len(score_df["test_score"])
print("k-fold cross-validation score:", score_kf)
