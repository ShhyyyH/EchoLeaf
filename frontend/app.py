import streamlit as st

st.set_page_config(
    page_title="EchoLeaf",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====== 全局样式 ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 侧边栏 */
[data-testid="stSidebar"] {
    background-color: #FAFAF8;
    border-right: 1px solid #E8E6E0;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-family: 'Lora', serif;
    font-size: 22px;
    font-weight: 500;
    color: #2C2C2A;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px;
    color: #5F5E5A;
}

/* 主区域 */
.main .block-container {
    background: #FFFFFF;
    padding-top: 2rem;
    max-width: 800px;
}

/* 共用组件 */
.el-title {
    font-family: 'Lora', serif;
    font-size: 26px;
    font-weight: 500;
    color: #2C2C2A;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}
.el-subtitle {
    font-size: 14px;
    color: #888780;
    margin-bottom: 2rem;
    font-style: italic;
}
.el-tag {
    display: inline-block;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 99px;
    background: #EEEDFE;
    color: #3C3489;
    margin: 3px 3px 3px 0;
    border: 0.5px solid #AFA9EC;
}
.el-insight {
    background: #FAFAF8;
    border-left: 2px solid #AFA9EC;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 13px;
    color: #5F5E5A;
    line-height: 1.65;
    margin-bottom: 1.25rem;
}
.el-card {
    background: #FAFAF8;
    border: 0.5px solid #E8E6E0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

/* 按钮 */
[data-testid="stButton"] button {
    background: #2C2C2A;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    padding: 0.5rem 1.5rem;
    font-family: 'DM Sans', sans-serif;
    width: 100%;
}
[data-testid="stButton"] button:hover {
    background: #444441;
}
</style>
""", unsafe_allow_html=True)

# ====== 侧边栏导航 ======
with st.sidebar:
    st.markdown("EchoLeaf")
    st.markdown(
        "<p style='font-family:DM Sans;font-size:12px;color:#B4B2A9;font-style:italic;margin-top:-0.5rem'>"
        "Every story leaves a trace.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

# ====== 欢迎页 ======
st.markdown("<div class='el-title'>欢迎回来</div>", unsafe_allow_html=True)
st.markdown("<div class='el-subtitle'>从侧边栏选择一个页面开始</div>", unsafe_allow_html=True)
