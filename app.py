from pathlib import Path
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# ROUTE//IQ — Last-mile delivery intelligence dashboard
# FA-2 | Mathematics for AI-II
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="ROUTE//IQ · Last-mile intelligence",
    page_icon="↗",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "last_mile_delivery.csv"
NAVY = "#111827"
INK = "#17212F"
MUTED = "#657184"
ORANGE = "#F28C28"
ORANGE_DARK = "#D96D0B"
TEAL = "#2C9C91"
BLUE = "#4777C7"
PURPLE = "#8171C7"
PALETTE = [ORANGE, BLUE, TEAL, PURPLE, "#C95A68", "#8B98A8", "#D7B34A"]

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
      :root { --route-ink:#17212F; --route-orange:#F28C28; --route-line:#E5E8ED; }
      html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
      .stApp { background: #F4F6F8; color: var(--route-ink); }
      [data-testid="stHeader"] { background: rgba(244,246,248,0.92); }
      [data-testid="stSidebar"] { background: #111827; border-right: 1px solid #273244; }
      [data-testid="stSidebar"] * { color: #F6F8FA !important; }
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#BAC3D0 !important; }
      [data-testid="stSidebar"] [data-baseweb="select"] > div { background:#202B3A; border-color:#374356; }
      [data-testid="stSidebar"] [data-baseweb="tag"] { background:#F28C28; }
      [data-testid="stSidebar"] hr { border-color:#303B4B; }
      .block-container { padding-top: 1.25rem; padding-bottom: 3.5rem; max-width: 1550px; }
      .route-kicker { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:#F28C28; }
      .route-hero { background:linear-gradient(118deg,#111827 0%,#1B283A 67%,#26374A 100%); border-radius:20px; padding:27px 31px 24px; color:#F8FAFC; position:relative; overflow:hidden; border:1px solid #263447; margin:0 0 21px; }
      .route-hero:after { content:''; position:absolute; width:310px; height:310px; right:-85px; top:-155px; border:1px solid rgba(242,140,40,.30); border-radius:50%; box-shadow:0 0 0 28px rgba(242,140,40,.035),0 0 0 58px rgba(242,140,40,.025); }
      .route-wordmark { font-family:'DM Mono',monospace; font-size:12px; letter-spacing:3px; color:#F28C28; margin-bottom:13px; }
      .route-title { font-size:clamp(28px,4vw,44px); line-height:1.05; font-weight:800; letter-spacing:-1.8px; color:#FFFFFF; margin:0; max-width:850px; }
      .route-subtitle { color:#C8D1DD; font-size:13px; line-height:1.6; margin-top:13px; max-width:720px; }
      .route-hero-bottom { display:flex; flex-wrap:wrap; gap:9px; margin-top:21px; position:relative; z-index:1; }
      .route-chip { border:1px solid #3A4658; border-radius:999px; padding:6px 10px; color:#DDE3EA; font-family:'DM Mono',monospace; font-size:10px; letter-spacing:.3px; }
      .route-chip-orange { background:#F28C28; border-color:#F28C28; color:#151B23; font-weight:700; }
      .section-eyebrow { font-family:'DM Mono',monospace; color:#D96D0B; font-size:10px; letter-spacing:1.8px; text-transform:uppercase; margin:6px 0 4px; }
      .section-title { font-size:22px; font-weight:800; letter-spacing:-.65px; color:#17212F; margin:0 0 4px; }
      .section-desc { color:#657184; font-size:12px; line-height:1.55; margin-bottom:14px; }
      .metric-card { background:#FFFFFF; border:1px solid #E4E8EE; border-radius:15px; padding:15px 17px 14px; min-height:118px; box-shadow:0 3px 12px rgba(23,33,47,.025); position:relative; overflow:hidden; }
      .metric-card:before { content:''; position:absolute; top:0; left:0; height:3px; width:38px; background:#F28C28; }
      .metric-label { color:#788393; font-family:'DM Mono',monospace; text-transform:uppercase; font-size:9px; letter-spacing:1.2px; }
      .metric-value { color:#17212F; font-size:28px; font-weight:800; letter-spacing:-1px; margin-top:9px; line-height:1; }
      .metric-note { color:#8791A0; font-size:10px; margin-top:8px; line-height:1.35; }
      div[data-testid="stPlotlyChart"] { background:#FFFFFF; border:1px solid #E4E8EE; border-radius:16px; padding:8px 8px 1px; box-shadow:0 3px 12px rgba(23,33,47,.025); margin:3px 0 11px; overflow:hidden; }
      .panel-kicker { color:#D96D0B; text-transform:uppercase; font-family:'DM Mono',monospace; letter-spacing:1.5px; font-size:9px; margin-bottom:7px; }
      .panel-title { color:#17212F; font-size:16px; line-height:1.25; font-weight:800; letter-spacing:-.3px; margin-bottom:5px; }
      .panel-copy { color:#657184; font-size:11px; line-height:1.55; margin-bottom:7px; }
      .insight-band { background:#FFF7ED; border-left:4px solid #F28C28; padding:13px 16px; border-radius:0 11px 11px 0; color:#573512; font-size:12px; line-height:1.6; margin:8px 0 18px; }
      .insight-band strong { color:#9A4E07; }
      .note-band { background:#EEF4FA; border-left:4px solid #4777C7; padding:12px 15px; border-radius:0 10px 10px 0; color:#304760; font-size:11px; line-height:1.55; margin:8px 0 14px; }
      .tag-row { display:flex; gap:7px; flex-wrap:wrap; margin:4px 0 12px; }
      .tiny-tag { display:inline-block; border-radius:6px; padding:5px 8px; background:#EDF0F4; color:#5B6677; font-family:'DM Mono',monospace; font-size:9px; }
      .tiny-tag.orange { background:#FFF0DE; color:#9C520C; }
      .footer-line { border-top:1px solid #E1E6EC; margin-top:25px; padding-top:13px; color:#8993A1; font-family:'DM Mono',monospace; font-size:9px; letter-spacing:.5px; }
      [data-testid="stMetric"] { background:white; padding:14px 16px; border:1px solid #E4E8EE; border-radius:14px; }
      div[data-testid="stTabs"] button { font-family:'DM Mono',monospace; font-size:11px; letter-spacing:.3px; }
      div[data-testid="stTabs"] button[aria-selected="true"] { color:#D96D0B; border-bottom-color:#F28C28; }
      .stButton > button { border-radius:8px; border:1px solid #46566D; background:#202B3A; color:#FFFFFF; font-weight:700; }
      .stButton > button:hover { border-color:#F28C28; color:#F28C28; }
      [data-testid="stDataFrame"] { border:1px solid #E4E8EE; border-radius:12px; overflow:hidden; }
      @media (max-width: 800px) { .route-hero {padding:22px;} .metric-value{font-size:24px;} }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading delivery records…")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "Order_ID", "Agent_Age", "Agent_Rating", "Store_Latitude", "Store_Longitude",
        "Drop_Latitude", "Drop_Longitude", "Order_Date", "Weather", "Traffic",
        "Vehicle", "Area", "Delivery_Time", "Category"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError("Required column(s) missing: " + ", ".join(sorted(missing)))
    df["Delivery_Time"] = pd.to_numeric(df["Delivery_Time"], errors="coerce")
    df["Agent_Age"] = pd.to_numeric(df["Agent_Age"], errors="coerce")
    df["Agent_Rating"] = pd.to_numeric(df["Agent_Rating"], errors="coerce")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    text_cols = ["Weather", "Traffic", "Vehicle", "Area", "Category"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip().replace("", pd.NA).fillna("Unknown")
    df = df.dropna(subset=["Delivery_Time"]).copy()
    # Late delivery threshold is defined from the whole prepared dataset and stays stable
    # as dashboard filters change: mean(Delivery_Time) + 1 standard deviation.
    threshold = df["Delivery_Time"].mean() + df["Delivery_Time"].std(ddof=1)
    df["Late_Flag"] = df["Delivery_Time"] > threshold
    df["Agent_Age_Group"] = pd.cut(
        df["Agent_Age"], bins=[-float("inf"), 24, 40, float("inf")],
        labels=["Under 25", "25–40", "Over 40"], right=True
    ).astype("string").fillna("Unknown")
    df["Order_Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()
    # Approximate straight-line distance in km (Haversine); context only, not road distance.
    lat1 = pd.to_numeric(df["Store_Latitude"], errors="coerce")
    lon1 = pd.to_numeric(df["Store_Longitude"], errors="coerce")
    lat2 = pd.to_numeric(df["Drop_Latitude"], errors="coerce")
    lon2 = pd.to_numeric(df["Drop_Longitude"], errors="coerce")
    r = 6371.0
    p1, p2 = lat1 * math.pi / 180, lat2 * math.pi / 180
    dp = (lat2 - lat1) * math.pi / 180
    dl = (lon2 - lon1) * math.pi / 180
    a = (dp / 2).apply(math.sin) ** 2 + p1.apply(math.cos) * p2.apply(math.cos) * (dl / 2).apply(math.sin) ** 2
    df["Approx_Distance_KM"] = 2 * r * a.clip(0, 1).apply(lambda x: math.asin(math.sqrt(x)))
    return df


def panel_heading(kicker, title, copy=None):
    st.markdown(f'<div class="panel-kicker">{kicker}</div><div class="panel-title">{title}</div>' + (f'<div class="panel-copy">{copy}</div>' if copy else ""), unsafe_allow_html=True)


def metric_card(label, value, note):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def style_chart(fig, height=350, legend=True):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=22, b=18),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Manrope, sans-serif", color=INK, size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10)) if legend else dict(orientation="h"),
        hoverlabel=dict(bgcolor=NAVY, font_size=11, font_family="Manrope, sans-serif", font_color="white"),
    )
    fig.update_xaxes(showgrid=False, linecolor="#DDE2E8", tickfont=dict(color=MUTED, size=10), title_font=dict(size=10, color=MUTED))
    fig.update_yaxes(gridcolor="#EDF0F3", zeroline=False, tickfont=dict(color=MUTED, size=10), title_font=dict(size=10, color=MUTED))
    return fig


def empty_state(message="No records match the current filter selection."):
    st.info(message)


if not DATA_PATH.exists():
    st.error("The dataset file is missing. Place `last_mile_delivery.csv` inside the `data` folder next to `app.py`.")
    st.stop()

try:
    raw = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

full_n = len(raw)
overall_mean = float(raw["Delivery_Time"].mean())
overall_std = float(raw["Delivery_Time"].std(ddof=1))
late_threshold = overall_mean + overall_std

# ------------------------------- Sidebar --------------------------------------
with st.sidebar:
    st.markdown("<div style='font-family:DM Mono,monospace;font-size:12px;letter-spacing:3px;color:#F28C28;font-weight:500;'>ROUTE//IQ</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:24px;line-height:1.15;font-weight:800;color:#FFFFFF;margin-top:7px;'>Control<br>your delivery<br>signals.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:DM Mono,monospace;font-size:9px;letter-spacing:1px;color:#8E9AAD;margin:12px 0 16px;'>LIVE FILTERS / DATA EXPLORER</div>", unsafe_allow_html=True)
    if st.button("↺  Reset all filters", use_container_width=True):
        for key in ["weather_filter", "traffic_filter", "vehicle_filter", "area_filter", "category_filter", "date_filter"]:
            st.session_state.pop(key, None)
        st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**01 / Conditions**")
    weather_options = sorted(raw["Weather"].dropna().unique().tolist())
    traffic_options = sorted(raw["Traffic"].dropna().unique().tolist())
    weather_sel = st.multiselect("Weather", weather_options, default=weather_options, key="weather_filter")
    traffic_sel = st.multiselect("Traffic", traffic_options, default=traffic_options, key="traffic_filter")
    st.markdown("**02 / Operations**")
    vehicle_options = sorted(raw["Vehicle"].dropna().unique().tolist())
    area_options = sorted(raw["Area"].dropna().unique().tolist())
    category_options = sorted(raw["Category"].dropna().unique().tolist())
    vehicle_sel = st.multiselect("Vehicle type", vehicle_options, default=vehicle_options, key="vehicle_filter")
    area_sel = st.multiselect("Area", area_options, default=area_options, key="area_filter")
    category_sel = st.multiselect("Product category", category_options, default=category_options, key="category_filter")
    st.markdown("**03 / Order window**")
    min_date = raw["Order_Date"].min().date()
    max_date = raw["Order_Date"].max().date()
    date_sel = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="date_filter")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:DM Mono,monospace;font-size:9px;color:#8E9AAD;line-height:1.8;'>DATASET / AMAZON LAST-MILE<br>ROWS / {full_n:,}<br>PERIOD / {min_date:%d %b %Y} — {max_date:%d %b %Y}<br>LATE RULE / MEAN + 1 SD</div>", unsafe_allow_html=True)

filtered = raw.copy()
filters = [
    ("Weather", weather_sel), ("Traffic", traffic_sel), ("Vehicle", vehicle_sel),
    ("Area", area_sel), ("Category", category_sel)
]
for col, chosen in filters:
    filtered = filtered[filtered[col].isin(chosen)] if chosen else filtered.iloc[0:0]
if isinstance(date_sel, (tuple, list)) and len(date_sel) == 2:
    d0, d1 = pd.Timestamp(date_sel[0]), pd.Timestamp(date_sel[1])
    filtered = filtered[filtered["Order_Date"].between(d0, d1 + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))]
elif date_sel:
    d0 = pd.Timestamp(date_sel)
    filtered = filtered[filtered["Order_Date"].dt.date == d0.date()]

# ------------------------------- Hero -----------------------------------------
st.markdown(
    f"""
    <div class="route-hero">
      <div class="route-wordmark">ROUTE<span style="color:#F8FAFC">//</span>IQ &nbsp; / &nbsp; DELIVERY INTELLIGENCE</div>
      <h1 class="route-title">Every delivery leaves<br>a signal.</h1>
      <div class="route-subtitle">A decision-support cockpit for last-mile operations. Compare delivery time across conditions, fleet, agents, places and product types — then investigate the signal, not just the number.</div>
      <div class="route-hero-bottom"><span class="route-chip route-chip-orange">FA-2 / INTERACTIVE DASHBOARD</span><span class="route-chip">{len(filtered):,} RECORDS IN VIEW</span><span class="route-chip">{len(raw.columns)} SOURCE FIELDS</span><span class="route-chip">PANDAS × PLOTLY × STREAMLIT</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-eyebrow">01 / Situation room</div><div class="section-title">Operations at a glance</div><div class="section-desc">Every headline metric responds to the current filters. Late delivery is defined by the assignment rule: delivery time greater than the full-dataset mean + one standard deviation.</div>', unsafe_allow_html=True)

if filtered.empty:
    empty_state("No records match these filters. Widen one or more selections in the sidebar.")
    view_mean = view_median = view_late_pct = view_rating = float("nan")
else:
    view_mean = filtered["Delivery_Time"].mean()
    view_median = filtered["Delivery_Time"].median()
    view_late_pct = 100 * filtered["Late_Flag"].mean()
    view_rating = filtered["Agent_Rating"].mean()

cols = st.columns(5, gap="small")
with cols[0]: metric_card("Deliveries in view", f"{len(filtered):,}", f"of {full_n:,} total records")
with cols[1]: metric_card("Average delivery", f"{view_mean:.1f}" if pd.notna(view_mean) else "—", "dataset units · lower is faster")
with cols[2]: metric_card("Median delivery", f"{view_median:.0f}" if pd.notna(view_median) else "—", "middle delivery-time record")
with cols[3]: metric_card("Late-delivery rate", f"{view_late_pct:.1f}%" if pd.notna(view_late_pct) else "—", f"threshold > {late_threshold:.1f} dataset units")
with cols[4]: metric_card("Average agent rating", f"{view_rating:.2f}" if pd.notna(view_rating) else "—", "available ratings only")

if not filtered.empty:
    traffic_means = filtered.groupby("Traffic", observed=False)["Delivery_Time"].mean().sort_values(ascending=False)
    weather_means = filtered.groupby("Weather", observed=False)["Delivery_Time"].mean().sort_values(ascending=False)
    insight_text = "Start by comparing all five required charts, then use filters to check whether the same pattern holds for a specific operating context."
    if len(traffic_means) and len(weather_means):
        worst_traffic, worst_weather = traffic_means.index[0], weather_means.index[0]
        insight_text = f"In the current selection, <strong>{worst_traffic}</strong> traffic has the highest average delivery time ({traffic_means.iloc[0]:.1f}), while <strong>{worst_weather}</strong> weather has the highest weather-group average ({weather_means.iloc[0]:.1f}). These are associations in the filtered records, not proof of causation."
    st.markdown(f'<div class="insight-band"><strong>READ THE SIGNAL →</strong> {insight_text}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-eyebrow">02 / Required analysis suite</div><div class="section-title">Five lenses. One delivery network.</div><div class="section-desc">These are the five compulsory visualisations named in the FA-2 brief. Each chart is calculated from the filtered records and includes contextual hover details where useful.</div>', unsafe_allow_html=True)

tab_delay, tab_vehicle, tab_agent, tab_area, tab_category = st.tabs([
    "01  DELAY ANALYZER", "02  VEHICLE COMPARISON", "03  AGENT PERFORMANCE", "04  AREA HEATMAP", "05  CATEGORY BOX PLOT"
])

with tab_delay:
    panel_heading("Required visual 01", "Where time starts to stretch", "Average delivery time by weather, split by traffic condition. Hover on each bar for delivery count and the exact mean.")
    if filtered.empty:
        empty_state()
    else:
        delay = filtered.groupby(["Weather", "Traffic"], observed=False).agg(
            Avg_Delivery=("Delivery_Time", "mean"), Deliveries=("Delivery_Time", "size")
        ).reset_index()
        fig = px.bar(delay, x="Weather", y="Avg_Delivery", color="Traffic", barmode="group", color_discrete_sequence=PALETTE,
                     custom_data=["Deliveries"], labels={"Weather":"Weather condition", "Avg_Delivery":"Average delivery time", "Traffic":"Traffic"})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Traffic: %{fullData.name}<br>Average: %{y:.1f}<br>Deliveries: %{customdata[0]:,}<extra></extra>", marker_line_width=0)
        fig.update_layout(yaxis_title="Average delivery time (dataset units)", xaxis_title="", bargap=.20, bargroupgap=.08)
        style_chart(fig, 390)
        st.plotly_chart(fig, use_container_width=True, key="delay_chart")
        if len(delay):
            high = delay.loc[delay["Avg_Delivery"].idxmax()]
            st.markdown(f'<div class="note-band"><strong>How to read it:</strong> the tallest bar is {high["Weather"]} / {high["Traffic"]} at {high["Avg_Delivery"]:.1f} average delivery-time units ({int(high["Deliveries"]):,} records). Check its count before prioritising action.</div>', unsafe_allow_html=True)

with tab_vehicle:
    panel_heading("Required visual 02", "The fleet, ranked by time", "Compare average delivery time by vehicle type; record counts remain visible so small groups are not mistaken for robust evidence.")
    if filtered.empty:
        empty_state()
    else:
        v = filtered.groupby("Vehicle", observed=False).agg(Avg_Delivery=("Delivery_Time", "mean"), Median=("Delivery_Time", "median"), Deliveries=("Delivery_Time", "size")).reset_index().sort_values("Avg_Delivery")
        fig = px.bar(v, x="Avg_Delivery", y="Vehicle", orientation="h", color="Avg_Delivery", color_continuous_scale=[[0,"#2C9C91"],[.5,"#E8B064"],[1,"#F28C28"]],
                     custom_data=["Median", "Deliveries"], labels={"Avg_Delivery":"Average delivery time", "Vehicle":"Vehicle type"})
        fig.update_traces(hovertemplate="<b>%{y}</b><br>Average: %{x:.1f}<br>Median: %{customdata[0]:.1f}<br>Deliveries: %{customdata[1]:,}<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title="Average delivery time (dataset units)", yaxis_title="", showlegend=False)
        style_chart(fig, 350, legend=False)
        st.plotly_chart(fig, use_container_width=True, key="vehicle_chart")
        low_n = v[v["Deliveries"] < 50]
        if not low_n.empty:
            st.markdown('<div class="note-band"><strong>Sample-size caution:</strong> ' + "; ".join(f"{r.Vehicle} has only {int(r.Deliveries)} deliveries" for r in low_n.itertuples()) + ". Treat small groups as a prompt for further checking, not a fleet decision on their own.</div>", unsafe_allow_html=True)

with tab_agent:
    panel_heading("Required visual 03", "Rating is a clue, not a verdict", "Agent rating on the x-axis and delivery time on the y-axis, coloured by age group. Patterns are descriptive; age and rating alone do not prove performance or cause.")
    if filtered.empty:
        empty_state()
    else:
        scatter_data = filtered.dropna(subset=["Agent_Rating", "Delivery_Time", "Agent_Age_Group"]).copy()
        if len(scatter_data) > 8000:
            scatter_data = scatter_data.sample(8000, random_state=23)
        fig = px.scatter(scatter_data, x="Agent_Rating", y="Delivery_Time", color="Agent_Age_Group", color_discrete_sequence=PALETTE,
                         opacity=.56, hover_data={"Agent_Age":True, "Vehicle":True, "Traffic":True, "Weather":True, "Delivery_Time":":.0f"},
                         labels={"Agent_Rating":"Agent rating", "Delivery_Time":"Delivery time", "Agent_Age_Group":"Agent age group"})
        fig.update_traces(marker=dict(size=7, line=dict(width=0)))
        fig.update_layout(xaxis_title="Agent rating (source scale needs validation)", yaxis_title="Delivery time (dataset units)")
        style_chart(fig, 390)
        st.plotly_chart(fig, use_container_width=True, key="agent_chart")
        valid_corr = scatter_data[["Agent_Rating", "Delivery_Time"]].corr().iloc[0, 1] if len(scatter_data) > 1 else float("nan")
        st.markdown(f'<div class="note-band"><strong>Exploratory association:</strong> correlation in the plotted subset = {valid_corr:.3f} (where calculable). The source contains missing ratings and values up to 6; confirm the intended rating scale before setting business rules.</div>', unsafe_allow_html=True)

with tab_area:
    panel_heading("Required visual 04", "Where the network runs hot", "Heatmap of average delivery time by area and traffic condition. Darker/brighter cells indicate higher averages; hover to see the exact value.")
    if filtered.empty:
        empty_state()
    else:
        pivot = filtered.pivot_table(index="Area", columns="Traffic", values="Delivery_Time", aggfunc="mean", observed=False)
        # Put common traffic conditions in a consistent order, with Unknown last.
        col_order = [x for x in ["Low", "Medium", "High", "Jam", "Unknown"] if x in pivot.columns]
        pivot = pivot.reindex(columns=col_order)
        area_order = filtered.groupby("Area", observed=False)["Delivery_Time"].mean().sort_values(ascending=False).index.tolist()
        pivot = pivot.reindex(area_order)
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0,"#FCE7CD"],[.45,"#F4A340"],[1,"#BA4B14"]],
            text=[[f"{v:.1f}" if pd.notna(v) else "—" for v in row] for row in pivot.values],
            texttemplate="%{text}", textfont={"size":12,"color":"#17212F"},
            colorbar=dict(title="Avg time", tickfont=dict(size=9)),
            hovertemplate="Area: %{y}<br>Traffic: %{x}<br>Avg delivery: %{z:.1f}<extra></extra>"
        ))
        fig.update_layout(xaxis_title="Traffic condition", yaxis_title="Area", coloraxis_showscale=True)
        style_chart(fig, max(280, 78 * len(pivot.index)), legend=False)
        st.plotly_chart(fig, use_container_width=True, key="area_heatmap")
        area_counts = filtered.groupby("Area", observed=False).size().sort_values()
        small_areas = area_counts[area_counts < 250]
        if len(small_areas):
            st.markdown('<div class="note-band"><strong>Coverage note:</strong> low-volume areas are still shown, but their averages are less stable. The current selection includes: ' + ", ".join(f"{idx} ({int(val):,})" for idx,val in small_areas.items()) + ".</div>", unsafe_allow_html=True)

with tab_category:
    panel_heading("Required visual 05", "The average can hide the story", "A box plot shows the median, spread and unusual values for each product category. This is safer than comparing averages alone.")
    if filtered.empty:
        empty_state()
    else:
        cat_order = filtered.groupby("Category", observed=False)["Delivery_Time"].median().sort_values().index.tolist()
        fig = px.box(filtered, x="Category", y="Delivery_Time", color="Category", category_orders={"Category":cat_order}, color_discrete_sequence=PALETTE, points=False,
                     labels={"Category":"Product category", "Delivery_Time":"Delivery time (dataset units)"})
        fig.update_traces(line_width=1.5, marker_size=3, showlegend=False)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Delivery time (dataset units)")
        style_chart(fig, 420, legend=False)
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(fig, use_container_width=True, key="category_boxplot")
        cat_stats = filtered.groupby("Category", observed=False)["Delivery_Time"].agg(["count", "mean", "median"]).sort_values("median")
        if "Grocery" in cat_stats.index and cat_stats["median"].min() < cat_stats["median"].median() * .5:
            st.markdown('<div class="note-band"><strong>Data-quality flag:</strong> Grocery delivery times in this workbook are substantially lower than most other categories. Verify units, record definitions and source data before treating this as a real operational advantage.</div>', unsafe_allow_html=True)

# ------------------------------- Optional visuals -----------------------------
st.markdown('<div class="section-eyebrow">03 / Additional intelligence</div><div class="section-title">Go beyond the required five</div><div class="section-desc">The assignment allows optional visualisations. These three add a time trend, a view of distribution and a consistent late-delivery comparison.</div>', unsafe_allow_html=True)
opt1, opt2, opt3 = st.columns([1.1, 1, 1], gap="medium")
with opt1:
    panel_heading("Optional 01", "Is the pattern changing over time?", "Monthly average delivery time")
    if filtered.empty or filtered["Order_Month"].notna().sum() == 0:
        empty_state()
    else:
        m = filtered.dropna(subset=["Order_Month"]).groupby("Order_Month").agg(Avg_Delivery=("Delivery_Time", "mean"), Deliveries=("Delivery_Time", "size")).reset_index()
        fig = px.line(m, x="Order_Month", y="Avg_Delivery", markers=True, color_discrete_sequence=[ORANGE], custom_data=["Deliveries"],
                      labels={"Order_Month":"Order month", "Avg_Delivery":"Average delivery time"})
        fig.update_traces(line_width=3, marker_size=7, hovertemplate="%{x|%b %Y}<br>Average: %{y:.1f}<br>Deliveries: %{customdata[0]:,}<extra></extra>")
        fig.update_layout(xaxis_title="", yaxis_title="Avg time")
        style_chart(fig, 270, legend=False)
        st.plotly_chart(fig, use_container_width=True, key="monthly_trend")
with opt2:
    panel_heading("Optional 02", "What does a typical order look like?", "Delivery-time distribution")
    if filtered.empty:
        empty_state()
    else:
        fig = px.histogram(filtered, x="Delivery_Time", nbins=30, color_discrete_sequence=[BLUE], labels={"Delivery_Time":"Delivery time (dataset units)"})
        fig.update_traces(marker_line_width=0, opacity=.92, hovertemplate="Delivery time: %{x}<br>Records: %{y:,}<extra></extra>")
        fig.update_layout(xaxis_title="Delivery time", yaxis_title="Number of deliveries")
        style_chart(fig, 270, legend=False)
        st.plotly_chart(fig, use_container_width=True, key="delivery_histogram")
with opt3:
    panel_heading("Optional 03", "Where does late risk cluster?", "Percentage above the fixed mean + 1 SD threshold")
    if filtered.empty:
        empty_state()
    else:
        late = filtered.groupby("Traffic", observed=False).agg(Late_Rate=("Late_Flag", "mean"), Deliveries=("Late_Flag", "size")).reset_index()
        late["Late_Rate_Pct"] = late["Late_Rate"] * 100
        late = late.sort_values("Late_Rate_Pct", ascending=True)
        fig = px.bar(late, x="Late_Rate_Pct", y="Traffic", orientation="h", color="Late_Rate_Pct", color_continuous_scale=[[0,"#B9DCD6"],[.6,"#F4A340"],[1,"#C55C31"]], custom_data=["Deliveries"],
                     labels={"Late_Rate_Pct":"Late deliveries (%)", "Traffic":"Traffic"})
        fig.update_traces(hovertemplate="%{y}<br>Late: %{x:.1f}%<br>Deliveries: %{customdata[0]:,}<extra></extra>")
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title="Late deliveries (%)", yaxis_title="", showlegend=False)
        style_chart(fig, 270, legend=False)
        st.plotly_chart(fig, use_container_width=True, key="late_rate_traffic")

# ------------------------------- Data stewardship -----------------------------
st.markdown('<div class="section-eyebrow">04 / Trust the numbers</div><div class="section-title">Data quality & calculation notes</div><div class="section-desc">A dashboard should make its limitations visible. The rules below are documented so a manager can interpret results responsibly.</div>', unsafe_allow_html=True)
with st.expander("Open data checks and preparation rules", expanded=False):
    original = pd.read_csv(DATA_PATH)
    check_cols = st.columns(4)
    with check_cols[0]: metric_card("Missing weather", f"{int(original['Weather'].isna().sum()):,}", "shown as Unknown in filters")
    with check_cols[1]: metric_card("Missing traffic", f"{int(original['Traffic'].isna().sum()):,}", "shown as Unknown in filters")
    with check_cols[2]: metric_card("Missing ratings", f"{int(original['Agent_Rating'].isna().sum()):,}", "excluded only from rating visuals")
    with check_cols[3]: metric_card("Duplicate order IDs", f"{int(original['Order_ID'].duplicated().sum()):,}", "inspect before deduplicating")
    st.markdown("**Preparation applied**")
    st.markdown("- Text categories are trimmed; missing Weather and Traffic values are retained as `Unknown` so the missingness remains visible.\n- Delivery_Time is converted to numeric and records without a valid Delivery_Time are excluded from analysis.\n- Agent_Rating remains missing where absent; no rating values are silently invented or capped.\n- `Late_Flag` is fixed using the full prepared dataset mean + one standard deviation, then reported within the active filter selection.\n- Monthly trend uses `Order_Date`. Approximate straight-line distance is calculated only for optional context; it is not road distance.")
    st.markdown(f"**Late threshold:** {late_threshold:.2f} dataset units (full-dataset mean {overall_mean:.2f} + standard deviation {overall_std:.2f}).")
    st.markdown("**Interpretation limits:** observed differences describe this workbook; they do not prove weather, traffic, age, ratings or vehicle type independently cause delivery delays. Small groups need cautious interpretation. Category results should be checked against source definitions, especially unusually low Grocery values.")

with st.expander("Inspect the filtered data table", expanded=False):
    show_cols = ["Order_ID", "Order_Date", "Weather", "Traffic", "Vehicle", "Area", "Category", "Agent_Age", "Agent_Rating", "Delivery_Time", "Late_Flag", "Approx_Distance_KM"]
    st.dataframe(filtered[show_cols].head(500), use_container_width=True, hide_index=True)
    st.caption(f"Showing up to 500 rows of {len(filtered):,} filtered records. Use the filters to narrow the selection.")

st.markdown(
    "<div class='footer-line'>ROUTE//IQ &nbsp; · &nbsp; MATHEMATICS FOR AI-II / FA-2 &nbsp; · &nbsp; DATA PREPARATION: PANDAS &nbsp; · &nbsp; VISUALS: PLOTLY &nbsp; · &nbsp; INTERACTION: STREAMLIT<br>DESIGNED FOR OPERATIONAL EXPLORATION — NOT AS A SUBSTITUTE FOR CONTEXTUAL REVIEW.</div>",
    unsafe_allow_html=True,
)
