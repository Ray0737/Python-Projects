from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
 
df = pd.read_csv("germany_auto_industry_dataset 1.csv")
print(df)

 
train_data = df.drop(columns=['Brand'])
target = df['Brand']
data_train, data_test, target_train, target_test = train_test_split(train_data, target, test_size=0.3,random_state=4)
clf = tree.DecisionTreeClassifier(max_depth=15)
clf.fit(data_train, target_train)
target_pred = clf.predict(data_test)

 
accuracy = accuracy_score(target_test, target_pred)
print(accuracy)

confusion_matrix = metrics.confusion_matrix(target_test, target_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix= confusion_matrix, display_labels=clf.classes_)

cm_display.plot()
plt.show()
 
tree.plot_tree(clf, feature_names=df.columns, class_names=clf.classes_)
plt.show()
 
 
Accuracy = metrics.accuracy_score(target_test,target_pred)
Precision = metrics.precision_score(target_test, target_pred,average='weighted')
Sensitivity_recall = metrics.recall_score(target_test, target_pred, average='weighted')
Specificity = metrics.recall_score(target_test, target_pred, pos_label=0,average='weighted')
F1_score = metrics.f1_score(target_test, target_pred,average='weighted')
 
print("Accuracy",Accuracy,"\nPrecision",Precision,"\nSensitivity_recall",Sensitivity_recall,"\nSpecificity",Specificity,"\nF1_score",F1_score)
