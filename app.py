import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🎨 Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)
sns.set_theme(style="whitegrid", palette="pastel")

# ------------------ HEADER ------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        color: #5B2C6F;
        background: linear-gradient(90deg, #74ABE2, #F9A1BC, #C39BD3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 10px;
    }
    .subtext {
        text-align: center;
        font-size: 16px;
        color: #4A4A4A;
        margin-bottom: 40px;
    }
    </style>
    <h1 class="main-title">🎓 Student Performance Analyzer</h1>
    <p class="subtext">Explore student performance data interactively with beautiful visuals.</p>
    """,
    unsafe_allow_html=True
)

# ------------------ LOAD DATA ------------------
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

# ------------------ SIDEBAR ------------------
st.sidebar.header("🎛️ Filters")

filter_cols = [c for c in ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"] if c in df.columns]

for col in filter_cols:
    options = ["All"] + sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.selectbox(f"Filter by {col}", options)
    if selected != "All":
        df = df[df[col] == selected]

show_data = st.sidebar.checkbox("Show Raw Data", False)

# ------------------ COLOR PALETTE ------------------
palette = ["#7AC8FF", "#FF9CEE", "#8DF5A6", "#FFD56B", "#C9A0FF"]

# ------------------ TABS ------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Overview", "📊 Descriptive Stats", "🔥 Correlation", "👩‍🎓 Gender Insights", "📦 Raw Data"]
)

# ------------------ OVERVIEW TAB ------------------
with tab1:
    st.subheader("📈 Overall Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Math Avg", f"{df['math_score'].mean():.2f}")
    c2.metric("Reading Avg", f"{df['reading_score'].mean():.2f}")
    c3.metric("Writing Avg", f"{df['writing_score'].mean():.2f}")
    c4.metric("Overall Avg", f"{df['average_score'].mean():.2f}")

    st.markdown("---")

    st.markdown("### 🌈 Score Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["average_score"], bins=20, kde=True, color="#9B59B6", ax=ax)
    ax.set_xlabel("Average Score")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

# ------------------ STATS TAB ------------------
with tab2:
    st.subheader("📊 Descriptive Statistics")
    st.dataframe(df[["math_score", "reading_score", "writing_score", "average_score"]].describe().T.style.background_gradient(cmap="PuBuGn"))

    st.markdown("### 📘 Standard Deviation")
    st.dataframe(df[["math_score", "reading_score", "writing_score"]].std().to_frame("Std Dev").style.background_gradient(cmap="YlOrBr"))

# ------------------ CORRELATION TAB ------------------
with tab3:
    st.subheader("🔥 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(
        df[["math_score", "reading_score", "writing_score", "average_score"]].corr(),
        annot=True, cmap="coolwarm", fmt=".2f", linewidths=1, ax=ax
    )
    st.pyplot(fig)

    st.markdown("### 🎨 Pairplot (Score Relationships)")
    st.caption("Observe patterns and relationships across subjects.")
    fig = sns.pairplot(df[["math_score", "reading_score", "writing_score", "average_score"]], palette="husl")
    st.pyplot(fig)

# ------------------ GENDER INSIGHTS TAB ------------------
with tab4:
    if "gender" in df.columns:
        st.subheader("👩‍🎓 Average Scores by Gender")
        means = df.groupby("gender")[["math_score", "reading_score", "writing_score", "average_score"]].mean().round(2)
        st.dataframe(means.style.background_gradient(cmap="RdPu"))

        st.markdown("### 💫 Comparison Bar Chart")
        fig, ax = plt.subplots(figsize=(7, 4))
        means.plot(kind="bar", ax=ax, color=palette, edgecolor="black")
        ax.set_ylabel("Average Score")
        ax.set_xlabel("Gender")
        st.pyplot(fig)

        st.markdown("### 🩵 Score Distribution Boxplot")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.boxplot(data=df, x="gender", y="average_score", palette="cool", ax=ax)
        st.pyplot(fig)
    else:
        st.info("⚠️ Column 'gender' not found in dataset.")

# ------------------ RAW DATA TAB ------------------
with tab5:
    if show_data:
        st.subheader("📦 Raw Data Preview")
        st.dataframe(df.style.background_gradient(cmap="BuPu"))
    else:
        st.info("Enable **Show Raw Data** in the sidebar to view the dataset.")
