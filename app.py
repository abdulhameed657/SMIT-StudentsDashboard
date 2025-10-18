import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Streamlit Config ---
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

sns.set(style="whitegrid")

st.title("📊 Student Performance Analyzer (Enhanced)")
st.write("Upload or place `StudentsPerformance.csv` next to `app.py` and run:")
st.code("streamlit run app.py")

# --- File Loading ---
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df = df.rename(columns={
        "math score": "math_score",
        "reading score": "reading_score",
        "writing score": "writing_score"
    })
    df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1)
    return df

csv_name = "StudentsPerformance.csv"

try:
    df = load_data(csv_name)
except FileNotFoundError:
    st.error(f"❌ Could not find `{csv_name}`. Please upload it or place it next to `app.py`.")
    uploaded = st.file_uploader("Or upload your CSV file manually:")
    if uploaded is not None:
        df = load_data(uploaded)
    else:
        st.stop()

# --- Sidebar Controls ---
st.sidebar.header("Options")
show_head = st.sidebar.checkbox("Show first 5 rows")
show_boxplot = st.sidebar.checkbox("Show boxplot by gender", value=True)
show_pairplot = st.sidebar.checkbox("Show pairplot (scatter matrix)", value=False)

# --- Show Data ---
if show_head:
    st.subheader("📋 First 5 Rows")
    st.dataframe(df.head())

# --- Descriptive Stats ---
st.header("1️⃣ Descriptive Statistics")
col1, col2 = st.columns(2)

with col1:
    st.metric("Math Mean", f"{df['math_score'].mean():.2f}")
    st.metric("Reading Mean", f"{df['reading_score'].mean():.2f}")
    st.metric("Writing Mean", f"{df['writing_score'].mean():.2f}")

with col2:
    st.metric("Math Median", f"{df['math_score'].median():.2f}")
    st.metric("Math Mode", f"{df['math_score'].mode()[0]:.2f}")
    st.metric("Average of Averages", f"{df['average_score'].mean():.2f}")

# --- Standard Deviation ---
st.header("2️⃣ Standard Deviation")
st.dataframe(df[["math_score", "reading_score", "writing_score"]].std().to_frame("Std Dev"))

# --- Correlation Heatmap ---
st.header("3️⃣ Correlation Heatmap")
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(
    df[["math_score", "reading_score", "writing_score", "average_score"]].corr(),
    annot=True, cmap="coolwarm", ax=ax, fmt=".2f"
)
st.pyplot(fig)

# --- Histogram ---
st.header("4️⃣ Histogram of Math Scores")
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["math_score"], bins=10, color="skyblue", edgecolor="black")
ax.set_xlabel("Math Score")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- Average Score by Gender ---
st.header("5️⃣ Average Score by Gender")
if "gender" in df.columns:
    means = df.groupby("gender")["average_score"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x=means.index, y=means.values, ax=ax, palette="pastel")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Average Score")
    st.pyplot(fig)
else:
    st.info("ℹ️ Column 'gender' not found — skipping this section.")

# --- Optional Plots ---
if show_boxplot and "gender" in df.columns:
    st.header("6️⃣ Score Distribution by Gender (Boxplot)")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(x="gender", y="average_score", data=df, palette="Set2", ax=ax)
    st.pyplot(fig)

if show_pairplot:
    st.header("7️⃣ Pairplot (Score Relationships)")
    st.info("This may take a moment for larger datasets.")
    fig = sns.pairplot(df[["math_score", "reading_score", "writing_score", "average_score"]], diag_kind="hist")
    st.pyplot(fig)
