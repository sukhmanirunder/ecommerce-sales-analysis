import streamlit as st

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    layout="wide"
)
st.markdown(
    """
    <h1 style="text-align:center; font-size:60px; font-weight:bold; margin-top: 10px;">
        🛒  E-commerce Sales Analysis
    </h1>
    """,
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    "<h3 style='text-align:center; color:#444;'>Turning Data into Business Insights</h3>",
    unsafe_allow_html=True
)

st.markdown("""
Welcome to the **E-commerce Sales Analysis Project**!  
This project explores customer purchasing behavior in an e-commerce dataset using Python.  
Through data visualization and analysis, it uncovers **sales patterns, product demand, seasonal trends, and customer segmentation** to generate valuable business insights.
""")

st.divider()

# ------------------------------
# WHY THIS PROJECT?
# ------------------------------
st.header("🌟 Why This Project?")
st.markdown("""
E-commerce businesses generate vast amounts of data daily.  
By analyzing this data, companies can:
- ✅ Understand **customer preferences**  
- ✅ Forecast **seasonal demand**  
- ✅ Improve **marketing strategies**  
- ✅ Optimize **inventory and supply chains**
""")

st.divider()

# ------------------------------
# TOOLS & TECHNOLOGIES
# ------------------------------
st.header("🧰 Tools & Technologies")
cols = st.columns(3)

with cols[0]:
    st.markdown("- **Python** 🐍")
    st.markdown("- **Pandas**")
    st.markdown("- **NumPy**")

with cols[1]:
    st.markdown("- **Matplotlib** 📊")
    st.markdown("- **Seaborn** 🎨")
    st.markdown("- **Jupyter Notebook**")

with cols[2]:
    st.markdown("- **Streamlit** 🌐")
    st.markdown("- **GitHub** 💻")

st.divider()
# ------------------------------
# DASHBOARD BUTTON SECTION
# ------------------------------
st.subheader("📊 Want to Explore the Dashboard?")
st.write("Click below to view the **interactive dashboard** of this project.")
if st.button("Go to Dashboard"):
    st.switch_page("pages/dashboard.py")

st.subheader("Want to Explore the Chatbot?")
st.write("Click below to view the **interactive Chatbot** of this project.")
if st.button("Go to Chatbot"):
    st.switch_page("pages/chatbot.py")


# ------------------------------
# FEATURES
# ------------------------------
st.header("🎯 Features")
st.markdown("""
- 🔹 Data cleaning & preprocessing  
- 🔹 Sales trend visualization  
- 🔹 Customer segmentation & behavior insights  
- 🔹 Product demand analysis  
- 🔹 Seasonal demand & forecasting  
""")

st.divider()

# ------------------------------
# SNEAK PEEK
# ------------------------------
st.header("📊 Sneak Peek of Insights")
st.info("""
📌 **Top-selling products** identified for targeted promotions  
📌 **Sales trends** show strong seasonal demand cycles  
📌 **Customer segmentation** reveals retention opportunities  
📌 **Visual dashboards** highlight actionable business insights  
""")

st.divider()

# ------------------------------
# GETTING STARTED
# ------------------------------
st.header("🚀 Getting Started")
st.code("""
git clone https://github.com/your-username/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

pip install -r requirements.txt

jupyter notebook
""", language="bash")

st.divider()


# ------------------------------
# FOOTER (AUTHOR INFO)
# ------------------------------
st.markdown(
       """
    <hr>
    <footer style="text-align:center; color:gray;">
        <div class="footer">
        👩‍💻 Developed by <b>Sukhmani</b> | 📧 sukhmanirunder40@gmail.com| 
        🔗 <a href="https://github.com/sukhmanirunder" target="_blank">GitHub</a>
    </div>
    </footer>
    """,
    unsafe_allow_html=True
)