import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------------------
# ฟังก์ชัน Activation ต่าง ๆ
# ---------------------------
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def deriv_sigmoid(z):
    s = sigmoid(z)
    return s * (1 - s)

def tanh(z):
    return np.tanh(z)

def deriv_tanh(z):
    return 1 - np.tanh(z)**2

def relu(z):
    return np.maximum(0, z)

def deriv_relu(z):
    return z > 0

def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

def deriv_leaky_relu(z, alpha=0.01):
    dz = np.ones_like(z)
    dz[z < 0] = alpha
    return dz

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
# Neural Network Class
# ---------------------------
class SimpleNN:
    def __init__(self, activation='relu'):
        self.activation_name = activation.lower()

        # initialize weights
        self.W1 = np.random.randn(128, 784) * 0.01
        self.b1 = np.zeros((128, 1))
        self.W2 = np.random.randn(64, 128) * 0.01
        self.b2 = np.zeros((64, 1))
        self.W3 = np.random.randn(10, 64) * 0.01
        self.b3 = np.zeros((10, 1))

    # เลือก Activation Function
    def activation(self, z):
        if self.activation_name == 'sigmoid':
            return sigmoid(z)
        elif self.activation_name == 'tanh':
            return tanh(z)
        elif self.activation_name == 'leakyrelu':
            return leaky_relu(z)
        else:
            return relu(z)

    # อนุพันธ์ของ Activation
    def activation_deriv(self, z):
        if self.activation_name == 'sigmoid':
            return deriv_sigmoid(z)
        elif self.activation_name == 'tanh':
            return deriv_tanh(z)
        elif self.activation_name == 'leakyrelu':
            return deriv_leaky_relu(z)
        else:
            return deriv_relu(z)

    # Forward propagation
    def forward_prop(self, X):
        Z1 = np.dot(self.W1, X) + self.b1
        A1 = self.activation(Z1)
        Z2 = np.dot(self.W2, A1) + self.b2
        A2 = self.activation(Z2)
        Z3 = np.dot(self.W3, A2) + self.b3
        A3 = softmax(Z3)
        return Z1, A1, Z2, A2, Z3, A3

    # Back propagation
    def back_prop(self, Z1, A1, Z2, A2, Z3, A3, X, Y, alpha):
        m = X.shape[1]
        one_hot_Y = one_hot(Y)

        # Output layer
        dZ3 = A3 - one_hot_Y
        dW3 = (1/m) * np.dot(dZ3, A2.T)
        db3 = (1/m) * np.sum(dZ3, axis=1, keepdims=True)

        # Hidden layer 2
        dZ2 = np.dot(self.W3.T, dZ3) * self.activation_deriv(Z2)
        dW2 = (1/m) * np.dot(dZ2, A1.T)
        db2 = (1/m) * np.sum(dZ2, axis=1, keepdims=True)

        # Hidden layer 1
        dZ1 = np.dot(self.W2.T, dZ2) * self.activation_deriv(Z1)
        dW1 = (1/m) * np.dot(dZ1, X.T)
        db1 = (1/m) * np.sum(dZ1, axis=1, keepdims=True)

        # Update weights
        self.W1 -= alpha * dW1
        self.b1 -= alpha * db1
        self.W2 -= alpha * dW2
        self.b2 -= alpha * db2
        self.W3 -= alpha * dW3
        self.b3 -= alpha * db3

    # คำนวณ Loss (Cross-Entropy)
    def compute_loss(self, A3, Y):
        m = Y.size
        Y = Y.astype(int)
        loss = -np.mean(np.log(A3[Y, np.arange(m)] + 1e-9))
        return loss

    # Train model
    def train(self, X, Y, alpha=0.05, iterations=5000, target_acc=0.95):
        start = time.time()
        for i in range(iterations + 1):
            Z1, A1, Z2, A2, Z3, A3 = self.forward_prop(X)
            self.back_prop(Z1, A1, Z2, A2, Z3, A3, X, Y, alpha)

            if i % 100 == 0:
                acc = get_accuracy(A3, Y)
                loss = self.compute_loss(A3, Y)
                print(f"[{self.activation_name}] Iter {i} -> Acc: {acc:.3f}, Loss: {loss:.4f}")
                if acc >= target_acc:
                    print(f"🎯 Target {target_acc*100:.0f}% reached at epoch {i}")
                    break

        duration = time.time() - start
        return acc, i, duration


# ---------------------------
# Load & prepare data
# ---------------------------
data = pd.read_csv('train.csv').to_numpy()
np.random.shuffle(data)
m, n = data.shape

# dev set
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n] / 255.0

# training set
data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n] / 255.0

# ensure label type is integer
Y_train = Y_train.astype(int)
Y_dev = Y_dev.astype(int)

# normalize input only
X_train = (X_train - 0.5) / 0.5
X_dev = (X_dev - 0.5) / 0.5


# ---------------------------
# เทรนและเปรียบเทียบ Activation Function
# ---------------------------
results = []
activations = ['sigmoid', 'tanh', 'relu', 'leakyrelu']

for act in activations:
    print(f"\n=== Training with {act} ===")
    model = SimpleNN(activation=act)
    acc, epoch, duration = model.train(X_train, Y_train, alpha=0.05, iterations=5000, target_acc=0.95)

    # Evaluate on dev set
    _, _, _, _, _, A3_dev = model.forward_prop(X_dev)
    acc_dev = get_accuracy(A3_dev, Y_dev)

    results.append({
        "Activation": act,
        "Train Acc": acc,
        "Dev Acc": acc_dev,
        "Epochs": epoch,
        "Time (s)": round(duration, 2)
    })


# ---------------------------
# แสดงผลสรุป
# ---------------------------
print("\n=== Summary ===")
df = pd.DataFrame(results)
print(df)
