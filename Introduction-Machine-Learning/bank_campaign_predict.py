import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.covariance import MinCovDet
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("../datafiles/Bank.csv")
# 前処理
y = df["y"]
X = df.drop(columns=["y", "id"])

cat_cols = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
]


num_cols = [c for c in X.columns if c not in cat_cols]
num_pipe = Pipeline(
    steps=[("null", SimpleImputer(strategy="mean")), ("sc", StandardScaler())]
)
cat_pipe = Pipeline(steps=[("dummy", OneHotEncoder(drop="first"))])
preprocess = ColumnTransformer(
    [("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)]
)

# 各モデル実行
y_cnt = df["y"].value_counts()  # 正解データ不均衡 -> class_weight=balanced
print(y_cnt)


def learn(X, y):
    pipe = Pipeline(
        steps=[("preprocess", preprocess), ("model", DecisionTreeClassifier())]
    )
    param_grid = [
        {
            "model": [DecisionTreeClassifier(random_state=0, class_weight="balanced")],
            "model__max_depth": [3, 5, 8, 12],
        },
        {
            "model": [LogisticRegression(max_iter=1000, class_weight="balanced")],
            "model__C": [0.1, 1, 10],
        },
        {
            "model": [RandomForestClassifier(random_state=0, class_weight="balanced")],
            "model__n_estimators": [200, 400],
            "model__max_depth": [None, 8, 12],
        },
        {
            "model": [
                AdaBoostClassifier(
                    random_state=0,
                    estimator=DecisionTreeClassifier(
                        max_depth=1,
                        class_weight="balanced",
                        random_state=0,
                    ),
                )
            ],
            "model__n_estimators": [200, 400],
            "model__learning_rate": [0.01, 0.1, 1.0],
            "model__estimator__max_depth": [1, 2, 3, 4],
        },
    ]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=0, stratify=y
    )
    # 複数モデルを同じ前処理で横断比較
    kf = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)
    gs = GridSearchCV(
        pipe,
        param_grid=param_grid,
        cv=kf,
        n_jobs=-1,
        scoring="f1",
        refit=True,
    )
    gs.fit(X_tr, y_tr)
    y_pred = gs.predict(X_te)
    print("best params:", gs.best_params_)
    print("CV best score:", gs.best_score_)
    print("test f1 score:", gs.score(X_te, y_te))
    print(classification_report(y_pred=y_pred, y_true=y_te))


# 決定木でtrain 0.74, test 0.75
learn(X, y)

# 欠損値の埋め方を変える
print(df.isnull().sum())  # durationが

# 外れ値の確認
# 回帰モデルは外れ値の影響を受けやすいため（数値データのみでまずは確認）
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y
)
X_num = X_tr.drop(columns=cat_cols).dropna()
mcd = MinCovDet(random_state=0, support_fraction=0.7)
mcd.fit(X_num)
mah = mcd.mahalanobis(X_num)
mah_df = pd.DataFrame(mah, index=X_num.index, columns=["mahalanobis"])
fig = plt.figure()
mah_df.plot(kind="box", ax=fig.add_subplot())
plt.show()

desc = mah_df.describe()  # 基本統計量
print(desc)
q1 = desc.loc["25%", "mahalanobis"]
q3 = desc.loc["75%", "mahalanobis"]
iqr = q3 - q1  # 中央値を基準に外れ値を決定する、全データの50%が分布
upper = q3 + iqr * 1.5
lower = q1 - iqr * 1.5
outlier_no = mah_df.index[
    (mah_df["mahalanobis"] < lower) | (mah_df["mahalanobis"] > upper)
]  # 2020件もあるので、除外しない

outlier = mah_df.loc[(mah_df["mahalanobis"] > 12000), :].index
# 目検でマハラノビス距離が12000以上が1件ある

# duration を求める回帰モデル
# # 単回帰、リッジ回帰、ラッソ回帰の予測性能比較
num_cols_dur = [c for c in df.columns if c not in cat_cols + ["y", "id", "duration"]]
preprocess_dur = ColumnTransformer(
    [("num", num_pipe, num_cols_dur), ("cat", cat_pipe, cat_cols)]
)
pipe2 = Pipeline(steps=[("preprocess", preprocess_dur), ("model", LinearRegression())])
param_grid2 = [
    {
        "model": [LinearRegression()],
    },
    {
        "model": [Lasso(max_iter=10000, random_state=0)],
        "model__alpha": [10**e for e in range(-4, 5)],
    },
    {
        "model": [Ridge()],
        "model__alpha": [10**e for e in range(-4, 5)],
    },
]
yy = df["duration"].drop(outlier, axis=0)
XX = df.drop(columns=["y", "id", "duration"]).drop(outlier, axis=0)
notna_mask = yy.notna()
yy = yy.loc[notna_mask]
XX = XX.loc[notna_mask]
XX_tr, XX_te, yy_tr, yy_te = train_test_split(XX, yy, test_size=0.2, random_state=0)
kf2 = KFold(n_splits=5, random_state=0, shuffle=True)
gs2 = GridSearchCV(
    pipe2,
    param_grid=param_grid2,
    cv=kf2,
    n_jobs=-1,
    scoring="neg_mean_absolute_error",
    refit=True,
)
gs2.fit(XX_tr, yy_tr)
print("best params:", gs2.best_params_)
print("CV best score:", gs2.best_score_)
print("test acc (best):", gs2.score(XX_te, yy_te))

# durationの欠損値を埋めて、再実行
XXX = df.drop(columns=["y", "id"]).drop(outlier, axis=0)
na_mask = XXX["duration"].isnull()
XXX_cols = df.columns.difference(["y", "id", "duration"])
XXX_na = XXX.loc[na_mask, XXX_cols]
XXX.loc[na_mask, "duration"] = gs2.predict(XXX_na)
yyy = df.loc[XXX.index, "y"]
learn(XXX, yyy)

# 前回のモデルの方が 0.82で高い
# 訓練・検証では回帰の種類によって決定係数は変わらないから、訓練・検証データのばらつきは小さいか。
# # でもテストデータはばらつきが大きいのかも。
