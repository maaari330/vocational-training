import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../datafiles/iris.csv")

# 訓練・テストデータ分割
x = df.iloc[:, 0:4]
t = df.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(x, t, test_size=0.2, random_state=0)

# 欠損値の穴埋め、標準化、ロジスティック回帰
pipe = make_pipeline(
    SimpleImputer(strategy="mean"),
    StandardScaler(),
    LogisticRegression(random_state=0, C=0.1, multi_class="auto", solver="lbfgs"),
)
pipe.fit(x_train, y_train)
print(pipe.score(x_train, y_train))
print(pipe.score(x_test, y_test))

# "種類" ごとの予測式の係数
logireModel = pipe[-1]
coef_df = pd.DataFrame(
    logireModel.coef_, index=logireModel.classes_, columns=x_train.columns
)
print(coef_df)

# 新規データでの予測
new_x = [[1, 2, 3, 4]]
pred = logireModel.predict(new_x)  # 分類されたクラス
pred_proba = logireModel.predict_proba(new_x)  # 各クラスの確率
print(pred, pred_proba, sep="\t")
