import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# ฟังก์ชันพื้นฐาน
# ---------------------------
def relu(z):
    return np.maximum(0, z)

def deriv_relu(z):
    return z > 0

def softmax(z):
    z = z - np.max(z, axis=0)
    return np.exp(z) / np.sum(np.exp(z), axis=0)

def one_hot(Y):
    m = len(Y)
    one_hot_matrix = np.zeros((10, m))
    for i in range(m):
        one_hot_matrix[int(Y[i]), i] = 1
    return one_hot_matrix

def get_predictions(A3):
    return np.argmax(A3, axis=0)

def get_accuracy(A3, Y):
    predictions = get_predictions(A3)
    return np.sum(predictions == Y) / Y.size


# ---------------------------
# สร้างคลาส Neural Network 3 ชั้น
# ---------------------------
class SimpleNN:
    def __init__(self):
        # layer1: 784 → 128
        # layer2: 128 → 64
        # layer3: 64 → 10
        self.W1 = np.random.randn(128, 784) * 0.01
        self.b1 = np.zeros((128, 1))
        self.W2 = np.random.randn(64, 128) * 0.01
        self.b2 = np.zeros((64, 1))
        self.W3 = np.random.randn(10, 64) * 0.01
        self.b3 = np.zeros((10, 1))

    def forward_prop(self, X):
        Z1 = np.dot(self.W1, X) + self.b1
        A1 = relu(Z1)
        Z2 = np.dot(self.W2, A1) + self.b2
        A2 = relu(Z2)
        Z3 = np.dot(self.W3, A2) + self.b3
        A3 = softmax(Z3)
        return Z1, A1, Z2, A2, Z3, A3

    def back_prop(self, Z1, A1, Z2, A2, Z3, A3, X, Y, alpha):
        m = X.shape[1]
        one_hot_Y = one_hot(Y)

        # Output layer
        dZ3 = A3 - one_hot_Y
        dW3 = (1/m) * np.dot(dZ3, A2.T)
        db3 = (1/m) * np.sum(dZ3, axis=1, keepdims=True)

        # Hidden layer 2
        dZ2 = np.dot(self.W3.T, dZ3) * deriv_relu(Z2)
        dW2 = (1/m) * np.dot(dZ2, A1.T)
        db2 = (1/m) * np.sum(dZ2, axis=1, keepdims=True)

        # Hidden layer 1
        dZ1 = np.dot(self.W2.T, dZ2) * deriv_relu(Z1)
        dW1 = (1/m) * np.dot(dZ1, X.T)
        db1 = (1/m) * np.sum(dZ1, axis=1, keepdims=True)

        # อัปเดตค่าน้ำหนัก
        self.W1 -= alpha * dW1
        self.b1 -= alpha * db1
        self.W2 -= alpha * dW2
        self.b2 -= alpha * db2
        self.W3 -= alpha * dW3
        self.b3 -= alpha * db3

    def train(self, X, Y, alpha, iterations):
        for i in range(iterations + 1):
            Z1, A1, Z2, A2, Z3, A3 = self.forward_prop(X)
            self.back_prop(Z1, A1, Z2, A2, Z3, A3, X, Y, alpha)
            if i % 100 == 0:
                acc = get_accuracy(A3, Y)
                print(f"Iteration {i} -> Accuracy: {acc:.3f}")

    def predict(self, X):
        _, _, _, _, _, A3 = self.forward_prop(X)
        return get_predictions(A3)


# ---------------------------
# เตรียมข้อมูล
# ---------------------------
data = pd.read_csv('train.csv')
data = np.array(data)
m, n = data.shape
np.random.shuffle(data)

# แบ่งชุดทดสอบ (dev set)
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n] / 255.0

# ชุดเทรน
data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n] / 255.0

print("Training data shape:", X_train.shape)
print("Training labels shape:", Y_train.shape)

# ---------------------------
# ฝึกโมเดล
# ---------------------------
model = SimpleNN()
model.train(X_train, Y_train, alpha=0.1, iterations=2800)

# ---------------------------
# ประเมินผลบน dev set
# ---------------------------
_, _, _, _, _, A3_dev = model.forward_prop(X_dev)
acc_dev = get_accuracy(A3_dev, Y_dev)
print(f"Final accuracy on dev set: {acc_dev:.3f}")

# ---------------------------
# ตัวอย่างการทำนาย 5 รูป
# ---------------------------
for i in range(5):
    img = X_dev[:, i].reshape(28, 28)
    plt.imshow(img, cmap='gray')
    plt.title(f"Predicted: {model.predict(X_dev[:, i].reshape(784,1))[0]}, True: {int(Y_dev[i])}")
    plt.show()
