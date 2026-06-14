import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------------------
# Activation Functions
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
    one_hot_matrix = np.zeros((10, m), dtype=np.float32)
    for i in range(m):
        one_hot_matrix[int(Y[i]), i] = 1
    return one_hot_matrix

def get_predictions(A):
    return np.argmax(A, axis=0)

def get_accuracy(A, Y):
    predictions = get_predictions(A)
    return np.sum(predictions == Y) / Y.size


# ---------------------------
# Neural Network (3 Hidden Layers)
# ---------------------------
class SimpleNN:
    def __init__(self, h1, h2, h3):

        # He initialization (ดีที่สุดสำหรับ ReLU)
        self.W1 = np.random.randn(h1, 784).astype(np.float32) * np.sqrt(2/784)
        self.b1 = np.zeros((h1, 1), dtype=np.float32)

        self.W2 = np.random.randn(h2, h1).astype(np.float32) * np.sqrt(2/h1)
        self.b2 = np.zeros((h2, 1), dtype=np.float32)

        self.W3 = np.random.randn(h3, h2).astype(np.float32) * np.sqrt(2/h2)
        self.b3 = np.zeros((h3, 1), dtype=np.float32)

        self.W4 = np.random.randn(10, h3).astype(np.float32) * np.sqrt(2/h3)
        self.b4 = np.zeros((10, 1), dtype=np.float32)


    def forward_prop(self, X):
        Z1 = np.dot(self.W1, X) + self.b1
        A1 = relu(Z1)

        Z2 = np.dot(self.W2, A1) + self.b2
        A2 = relu(Z2)

        Z3 = np.dot(self.W3, A2) + self.b3
        A3 = relu(Z3)

        Z4 = np.dot(self.W4, A3) + self.b4
        A4 = softmax(Z4)

        return Z1, A1, Z2, A2, Z3, A3, Z4, A4


    def back_prop(self, Z1, A1, Z2, A2, Z3, A3, Z4, A4, X, Y, alpha):
        m = X.shape[1]
        one_hot_Y = one_hot(Y)

        # Output layer
        dZ4 = A4 - one_hot_Y
        dW4 = (1/m) * np.dot(dZ4, A3.T)
        db4 = (1/m) * np.sum(dZ4, axis=1, keepdims=True)

        # Hidden layer 3
        dZ3 = np.dot(self.W4.T, dZ4) * deriv_relu(Z3)
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

        # Gradient update
        self.W1 -= alpha * dW1
        self.b1 -= alpha * db1
        self.W2 -= alpha * dW2
        self.b2 -= alpha * db2
        self.W3 -= alpha * dW3
        self.b3 -= alpha * db3
        self.W4 -= alpha * dW4
        self.b4 -= alpha * db4


    def train(self, X, Y, alpha, iterations, target_acc=0.95):
        start = time.time()

        for i in range(iterations + 1):
            Z1, A1, Z2, A2, Z3, A3, Z4, A4 = self.forward_prop(X)
            self.back_prop(Z1, A1, Z2, A2, Z3, A3, Z4, A4, X, Y, alpha)

            if i % 100 == 0:
                acc = get_accuracy(A4, Y)
                print(f"Iterations {i} -> Acc: {acc:.3f}")
                if acc >= target_acc:
                    elapsed = time.time() - start
                    print(f"Reached {target_acc} at epoch {i} ({elapsed:.2f}s)")
                    return acc, i, elapsed

        elapsed = time.time() - start
        print(f"Final train acc = {acc:.3f}")
        return acc, iterations, elapsed


# ---------------------------
# Load Data
# ---------------------------
data = pd.read_csv("train.csv").to_numpy()
np.random.shuffle(data)

m, n = data.shape

data_dev = data[:1000].T
Y_dev = data_dev[0]
X_dev = (data_dev[1:n] / 255.0).astype(np.float32)

data_train = data[1000:].T
Y_train = data_train[0]
X_train = (data_train[1:n] / 255.0).astype(np.float32)

print("Training Set:", X_train.shape)
print("Dev Set:", X_dev.shape)

# ---------------------------
# Compare 3 models
# ---------------------------
hidden_sizes = [
    (10, 10, 10),
    (100, 100, 100),
    (1000, 1000, 1000)
]

results = []

for h1, h2, h3 in hidden_sizes:
    print("\n" + "="*60)
    print(f"Training Model With Hidden Sizes: {h1}, {h2}, {h3}")
    print("="*60)

    model = SimpleNN(h1, h2, h3)

    acc, epochs, elapsed = model.train(
        X_train, Y_train,
        alpha=0.04,          # LR เดียวที่เวิร์กกับทั้ง 3
        iterations=5000,
        target_acc=0.92
    )

    # Evaluate on dev set
    *_, A4_dev = model.forward_prop(X_dev)
    acc_dev = get_accuracy(A4_dev, Y_dev)

    print(f"Dev Accuracy = {acc_dev:.3f}")

    results.append({
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "train_acc": acc,
        "dev_acc": acc_dev,
        "epochs": epochs,
        "time_sec": elapsed
    })

# ---------------------------
# Summary
# ---------------------------
# ---------------------------
# Summary (Styled Like Your Hidden Layer 1 & 2 Table)
# ---------------------------
import pandas as pd
print("\n\n=== SUMMARY ===")

df = pd.DataFrame(results)

# Add time/epoch
df["time_per_epoch"] = df["time_sec"] / df["epochs"]

# Reorder columns
df = df[["h1", "h2", "h3", "train_acc", "dev_acc", "epochs", "time_sec", "time_per_epoch"]]

# Pretty print formatting
print(f"{'h1':>5} {'h2':>5} {'h3':>5} {'train_acc':>12} {'dev_acc':>10} "
      f"{'epochs':>10} {'time_sec':>12} {'time/epoch':>12}")

for i, row in df.iterrows():
    print(f"{int(row['h1']):5d} {int(row['h2']):5d} {int(row['h3']):5d} "
          f"{row['train_acc']:12.3f} {row['dev_acc']:10.3f} "
          f"{row['epochs']:10d} {row['time_sec']:12.2f} {row['time_per_epoch']:12.3f}")



