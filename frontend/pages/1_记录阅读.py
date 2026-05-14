import streamlit as st
from datetime import datetime
from db import save_reading, load_readings, delete_reading

# ====== 页面专属样式 ======
st.markdown("""
<style>
.success-box {
    background: #E1F5EE;
    border: 0.5px solid #5DCAA5;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-size: 14px;
    color: #085041;
}
.delete-btn button {
    background: transparent !important;
    color: #C4C2B8 !important;
    border: 1px solid #E8E6E0 !important;
    font-size: 12px !important;
    padding: 2px 10px !important;
    width: auto !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='el-title'>记录阅读</div>", unsafe_allow_html=True)
st.markdown("<div class='el-subtitle'>记下这本书在你身上留下的痕迹</div>", unsafe_allow_html=True)

# ====== 输入表单 ======
with st.form("record_form", clear_on_submit=True):
    book_name = st.text_input("书名", placeholder="例：春雪")

    feeling = st.text_area(
        "阅读感受",
        placeholder="它打动你的是什么？看完之后你现在的感觉是什么？不用完整，想到什么写什么。",
        height=120,
    )

    st.markdown("**情绪标签**（多选）")
    tag_options = ["后劲强", "压抑", "克制", "宿命感", "治愈", "虐心", "意犹未尽", "轻盈", "沉重", "释然"]
    selected_tags = st.multiselect(
        "选择符合的情绪",
        tag_options,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        rating = st.select_slider(
            "评分",
            options=["还行", "不错", "很好", "非常好", "封神"],
            value="很好",
        )
    with col2:
        read_date = st.date_input("读完时间", value=datetime.today())

    fragment = st.text_area(
        "印象深刻的片段（可选）",
        placeholder="某句话、某个场景，粘贴在这里",
        height=80,
    )

    submitted = st.form_submit_button("保存")

if submitted:
    if not book_name or not feeling:
        st.warning("书名和阅读感受不能为空")
    else:
        save_reading(book_name, feeling, selected_tags, rating, read_date, fragment)
        tags_html = "".join([f"<span class='el-tag'>{t}</span>" for t in selected_tags])
        st.markdown(f"""
        <div class='success-box'>
            已记录《{book_name}》· {rating}<br>
            {tags_html}
        </div>
        """, unsafe_allow_html=True)
        st.rerun()

# ====== 历史记录 ======
st.divider()
st.markdown("**所有记录**")

records = load_readings()

if not records:
    st.info("还没有阅读记录，写一条吧。")
else:
    for r in records:
        with st.container():
            col_main, col_del = st.columns([10, 1])
            with col_main:
                tags_html = "".join([f"<span class='el-tag'>{t}</span>" for t in r["tags"]])
                st.markdown(f"### 《{r['book']}》")
                st.caption(r["date"][:10] if r["date"] else "")
                st.write(r["feeling"])
                if r.get("fragment"):
                    st.caption(f"「{r['fragment'][:120]}」")
                st.markdown(tags_html, unsafe_allow_html=True)
            with col_del:
                if st.button("✕", key=f"del_{r['id']}", help="删除这条记录"):
                    delete_reading(r["id"])
                    st.rerun()
            st.divider()
