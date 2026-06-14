from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
import itertools

mnist_raw = loadmat("mnist-original.mat")
mnist={
    'data':mnist_raw['data'].T,
    'target':mnist_raw['label'] [0]

}
x,y=mnist['data'],mnist['target']

x_train, x_test, y_train, y_test = x[:60000],x[60000:],y[:60000],y[60000:]

predict_number = 6666
y_train_0 = (y_train ==0)
y_test_0 = (y_test ==0)

y_train_6 = (y_train ==6)
y_test_6 = (y_test ==6)

def displayImage(x):
    plt.imshow(
    x.reshape(28,28),
    cmap=plt.cm.binary,
    interpolation='nearest')
    plt.show()

def displayPredict(clf,actually_y,x):
    print('Acttually = ',actually_y)
    print('Prediction = ',clf.predict([x])[0])

def displayConfusionMatrix(cm,cmap=plt.cm.GnBu):
    classes=['Other Number','Number 6']
    plt.imshow(cm,interpolation='nearest',cmap=cmap)
    plt.title('Confusion Matrix')
    plt.colorbar()
    trick_marks=np.arange(len(classes))
    plt.xticks(trick_marks,classes)
    plt.yticks(trick_marks,classes)
    thresh=cm.max()/2
    for i , j in itertools.product(range(cm.shape[0]),range(cm.shape[1])):
        plt.text(j,i,format(cm[i,j],'d'),
        horizontalalignment='center',
        color='white' if cm[i,j]>thresh else 'black')
    plt.tight_layout()
    plt.ylabel('Actially')
    plt.xlabel('Prediction')
    plt.show()

sgd_clf = SGDClassifier()
sgd_clf.fit(x_train,y_train_6)

displayImage(x_test[predict_number])
displayPredict(sgd_clf,y_test_6[predict_number], x_test[predict_number])

score = cross_val_score(sgd_clf,x_train,y_train_6,cv=3,scoring='accuracy')
print(score)

y_train_pred = cross_val_predict(sgd_clf,x_train,y_train_6,cv=3)
cm=confusion_matrix(y_train_6,y_train_pred)
# print(cm)

plt.figure()
displayConfusionMatrix(cm)
