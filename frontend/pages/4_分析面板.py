import streamlit as st
from collections import Counter
from db import load_readings

# ====== 页面专属样式 ======
st.markdown("""
<style>
.metric-card { background: #FAFAF8; border: 0.5px solid #E8E6E0; border-radius: 10px; padding: 1rem 1.25rem; text-align: center; }
.metric-label { font-size: 11px; color: #B4B2A9; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 6px; }
.metric-value { font-family: 'Lora', serif; font-size: 28px; font-weight: 500; color: #2C2C2A; }
.persona-box { background: #FAFAF8; border: 0.5px solid #E8E6E0; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; }
.persona-label { font-size: 11px; color: #B4B2A9; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px; }
.persona-text { font-size: 14px; color: #2C2C2A; line-height: 1.75; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='el-title'>分析面板</div>", unsafe_allow_html=True)
st.markdown("<div class='el-subtitle'>你的阅读人格正在成形</div>", unsafe_allow_html=True)

records = load_readings()

# ====== 指标卡 ======
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>已记录</div>
        <div class='metric-value'>{len(records)}</div>
    </div>
    """, unsafe_allow_html=True)

all_tags = [tag for r in records for tag in r.get("tags", [])]
top_tag = Counter(all_tags).most_common(1)[0][0] if all_tags else "—"

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>最高频情绪</div>
        <div class='metric-value' style='font-size:20px'>{top_tag}</div>
    </div>
    """, unsafe_allow_html=True)

ratings = [r.get("rating", "") for r in records]
top_rating = Counter(ratings).most_common(1)[0][0] if ratings else "—"

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>最多评价</div>
        <div class='metric-value' style='font-size:20px'>{top_rating}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====== 阅读人格（基于真实数据） ======
if len(records) >= 3:
    top_two_tags = [t for t, _ in Counter(all_tags).most_common(2)]
    tag_text = f"「{'」和「'.join(top_two_tags)}」" if top_two_tags else "某种情绪"
    st.markdown(f"""
    <div class='persona-box'>
        <div class='persona-label'>你的阅读人格</div>
        <div class='persona-text'>
            基于 {len(records)} 本书的记录，你似乎更容易被
            {tag_text} 类型的作品打动。
            记录更多书之后，这里会由 AI 基于真实数据自动生成更深入的分析。
        </div>
    </div>
    """, unsafe_allow_html=True)
elif len(records) > 0:
    st.markdown("""
    <div class='persona-box'>
        <div class='persona-label'>你的阅读人格</div>
        <div class='persona-text'>
            记录更多书之后，这里会基于你的真实数据自动生成阅读人格分析。
            现在还差几本——再去「记录阅读」写几条吧。
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='persona-box'>
        <div class='persona-label'>你的阅读人格</div>
        <div class='persona-text'>
            还没有数据。去「记录阅读」添加你的第一本书，分析面板会随着记录越来越准确。
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====== 系统洞察 ======
if len(records) >= 2:
    recent_tags = [tag for r in records[:3] for tag in r.get("tags", [])]
    recent_counter = Counter(recent_tags)
    if len(recent_counter) >= 2:
        rc_tags = [t for t, _ in recent_counter.most_common(2)]
        st.markdown(f"""
        <div class='el-insight'>
            <strong style='color:#2C2C2A'>近期变化：</strong>
            最近几本书更偏向「{'」和「'.join(rc_tags)}」的情绪方向。
        </div>
        """, unsafe_allow_html=True)

# ====== 高频标签分布 ======
if all_tags:
    st.markdown("**高频情绪标签**")
    tag_counts = Counter(all_tags).most_common(8)
    tags_html = "".join([
        f"<span class='el-tag'>{tag} · {count}</span>"
        for tag, count in tag_counts
    ])
    st.markdown(tags_html, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='el-insight'>
        还没有足够的数据。去「记录阅读」添加几本书吧，分析面板会随着记录越来越准确。
    </div>
    """, unsafe_allow_html=True)
