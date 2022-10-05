from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm, tree
import pandas as pd
import seaborn as sb
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

df = pd.read_excel("Resultados 50 partidas KR.xlsx")

corr = df.corr()
sb.heatmap(corr, annot=True)

x_keep = ["Gold", "Minions", "Kills", "Assists", "Deaths", "Towers", "Dragons", "Heralds", "Gold_diff"]
X = df[x_keep]
y = df["Win"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
model = RandomForestClassifier().fit(X_train, y_train)
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
