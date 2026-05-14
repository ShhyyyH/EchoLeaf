import streamlit as st
from db import load_readings

# ====== 页面专属样式 ======
st.markdown("""
<style>
.chat-ai { background: #FAFAF8; border: 0.5px solid #E8E6E0; border-radius: 4px 16px 16px 16px; padding: 12px 16px; font-size: 14px; color: #2C2C2A; line-height: 1.65; margin-bottom: 12px; max-width: 85%; }
.chat-user { background: #EEEDFE; border-radius: 16px 4px 16px 16px; padding: 12px 16px; font-size: 14px; color: #3C3489; line-height: 1.65; margin-left: auto; margin-bottom: 12px; max-width: 85%; }
.chat-wrap { display: flex; flex-direction: column; }
.memory-tip { background: #FAFAF8; border: 0.5px solid #E8E6E0; border-radius: 8px; padding: 0.6rem 1rem; font-size: 12px; color: #B4B2A9; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='el-title'>聊天</div>", unsafe_allow_html=True)
st.markdown("<div class='el-subtitle'>它记得你读过的每一本书</div>", unsafe_allow_html=True)

# ====== 初始化对话历史 ======
records = load_readings()

if "chat_history" not in st.session_state:
    if records:
        books = "、".join([f"《{r['book']}》" for r in records[:3]])
        greeting = f"你好，我记得你读过 {books}。你现在在看什么，或者想聊哪本书？"
    else:
        greeting = "你好，欢迎来到 EchoLeaf。去「记录阅读」添加你的第一本书，我们就可以开始聊了。"
    st.session_state.chat_history = [{"role": "ai", "content": greeting}]

# ====== 显示已读书籍 ======
if records:
    books = "、".join([f"《{r['book']}》" for r in records[:3]])
    st.markdown(f"<div class='memory-tip'>📖 我记得你读过：{books}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='memory-tip'>📖 先去「记录阅读」添加几本书，我就能联系你的阅读历史来聊了</div>", unsafe_allow_html=True)

# ====== 渲染对话历史 ======
st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "ai":
        st.markdown(f"<div class='chat-ai'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ====== 输入框 ======
user_input = st.chat_input("聊聊你最近在读的...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # TODO: 后续接入 AI，替换占位回复
    reply = "（聊天功能将在接入 LLM 后生效。目前已经能从数据库读到你的阅读记录，等后端 API 就绪后，这里就能基于你的阅读历史进行对话了。）"
    st.session_state.chat_history.append({"role": "ai", "content": reply})

    st.rerun()
