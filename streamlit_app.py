import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="🌱 Soil Moisture Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e, #16213e); }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .main-header {
        background: linear-gradient(135deg, rgba(0,212,170,0.15), rgba(0,180,216,0.1));
        border: 1px solid rgba(0,212,170,0.4);
        border-radius: 16px; padding: 28px 32px;
        margin-bottom: 24px; text-align: center;
    }
    .main-header h1 {
        font-size: 2.8rem; font-weight: 800; margin: 0;
        background: linear-gradient(135deg, #00d4aa, #00b4d8, #90e0ef);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .main-header p { color: #90e0ef; font-size: 1rem; margin: 8px 0 0 0; }
    .section-header {
        background: linear-gradient(90deg, rgba(0,212,170,0.2), transparent);
        border-left: 4px solid #00d4aa; border-radius: 0 8px 8px 0;
        padding: 10px 16px; margin: 20px 0 16px 0;
        color: #00d4aa !important; font-size: 1.2rem; font-weight: 700;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a2a3a, #1e3448);
        border: 1px solid rgba(0,212,170,0.3); border-radius: 12px;
        padding: 16px; text-align: center; margin-bottom: 8px;
    }
    .metric-label { color: #90e0ef; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .metric-green { color: #00d4aa; font-size: 1.9rem; font-weight: 800; }
    .metric-red   { color: #ff6b6b; font-size: 1.9rem; font-weight: 800; }
    .metric-status-ok  { color: #00d4aa; font-size: 0.75rem; }
    .metric-status-bad { color: #ff6b6b; font-size: 0.75rem; }
    .alert-green {
        background: rgba(0,212,170,0.12); border: 1px solid rgba(0,212,170,0.5);
        border-radius: 10px; padding: 14px; text-align: center; color: #00d4aa; font-weight: 700;
    }
    .alert-red {
        background: rgba(255,107,107,0.12); border: 1px solid rgba(255,107,107,0.5);
        border-radius: 10px; padding: 14px; text-align: center; color: #ff6b6b; font-weight: 700;
    }
    .stMarkdown p { color: #e0e0e0; }
    h1,h2,h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df["datetime"] = pd.to_datetime(
        df["tanggal"] + " " + df["waktu"],
        format="%d/%m/%Y %H:%M:%S"
    )
    return df

df            = load_data()
moisture_cols = ["moisture0","moisture1","moisture2","moisture3","moisture4"]
COLORS        = ["#00d4aa","#00b4d8","#90e0ef","#48cae4","#ade8f4"]

with st.sidebar:
    st.markdown("### ⚙️ Filter & Info")
    sumber_options = ["Semua"] + list(df["sumber"].unique())
    sumber_pilihan = st.selectbox("🌿 Pilih Sumber Data:", sumber_options)
    THRESHOLD      = st.slider("🎚️ Threshold Alert:", 0.0, 1.0, 0.30, 0.05)
    st.markdown("---")
    st.markdown("### 📊 Info Dataset")
    st.markdown(f"**Total:** {len(df):,} baris")
    for s in df["sumber"].unique():
        st.markdown(f"- {s}: **{len(df[df['sumber']==s]):,}**")
    st.markdown("---")
    st.markdown("### 📅 Rentang Tanggal")
    st.markdown(f"Mulai: **{df['tanggal'].min()}**")
    st.markdown(f"Akhir: **{df['tanggal'].max()}**")

df_filter = df[df["sumber"]==sumber_pilihan].copy() if sumber_pilihan != "Semua" else df.copy()

st.markdown(f"""
<div class="main-header">
    <h1>🌱 Soil Moisture Dashboard</h1>
    <p>Monitoring Kelembaban Tanah | Sumber: <b style="color:#00d4aa">{sumber_pilihan}</b>
    &nbsp;|&nbsp; Total: <b style="color:#00d4aa">{len(df_filter):,}</b> data
    &nbsp;|&nbsp; Threshold: <b style="color:#ff6b6b">{THRESHOLD}</b></p>
</div>
""", unsafe_allow_html=True)

# ── SECTION 1: STATISTIK ──────────────────────────────────
st.markdown('<div class="section-header">📊 Ringkasan Statistik</div>', unsafe_allow_html=True)
stat_cols = st.columns(5)
for i, col_name in enumerate(moisture_cols):
    avg = df_filter[col_name].mean()
    ok  = avg >= THRESHOLD
    stat_cols[i].markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{col_name}</div>
        <div class="{'metric-green' if ok else 'metric-red'}">{avg:.3f}</div>
        <div class="{'metric-status-ok' if ok else 'metric-status-bad'}">{'🟢 Normal' if ok else '🔴 Rendah'}</div>
        <div style="color:#aaa;font-size:0.72rem">min: {df_filter[col_name].min():.3f} | max: {df_filter[col_name].max():.3f}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SECTION 2: GAUGE METER ────────────────────────────────
st.markdown('<div class="section-header">🔵 Gauge Meter Kelembaban</div>', unsafe_allow_html=True)
fig_gauges = make_subplots(rows=1, cols=5, specs=[[{"type":"indicator"}]*5], subplot_titles=moisture_cols)
for i, col_name in enumerate(moisture_cols):
    avg   = df_filter[col_name].mean()
    color = "#00d4aa" if avg >= THRESHOLD else "#ff6b6b"
    fig_gauges.add_trace(go.Indicator(
        mode  = "gauge+number+delta",
        value = round(avg, 3),
        delta = {"reference": THRESHOLD, "valueformat":".3f",
                 "increasing":{"color":"#00d4aa"}, "decreasing":{"color":"#ff6b6b"}},
        gauge = {
            "axis"       : {"range":[0,1], "tickcolor":"#aaa", "tickfont":{"color":"#aaa"}},
            "bar"        : {"color": color, "thickness": 0.3},
            "bgcolor"    : "#1a2a3a",
            "borderwidth": 1,
            "bordercolor": "gray",
            "steps"      : [
                {"range":[0, THRESHOLD], "color":"rgba(255,107,107,0.15)"},
                {"range":[THRESHOLD, 1], "color":"rgba(0,212,170,0.15)"}
            ],
            "threshold"  : {"line":{"color":"#ff6b6b","width":3}, "thickness":0.8, "value":THRESHOLD}
        },
        number = {"font":{"color":color, "size":22}}
    ), row=1, col=i+1)
fig_gauges.update_layout(
    height=260, paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)", font_color="#ffffff",
    margin=dict(t=40, b=10, l=10, r=10)
)
st.plotly_chart(fig_gauges, use_container_width=True)

# ── SECTION 3: ALERT SYSTEM ───────────────────────────────
st.markdown('<div class="section-header">🚨 Alert System</div>', unsafe_allow_html=True)
alert_cols = st.columns(5)
for i, col_name in enumerate(moisture_cols):
    avg = df_filter[col_name].mean()
    ok  = avg >= THRESHOLD
    alert_cols[i].markdown(f"""
    <div class="{'alert-green' if ok else 'alert-red'}">
        {'🟢' if ok else '🔴'} <b>{col_name}</b><br>
        <span style="font-size:1.5rem;font-weight:800">{avg:.3f}</span><br>
        <span style="font-size:0.72rem">{'✅ NORMAL' if ok else '⚠️ BAHAYA'} | Threshold: {THRESHOLD}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── SECTION 4: TIME SERIES ────────────────────────────────
st.markdown('<div class="section-header">📈 Time Series Trend</div>', unsafe_allow_html=True)
c1, c2 = st.columns([4, 1])
with c2:
    m_sel    = st.multiselect("Sensor:", moisture_cols, default=moisture_cols)
    resample = st.selectbox("Agregasi:", ["Raw","Per Jam","Per Hari"])

df_ts = df_filter.sort_values("datetime").copy()
if resample == "Per Jam":
    df_ts = df_ts.set_index("datetime")[moisture_cols].resample("1H").mean().reset_index()
elif resample == "Per Hari":
    df_ts = df_ts.set_index("datetime")[moisture_cols].resample("1D").mean().reset_index()

with c1:
    if m_sel:
        fig_ts = go.Figure()
        for col_name in m_sel:
            cidx = moisture_cols.index(col_name)
            fig_ts.add_trace(go.Scatter(
                x=df_ts["datetime"], y=df_ts[col_name], name=col_name,
                line={"color": COLORS[cidx], "width": 1.5},
                hovertemplate=f"<b>{col_name}</b>: %{{y:.3f}}<extra></extra>"
            ))
        fig_ts.add_hline(y=THRESHOLD, line_dash="dash", line_color="#ff6b6b",
                         annotation_text=f"Threshold ({THRESHOLD})",
                         annotation_font_color="#ff6b6b")
        fig_ts.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,25,40,0.9)", font_color="#ffffff",
            legend={"bgcolor":"rgba(0,0,0,0.3)", "borderwidth":1, "font":{"color":"#fff"}},
            xaxis={"gridcolor":"rgba(255,255,255,0.07)", "title":"Waktu"},
            yaxis={"gridcolor":"rgba(255,255,255,0.07)", "title":"Nilai Moisture", "range":[0,1]},
            hovermode="x unified", margin=dict(t=20, b=40, l=50, r=20)
        )
        st.plotly_chart(fig_ts, use_container_width=True)

# ── SECTION 5: HEATMAP ────────────────────────────────────
st.markdown('<div class="section-header">🌡️ Correlation Heatmap per Sumber</div>', unsafe_allow_html=True)

sumber_unik  = df["sumber"].unique()
heatmap_cols = st.columns(len(sumber_unik))

# ✅ PERBAIKAN: gunakan tuple warna, bukan string rgba
cmap_custom = mcolors.LinearSegmentedColormap.from_list(
    "custom",
    [(1.0, 0.42, 0.42),   # merah #ff6b6b
     (0.10, 0.16, 0.23),  # gelap #1a2a3a
     (0.0,  0.83, 0.67)]  # hijau #00d4aa
)

for i in range(len(sumber_unik)):
    nama     = sumber_unik[i]
    data_src = df[df["sumber"] == nama][moisture_cols]
    corr     = data_src.corr()

    fig_hm, ax = plt.subplots(figsize=(4, 3.5))
    fig_hm.patch.set_facecolor("#0f1e2e")
    ax.set_facecolor("#0f1e2e")

    sns.heatmap(
        corr, annot=True, fmt=".2f",
        cmap=cmap_custom, vmin=-1, vmax=1,
        square=True,
        linewidths=0.5,
        linecolor="#1a2a3a",        # ✅ hex string biasa, bukan rgba
        ax=ax,
        annot_kws={"size":8, "color":"white", "weight":"bold"},
        cbar_kws={"shrink":0.8}
    )
    ax.set_title(nama, color="#00d4aa", fontsize=10, fontweight="bold", pad=10)
    ax.tick_params(colors="#aaaaaa", labelsize=7)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", color="#aaaaaa")
    plt.setp(ax.get_yticklabels(), rotation=0,  color="#aaaaaa")
    ax.collections[0].colorbar.ax.tick_params(colors="#aaaaaa", labelsize=7)
    plt.tight_layout()
    heatmap_cols[i].pyplot(fig_hm, clear_figure=True)
    plt.close()

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#90e0ef;font-size:0.85rem;padding:10px">
    🌱 <b>Soil Moisture Dashboard</b> | Data Lifecycle Management 2024 | Built with Streamlit & Plotly
</div>""", unsafe_allow_html=True)
