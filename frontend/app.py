import sqlite3
import os
from datetime import datetime, timezone
import streamlit as st

# --- 数据库路径 ---
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "echoleaf.db")

os.makedirs(DB_DIR, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            reflection TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_reading(title: str, reflection: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO readings (title, reflection, created_at) VALUES (?, ?, ?)",
        (title.strip(), reflection.strip(), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def load_readings():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, title, reflection, created_at FROM readings ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


# --- 页面 ---
st.set_page_config(page_title="EchoLeaf", page_icon="📖")

init_db()

st.title("EchoLeaf")
st.caption("记录你与书之间的情感关系")

# --- 输入表单 ---
with st.form("reading_form"):
    title = st.text_input("书名", placeholder="输入你正在读或刚读完的书名")
    reflection = st.text_area(
        "阅读感受",
        placeholder="你现在想到这本书时，心里是什么感觉？有什么印象深刻的地方？",
        height=150,
    )
    submitted = st.form_submit_button("保存")

    if submitted:
        if not title.strip():
            st.warning("请填写书名")
        elif not reflection.strip():
            st.warning("请写下你的阅读感受")
        else:
            save_reading(title, reflection)
            st.success(f"《{title.strip()}》的记录已保存")
            st.rerun()

# --- 历史记录 ---
st.divider()
st.subheader("阅读记录")

readings = load_readings()

if not readings:
    st.info("还没有阅读记录，写一条吧。")
else:
    for row_id, row_title, row_reflection, row_time in readings:
        with st.container():
            display_time = row_time[:19].replace("T", " ")
            st.markdown(f"### 《{row_title}》")
            st.caption(display_time)
            st.write(row_reflection)
            st.divider()
