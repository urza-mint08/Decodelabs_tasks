import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, f1_score, classification_report, accuracy_score

#load Dataset
iris = load_iris()
X, y = iris.data, iris.target

df = pd.DataFrame(X, columns=iris.feature_names)
df["species"] = pd.Categorical.from_codes(y, iris.target_names)

print("=" * 55)
print("DATASET OVERVIEW")
print("=" * 55)
print(f"Shape       : {X.shape}  ({X.shape[0]} samples, {X.shape[1]} features)")
print(f"Classes     : {list(iris.target_names)}")
print(f"\nClass distribution:\n{df['species'].value_counts().to_string()}")
print(f"\nFirst 5 rows:\n{df.head().to_string(index=False)}")

#Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print("\n" + "=" * 55)
print("TRAIN / TEST SPLIT  (80 / 20, stratified)")
print("=" * 55)
print(f"Training samples : {len(X_train)}")
print(f"Test samples     : {len(X_test)}")

#Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

#K selection
print("\n" + "=" * 55)
print("K-VALUE EVALUATION  (k = 1 … 20, macro F1)")
print("=" * 55)

results = {}
for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    preds = knn.predict(X_test_scaled)
    f1 = f1_score(y_test, preds, average="macro")
    results[k] = f1
    print(f"  k={k:2d}  →  macro F1 = {f1:.4f}")

best_k = max(results, key=results.get)
print(f"\nBest K : {best_k}  (macro F1 = {results[best_k]:.4f})")
print("Reason : highest macro-averaged F1 on the hold-out test set,")
print("         balancing precision and recall across all three classes.")

#Model Predictions
model = KNeighborsClassifier(n_neighbors=best_k)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

#Evaluation
print("\n" + "=" * 55)
print(f"EVALUATION  (KNN, k={best_k})")
print("=" * 55)

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
cm_df = pd.DataFrame(
    cm,
    index  =[f"True: {c}"  for c in iris.target_names],
    columns=[f"Pred: {c}" for c in iris.target_names],
)
print(cm_df.to_string())

macro_f1  = f1_score(y_test, y_pred, average="macro")
weighted_f1 = f1_score(y_test, y_pred, average="weighted")
acc       = accuracy_score(y_test, y_pred)

print(f"\nMacro F1 Score    : {macro_f1:.4f}")
print(f"Weighted F1 Score : {weighted_f1:.4f}")
print(f"Accuracy          : {acc:.4f}  ({int(acc * len(y_test))}/{len(y_test)} correct)")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
