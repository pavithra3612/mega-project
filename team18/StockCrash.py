import streamlit as st
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression

# Optional TensorFlow import
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.callbacks import EarlyStopping
except ModuleNotFoundError:
    tf = None
    layers = None
    models = None
    EarlyStopping = None

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Stock Crash Analysis", layout="wide")
st.title("📉 Stock Crash Analysis Dashboard")

# -----------------------------
# Config
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "CleanedUp.csv"

CRASH_THRESHOLD = -4.0
TEST_SIZE = 0.2
RANDOM_SEED = 42
EPOCHS = 50
BATCH_SIZE = 32

np.random.seed(RANDOM_SEED)
if tf is not None:
    tf.random.set_seed(RANDOM_SEED)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path.name} in team18 folder.")
    return pd.read_csv(path)

try:
    df = load_data(CSV_PATH)
except FileNotFoundError:
    st.warning("⚠️ Dataset not available for Team 18. Showing demo data instead.")

    # --- DEMO DATA ---
    dates = pd.date_range(start="2000-01-01", periods=300)
    df = pd.DataFrame({
        "Date": dates,
        "Index_Change_Percent": np.random.normal(0, 2, size=300),
        "Trading_Volume": np.random.randint(1000, 10000, size=300)

# -----------------------------
# Clean / prepare data
# -----------------------------
cols_to_keep = ["Date", "Index_Change_Percent", "Trading_Volume"]
missing_cols = [c for c in cols_to_keep if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

df = df[cols_to_keep].copy()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Index_Change_Percent", "Trading_Volume"])

# Crash label
df["Crash"] = (df["Index_Change_Percent"] <= CRASH_THRESHOLD).astype(int)

# -----------------------------
# Summary metrics
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rows", len(df))
with col2:
    st.metric("Crash Days", int(df["Crash"].sum()))
with col3:
    st.metric("Non-Crash Days", int((df["Crash"] == 0).sum()))

# -----------------------------
# Plot crashes over time
# -----------------------------
st.subheader("Crash vs Normal Days Over Time")

fig1, ax1 = plt.subplots(figsize=(10, 5))

normal = df[df["Crash"] == 0]
crash = df[df["Crash"] == 1]

ax1.scatter(
    normal["Date"],
    normal["Index_Change_Percent"],
    label="Normal",
    alpha=0.5
)
ax1.scatter(
    crash["Date"],
    crash["Index_Change_Percent"],
    label="Crash",
    alpha=0.9,
    marker="x"
)

ax1.axhline(CRASH_THRESHOLD, linestyle="--")
ax1.set_title("Index Change Percent Over Time (Crashes Highlighted)")
ax1.set_xlabel("Date")
ax1.set_ylabel("Index Change Percent")
ax1.legend()
ax1.grid(True)
fig1.tight_layout()

st.pyplot(fig1)

# -----------------------------
# Prepare ML data
# -----------------------------
X = df[["Index_Change_Percent", "Trading_Volume"]].values
y = df["Crash"].values

# Need at least 2 classes
if len(np.unique(y)) < 2:
    st.warning("The dataset does not contain both crash and non-crash classes.")
    st.stop()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_SEED,
    stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Train model
# -----------------------------
st.subheader("Model Training")

if tf is not None:
    st.success("TensorFlow detected — using Neural Network model.")

    model = models.Sequential([
        layers.Input(shape=(X_train_scaled.shape[1],)),
        layers.Dense(16, activation="relu"),
        layers.Dense(8, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    history = model.fit(
        X_train_scaled,
        y_train,
        validation_split=0.2,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stop],
        verbose=0
    )

    # Plot training loss
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(history.history["loss"], label="Train loss")
    ax2.plot(history.history["val_loss"], label="Val loss")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.set_title("Training vs Validation Loss")
    ax2.legend()
    ax2.grid(True)
    fig2.tight_layout()
    st.pyplot(fig2)

    # Plot training accuracy
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(history.history["accuracy"], label="Train accuracy")
    ax3.plot(history.history["val_accuracy"], label="Val accuracy")
    ax3.set_xlabel("Epoch")
    ax3.set_ylabel("Accuracy")
    ax3.set_title("Training vs Validation Accuracy")
    ax3.legend()
    ax3.grid(True)
    fig3.tight_layout()
    st.pyplot(fig3)

    # Predictions
    y_pred_prob = model.predict(X_test_scaled, verbose=0).ravel()
    y_pred = (y_pred_prob >= 0.5).astype(int)

else:
    st.warning("TensorFlow not available — using Logistic Regression fallback.")

    model = LogisticRegression(random_state=RANDOM_SEED, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

# -----------------------------
# Evaluation
# -----------------------------
st.subheader("Model Evaluation")

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, digits=3)

col4, col5 = st.columns(2)
with col4:
    st.metric("Test Accuracy", f"{acc:.3f}")
with col5:
    st.metric("Test Samples", len(y_test))

st.write("### Confusion Matrix")
cm_df = pd.DataFrame(
    cm,
    index=["Actual 0", "Actual 1"],
    columns=["Pred 0", "Pred 1"]
)
st.dataframe(cm_df)

st.write("### Classification Report")
st.text(report)

# -----------------------------
# Raw data preview
# -----------------------------
st.subheader("Preview of Processed Data")
st.dataframe(df.head(50), use_container_width=True)
