# モデルの予測性能を高める

import pickle as pk

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree


# チューニング用関数
def learn(x, t, model):
    x_train, x_test, y_train, y_test = train_test_split(
        x, t, test_size=0.2, random_state=0
    )
    model.fit(X=x_train, y=y_train)
    # score
    score2 = model.score(x_train, y_train)  # 訓練データ
    score = model.score(x_test, y_test)  # テストデータ
    return round(score2, 3), round(score, 3)


# 使用データ
df = pd.read_csv("../datafiles/Survived.csv")
xcol_draft = df.columns
xcol = [xcol_draft[2], xcol_draft[4], xcol_draft[5], xcol_draft[6], xcol_draft[8]]
x = df[xcol]
t = df["Survived"]

# 木の深さ & 過学習の相関
for i in range(1, 15):
    train_score, test_score = learn(
        x,
        t,
        DecisionTreeClassifier(max_depth=i, random_state=0, class_weight="balanced"),
    )
    print(f"深さ{i}:訓練データの正解率{train_score},テストデータの正解率{test_score}")


# 欠損値の埋め込み　見直し
df2 = pd.read_csv("../datafiles/Survived.csv")
print(
    df2["Age"].mean(), df2["Age"].median(), sep="\n"
)  # 平均≒中央 平均->中央でも効果薄い

# 基準軸（小グループに分ける）での集計　※集計は数値データでないとできない
g1 = df2.groupby("Survived")
print(g1.mean(numeric_only=True))
g2 = df2.groupby("Pclass")
print(g2.mean(numeric_only=True))

# 2つ以上の基準軸：pivot table
pv1 = pd.pivot_table(
    df2, index="Survived", columns="Pclass", values="Age", aggfunc="mean"
)
print(pv1)
pv2 = pd.pivot_table(
    df2, index="Survived", columns="Pclass", values="Age", aggfunc="max"
)
print(pv2)

# isnull pivot tableの値で穴埋め
is_null = df2["Age"].isnull()


def fill(df, pclass, survive, age):
    df.loc[
        (df["Pclass"] == pclass) & (df["Survived"] == survive) & (is_null), "Age"
    ] = age


fill(df2, 1, 0, 43)
fill(df2, 1, 1, 35)
fill(df2, 2, 0, 33)
fill(df2, 2, 1, 25)
fill(df2, 3, 0, 26)
fill(df2, 3, 1, 20)
# 上記データでモデル精度
xcol_draft = df2.columns
xcol = [xcol_draft[2], xcol_draft[4], xcol_draft[5], xcol_draft[6], xcol_draft[8]]
x = df2[xcol]
t = df2["Survived"]
for i in range(1, 15):
    train_score, test_score = learn(
        x,
        t,
        DecisionTreeClassifier(max_depth=i, random_state=0, class_weight="balanced"),
    )
    print(f"深さ{i}:訓練データの正解率{train_score},テストデータの正解率{test_score}")

# 文字データ 性別
fig, ax = plt.subplots(1, 1)
sex = df2.groupby("Sex")["Survived"].mean()
ax = sex.plot(kind="bar")
plt.show()

print(xcol_draft, xcol)
xcol = list(xcol_draft[2:7]) + [xcol_draft[8]]
x = df2[xcol]
# learn(x,t)  # 文字データでのモデル学習はエラーになる

# ダミー変数化（male:1 female:0）
male = pd.get_dummies(data=df2["Sex"], dtype=int, drop_first=True)
print(male.head(3))
# ダミー変数化（embarked: C,Q,S）　※欠損が多いため、列ごと対象外とする
dummy2 = pd.get_dummies(data=df2["Embarked"], dtype=int, drop_first=True)
dummy3 = pd.get_dummies(data=df2["Embarked"], dtype=int)
print(dummy2.head(3), dummy3.head(3), sep="\n")

# ダミー変数（性別）を結合
x_new = pd.concat([x, male], axis=1).drop(axis=1, labels="Sex")

# 上記データでモデル精度
testMax = 0
for i in range(1, 7):
    tmp_model = DecisionTreeClassifier(
        max_depth=i, random_state=0, class_weight="balanced"
    )
    train_score, test_score = learn(x_new, t, tmp_model)
    if testMax < test_score:
        final_depth = i
        final_train_score = train_score
        final_test_score = test_score
        DecitreeModel = tmp_model

print(
    f"深さ{final_depth}",
    f"{'decision tree: train score:':20}{final_train_score}",
    f"{'decision tree: test score:':20}{final_test_score}",
    sep="\n",
)

# 決定木モデル　特徴量の重要度
deci_import = pd.DataFrame([DecitreeModel.feature_importances_], columns=x_new.columns)
print(deci_import)

with open("survived.pkl", mode="wb") as f:
    pk.dump(DecitreeModel, f)

# ランダムフォレスト
randforeModel = RandomForestClassifier(n_estimators=200, random_state=0)
train_score, test_score = learn(x_new, t, randforeModel)
print(
    f"{'random forest: train score:':20}{train_score}",
    f"{'random forest: test score:':20}{test_score}",
    sep="\n",
)

# ランダムフォレスト　特徴量の重要度
rand_import = pd.DataFrame([randforeModel.feature_importances_], columns=x_new.columns)
print(rand_import)

# アダブースト
base_model = DecisionTreeClassifier(max_depth=5, random_state=0)
adabooModel = AdaBoostClassifier(n_estimators=500, random_state=0, estimator=base_model)
train_score, test_score = learn(x_new, t, adabooModel)
print(
    f"{'adaboost: train score:':20}{train_score}",
    f"{'adaboost: test score:':20}{test_score}",
    sep="\n",
)

# 決定木の描画
fig, ax = plt.subplots(dpi=150)
plot_tree(
    DecitreeModel,
    max_depth=2,
    feature_names=x.columns,
    class_names=["passed", "survived"],
    filled=True,
    fontsize=12,
    ax=ax,
)
plt.tight_layout()
plt.show()

# 再現率、適合率
pred = DecitreeModel.predict(x_new)
scores = classification_report(t, pred, output_dict=True)
scores_df = pd.DataFrame(scores)
print(scores_df)
