from sklearn.ensemble import RandomForestClassifier
import sklearn
print(sklearn.__version__)

clf = RandomForestClassifier(random_state=0)
X = [[1,2,3],[11,12,13]]
y=[0,1]
print(clf.fit(X,y))