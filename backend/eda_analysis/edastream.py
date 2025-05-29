import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Custom CSS for Styling ---
def add_custom_css():
    st.markdown("""<style>body { font-family: Arial; }</style>""", unsafe_allow_html=True)

# --- Function to Convert DataFrame to Arrow-Compatible ---
def make_arrow_compatible(df):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype('str')
        elif pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype('str')
    return df

# --- Streamlit App ---
def main():
    add_custom_css()
    st.markdown('## 📊 EDA Assistant', unsafe_allow_html=True)

    file_path = "data/data.csv"

    if file_path:
        try:
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            df = make_arrow_compatible(df)
            st.write("### 🔍 Dataset Preview:")
            st.dataframe(df.head())
            st.write("#### 📌 Columns Detected:", df.columns.tolist())

            # --- Custom Graphing Section ---
            st.markdown("## 📊 Custom Visualizations")
            x_column = st.selectbox("🧭 Select X-axis column", df.columns)
            y_column = st.selectbox("📏 Select Y-axis column", df.columns)

            df[y_column] = pd.to_numeric(df[y_column], errors='coerce')

            chart_type = st.selectbox("📊 Select Chart Type", [
                "Bar Chart", "Line Graph", "Scatter Plot", "Histogram", "Box Plot", "Heatmap"
            ])

            color = st.color_picker("🎨 Pick a Color", "#4CAF50")

            st.write(f"### 🔧 {chart_type} for {x_column} vs {y_column}")

            if chart_type == "Bar Chart":
                st.bar_chart(df.set_index(x_column)[y_column])
            elif chart_type == "Line Graph":
                st.line_chart(df.set_index(x_column)[y_column])
            elif chart_type == "Scatter Plot":
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[x_column], y=df[y_column], ax=ax, color=color)
                st.pyplot(fig)
            elif chart_type == "Histogram":
                fig, ax = plt.subplots()
                df[y_column].plot.hist(ax=ax, color=color)
                st.pyplot(fig)
            elif chart_type == "Box Plot":
                fig, ax = plt.subplots()
                sns.boxplot(x=df[x_column], y=df[y_column], ax=ax, color=color)
                st.pyplot(fig)
            elif chart_type == "Heatmap":
                fig, ax = plt.subplots()
                sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

        except Exception as e:
            st.error(f"🚫 Error loading or processing file: {e}")

if __name__ == "__main__":
    main()
