import streamlit as st
from collections import Counter
from db import load_readings

# ====== 页面专属样式 ======
st.markdown("""
<style>
.tl-wrap { border-left: 1px solid #E8E6E0; padding-left: 1.5rem; margin-left: 0.5rem; }
.tl-dot-row { display: flex; align-items: flex-start; gap: 0; margin-left: -1.85rem; margin-bottom: 1.25rem; }
.tl-dot { width: 10px; height: 10px; border-radius: 50%; background: #AFA9EC; margin-top: 6px; margin-right: 1rem; flex-shrink: 0; }
.tl-card { flex: 1; background: #FAFAF8; border: 0.5px solid #E8E6E0; border-radius: 10px; padding: 1rem 1.25rem; }
.tl-date { font-size: 11px; color: #B4B2A9; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px; }
.tl-book { font-family: 'Lora', serif; font-size: 16px; font-weight: 500; color: #2C2C2A; margin-bottom: 6px; }
.tl-note { font-size: 13px; color: #5F5E5A; line-height: 1.6; margin-bottom: 8px; }
.tl-rating { font-size: 12px; color: #B4B2A9; margin-top: 6px; }
.empty-tip { text-align: center; color: #B4B2A9; font-size: 14px; padding: 3rem 0; font-style: italic; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='el-title'>阅读时间轴</div>", unsafe_allow_html=True)
st.markdown("<div class='el-subtitle'>你的阅读在时间里留下的轨迹</div>", unsafe_allow_html=True)

records = load_readings()

# ====== 基于真实数据的系统观察 ======
if records:
    all_tags = [tag for r in records for tag in r.get("tags", [])]
    tag_counter = Counter(all_tags)
    top_tags = [t for t, _ in tag_counter.most_common(3)]
    book_count = len(records)

    if len(records) >= 2:
        recent_tags = [tag for r in records[:3] for tag in r.get("tags", [])]
        early_tags = [tag for r in records[3:] for tag in r.get("tags", [])] if len(records) > 3 else []
        recent_counter = Counter(recent_tags)

        insight_parts = [f"你已记录了 {book_count} 本书"]
        if top_tags:
            insight_parts.append(f"「{'」和「'.join(top_tags[:2])}」是你最高频的情绪标签")
        st.markdown(f"""
        <div class='el-insight'>
            <strong style='color:#2C2C2A'>系统观察：</strong>
            {'，'.join(insight_parts)}。
        </div>
        """, unsafe_allow_html=True)

# ====== 时间轴 ======
if not records:
    st.markdown("<div class='empty-tip'>还没有阅读记录，去「记录阅读」写第一条吧</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='tl-wrap'>", unsafe_allow_html=True)

    for r in reversed(records):
        tags_html = "".join([f"<span class='el-tag'>{t}</span>" for t in r.get("tags", [])])
        date_str = r.get("date", "")[:10] if r.get("date", "") else ""
        rating = r.get("rating", "")

        st.markdown(f"""
        <div class='tl-dot-row'>
            <div class='tl-dot'></div>
            <div class='tl-card'>
                <div class='tl-date'>{date_str}</div>
                <div class='tl-book'>《{r['book']}》</div>
                <div class='tl-note'>{r['feeling']}</div>
                {tags_html}
                <div class='tl-rating'>{rating}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
