import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ Page Setup ------------------
st.set_page_config(
    page_title="📊 Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)
sns.set_theme(style="whitegrid")

st.title("🎓 Student Performance Analyzer (Pro)")
st.caption("Analyze academic performance patterns using the Kaggle dataset.")

# ------------------ Data Loading ------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df = df.rename(columns={
        "math score": "math_score",
        "reading score": "reading_score",
        "writing score": "writing_score"
    })
    df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1)
    return df

uploaded_file = st.sidebar.file_uploader("📂 Upload StudentsPerformance.csv", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
else:
    try:
        df = load_data("StudentsPerformance.csv")
    except FileNotFoundError:
        st.warning("⚠️ Please upload or place `StudentsPerformance.csv` next to this app.")
        st.stop()

# ------------------ Sidebar Filters ------------------
st.sidebar.header("🔍 Filter Data")

# Dynamic filtering
filter_cols = [c for c in ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"] if c in df.columns]

for col in filter_cols:
    unique_vals = ["All"] + sorted(df[col].dropna().unique().tolist())
    selection = st.sidebar.selectbox(f"Filter by {col}", unique_vals)
    if selection != "All":
        df = df[df[col] == selection]

st.sidebar.markdown("---")
show_raw = st.sidebar.checkbox("Show Raw Data", value=False)

# ------------------ Tabs Layout ------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "📊 Descriptive Stats",
    "🔥 Correlation & Insights",
    "📚 Gender Analysis",
    "📦 Raw Data"
])

# ------------------ Overview Tab ------------------
with tab1:
    st.subheader("📈 Overall Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Math Mean", f"{df['math_score'].mean():.2f}")
    col2.metric("Reading Mean", f"{df['reading_score'].mean():.2f}")
    col3.metric("Writing Mean", f"{df['writing_score'].mean():.2f}")
    col4.metric("Overall Avg", f"{df['average_score'].mean():.2f}")

    st.markdown("### 🎯 Distribution of Scores")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["average_score"], bins=20, kde=True, color="#4C72B0", ax=ax)
    ax.set_xlabel("Average Score")
    st.pyplot(fig)

# ------------------ Descriptive Stats ------------------
with tab2:
    st.subheader("📊 Descriptive Statistics")
    st.dataframe(df[["math_score", "reading_score", "writing_score", "average_score"]].describe())

    st.markdown("### 📘 Standard Deviation")
    st.dataframe(df[["math_score", "reading_score", "writing_score"]].std().to_frame("Std Dev"))

# ------------------ Correlation Tab ------------------
with tab3:
    st.subheader("🔥 Correlation Matrix")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(df[["math_score", "reading_score", "writing_score", "average_score"]].corr(), 
                annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.markdown("### 📉 Pairwise Relationships")
    st.caption("Use this to spot trends and relationships between score types.")
    fig = sns.pairplot(df[["math_score", "reading_score", "writing_score", "average_score"]], diag_kind="hist")
    st.pyplot(fig)

# ------------------ Gender Analysis Tab ------------------
with tab4:
    if "gender" in df.columns:
        st.subheader("📚 Average Scores by Gender")
        means = df.groupby("gender")[["math_score", "reading_score", "writing_score", "average_score"]].mean().round(2)
        st.dataframe(means)

        st.markdown("### 🧭 Visualization")
        fig, ax = plt.subplots(figsize=(7, 4))
        means.plot(kind="bar", ax=ax, color=["#6BAED6", "#FD8D3C", "#74C476", "#9E9AC8"])
        ax.set_ylabel("Average Score")
        ax.set_xlabel("Gender")
        st.pyplot(fig)

        st.markdown("### 🎨 Score Distribution by Gender")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.boxplot(data=df, x="gender", y="average_score", palette="Set2", ax=ax)
        st.pyplot(fig)
    else:
        st.info("ℹ️ Column 'gender' not found in dataset.")

# ------------------ Raw Data Tab ------------------
with tab5:
    if show_raw:
        st.subheader("📦 Raw Data Preview")
        st.dataframe(df)
    else:
        st.info("Enable **Show Raw Data** in the sidebar to view the full dataset.")
