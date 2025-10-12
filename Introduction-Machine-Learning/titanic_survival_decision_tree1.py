import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split

df = pd.read_csv("../datafiles/Survived.csv")
# 正解データ Survived (0,1) の不均衡
print(df["Survived"].value_counts())

# isnull, age->mean, embarked->mode
print(df.isnull().sum(axis=0))
print(df.shape)
df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
print(df.isnull().sum(axis=0))

# test data
xcol_draft = df.columns
xcol = [xcol_draft[2], xcol_draft[4], xcol_draft[5], xcol_draft[6], xcol_draft[8]]
print(xcol)
x = df[xcol]
t = df["Survived"]
x_train, x_test, y_train, y_test = train_test_split(x, t, test_size=0.2, random_state=0)
print(x_train.shape)

# model ※class_weight
model = tree.DecisionTreeClassifier(
    max_depth=5, random_state=0, class_weight="balanced"
)
model.fit(X=x_train, y=y_train)
# score
score = model.score(x_test, y_test)
print(score)
