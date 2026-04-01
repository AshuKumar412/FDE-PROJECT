# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime
# import sys, os, subprocess

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pipeline.load import query_database

# st.set_page_config(
#     page_title="Medic · Analytics",
#     page_icon="⬡",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─────────────────────────────────────────────────────────────────────────────
# # GLOBAL CSS  (static only — zero dynamic values injected here)
# # This is the only place we use class names. Dynamic HTML always uses inline styles.
# # ─────────────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500&display=swap');

# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif !important;
#     background-color: #0a0d12 !important;
#     color: #edf2f7 !important;
# }
# .main .block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }

# [data-testid="stSidebar"] {
#     background: #111520 !important;
#     border-right: 1px solid rgba(255,255,255,0.06) !important;
# }
# [data-testid="stSidebar"] * { color: #edf2f7 !important; }
# [data-testid="stSidebar"] .stSelectbox > div > div {
#     background: #161b27 !important;
#     border-color: rgba(255,255,255,0.08) !important;
#     border-radius: 8px !important;
# }
# .stSelectbox > div > div {
#     background: #161b27 !important;
#     border-color: rgba(255,255,255,0.08) !important;
#     border-radius: 8px !important;
# }
# .stTextInput > div > div input {
#     background: #161b27 !important;
#     border-color: rgba(255,255,255,0.08) !important;
#     border-radius: 8px !important;
#     color: #edf2f7 !important;
# }
# .stAlert {
#     background: #161b27 !important;
#     border: 1px solid rgba(255,255,255,0.06) !important;
#     border-radius: 10px !important;
# }
# .stButton > button {
#     background: transparent !important;
#     border: 1px solid rgba(99,179,237,0.35) !important;
#     color: #63b3ed !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.78rem !important;
#     letter-spacing: 0.06em !important;
#     border-radius: 8px !important;
# }
# .stButton > button:hover { background: rgba(99,179,237,0.08) !important; }
# .stDownloadButton > button {
#     background: linear-gradient(135deg, #63b3ed, #4fd1c5) !important;
#     color: #0a0d12 !important;
#     border: none !important;
#     font-weight: 600 !important;
#     border-radius: 8px !important;
#     font-size: 0.8rem !important;
#     letter-spacing: 0.04em !important;
# }
# [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
# @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.25;} }
# .live-dot { animation: pulse 2s infinite; }
# ::-webkit-scrollbar { width: 4px; height: 4px; }
# ::-webkit-scrollbar-track { background: #0a0d12; }
# ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 2px; }
# </style>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────────────────────────────────────────
# # DESIGN TOKENS
# # ─────────────────────────────────────────────────────────────────────────────
# C_BG     = "#0a0d12"
# C_CARD   = "#111520"
# C_SUBTLE = "#161b27"
# C_BORDER = "rgba(255,255,255,0.06)"
# C_TEXT   = "#edf2f7"
# C_SEC    = "#a0aec0"
# C_MUTED  = "#4a5568"
# C_TEAL   = "#63b3ed"
# C_MINT   = "#4fd1c5"
# C_AMBER  = "#f6ad55"
# C_VIOLET = "#b794f4"
# C_ROSE   = "#fc8181"

# TEAL_SCALE   = [[0, "#1a3a4a"], [0.5, "#2c7a99"], [1, C_TEAL]]
# MINT_SCALE   = [[0, "#1a4040"], [0.5, "#2c9999"], [1, C_MINT]]

# BASE_LAYOUT = dict(
#     paper_bgcolor="rgba(0,0,0,0)",
#     plot_bgcolor="rgba(0,0,0,0)",
#     font=dict(family="DM Sans", color=C_SEC, size=11),
#     title_font=dict(family="DM Serif Display", color=C_TEXT, size=15),
#     xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.05)", tickcolor="rgba(255,255,255,0.04)"),
#     yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.05)", tickcolor="rgba(255,255,255,0.04)"),
#     margin=dict(l=20, r=20, t=52, b=20),
#     hoverlabel=dict(bgcolor="#161b27", bordercolor="rgba(255,255,255,0.1)", font=dict(color=C_TEXT)),
#     legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=C_BORDER),
# )

# def apply_layout(fig, **kw):
#     fig.update_layout(**{**BASE_LAYOUT, **kw})
#     return fig

# # ─────────────────────────────────────────────────────────────────────────────
# # HTML HELPERS  (all inline styles — never reference CSS classes)
# # ─────────────────────────────────────────────────────────────────────────────

# def _div(style, content):
#     return f'<div style="{style}">{content}</div>'

# def insight_row(label, value, color=None):
#     color = color or C_TEAL
#     return (
#         f'<div style="display:flex;justify-content:space-between;align-items:center;'
#         f'padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:.82rem;">'
#         f'<span style="color:{C_SEC};">{label}</span>'
#         f'<span style="font-family:DM Mono,monospace;font-size:.8rem;color:{color};">{value}</span>'
#         f'</div>'
#     )

# def card(content, extra_style=""):
#     return (
#         f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;'
#         f'padding:1.4rem 1.5rem;{extra_style}">{content}</div>'
#     )

# def card_header(title, dot_color):
#     return (
#         f'<div style="font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;'
#         f'color:{C_MUTED};margin-bottom:1rem;display:flex;align-items:center;gap:6px;">'
#         f'<div style="width:5px;height:5px;border-radius:50%;background:{dot_color};flex-shrink:0;"></div>'
#         f'{title}</div>'
#     )

# def chart_subtitle(text):
#     return (
#         f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;'
#         f'padding:1.2rem 1.4rem 0.3rem;">'
#         f'<div style="font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:{C_MUTED};">'
#         f'{text}</div></div>'
#     )

# def section_header(text):
#     st.markdown(
#         f'<div style="display:flex;align-items:center;gap:12px;margin:2rem 0 1rem;">'
#         f'<span style="font-family:DM Serif Display,serif;font-size:1.2rem;color:{C_TEXT};white-space:nowrap;">'
#         f'{text}</span>'
#         f'<div style="flex:1;height:1px;background:{C_BORDER};"></div></div>',
#         unsafe_allow_html=True
#     )

# def sidebar_label(text):
#     st.markdown(
#         f'<div style="font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;'
#         f'color:{C_MUTED};padding:.5rem 0 .2rem;">{text}</div>',
#         unsafe_allow_html=True
#     )

# def sidebar_divider():
#     st.markdown(
#         f'<hr style="border:none;border-top:1px solid {C_BORDER};margin:.6rem 0;">',
#         unsafe_allow_html=True
#     )

# # ─────────────────────────────────────────────────────────────────────────────
# # DATA
# # ─────────────────────────────────────────────────────────────────────────────

# @st.cache_data(ttl=3600)
# def load_data():
#     try:
#         df = query_database()
#         return df if df is not None and len(df) > 0 else None
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return None

# # ─────────────────────────────────────────────────────────────────────────────
# # KPI CARDS
# # ─────────────────────────────────────────────────────────────────────────────

# def create_kpi_cards(df):
#     n_patients  = df["patient_id"].nunique() if "patient_id" in df.columns else len(df)
#     revenue     = df["amount"].sum()  if "amount" in df.columns else 0
#     avg_cost    = df["amount"].mean() if "amount" in df.columns else 0
#     tc          = df["treatment_type"].value_counts() if "treatment_type" in df.columns else pd.Series()
#     top_tx      = str(tc.index[0])[:22] if len(tc) else "—"
#     completion  = 0.0
#     if "status" in df.columns and len(df):
#         completion = len(df[df["status"] == "Completed"]) / len(df) * 100

#     kpi_data = [
#         (C_TEAL,   f"{n_patients:,}",   "Total Patients",     "↑ Active cohort"),
#         (C_MINT,   f"${revenue:,.0f}",  "Total Revenue",      "Gross billings"),
#         (C_AMBER,  f"${avg_cost:,.0f}", "Avg Treatment Cost", "Per encounter"),
#         (C_VIOLET, top_tx,              "Top Treatment",      "By volume"),
#     ]

#     cols = st.columns(4)
#     for col, (color, value, label, delta) in zip(cols, kpi_data):
#         with col:
#             st.markdown(
#                 f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;padding:1.4rem 1.5rem;">'
#                 f'<div style="width:3px;height:36px;border-radius:2px;background:{color};margin-bottom:1rem;"></div>'
#                 f'<div style="font-family:DM Serif Display,serif;font-size:2rem;line-height:1;margin-bottom:.3rem;color:{C_TEXT};">{value}</div>'
#                 f'<div style="font-size:.72rem;color:{C_MUTED};letter-spacing:.06em;text-transform:uppercase;">{label}</div>'
#                 f'<div style="font-family:DM Mono,monospace;font-size:.72rem;margin-top:.6rem;color:{color};">{delta}</div>'
#                 f'</div>',
#                 unsafe_allow_html=True
#             )

#     pct = f"{completion:.1f}"
#     st.markdown(
#         f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:10px;'
#         f'padding:1rem 1.5rem;margin:1rem 0 2rem;display:flex;align-items:center;gap:1.2rem;">'
#         f'<div style="font-size:.72rem;color:{C_MUTED};letter-spacing:.07em;text-transform:uppercase;white-space:nowrap;min-width:200px;">Appointment Completion</div>'
#         f'<div style="flex:1;height:4px;background:{C_SUBTLE};border-radius:2px;overflow:hidden;">'
#         f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{C_TEAL},{C_MINT});border-radius:2px;"></div></div>'
#         f'<div style="font-family:DM Mono,monospace;font-size:.8rem;color:{C_TEAL};min-width:40px;text-align:right;">{pct}%</div>'
#         f'</div>',
#         unsafe_allow_html=True
#     )

# # ─────────────────────────────────────────────────────────────────────────────
# # CHARTS
# # ─────────────────────────────────────────────────────────────────────────────

# def fig_treatment(df):
#     if "treatment_type" not in df.columns:
#         return None
#     tc = df["treatment_type"].value_counts().head(10).reset_index()
#     tc.columns = ["Treatment", "Count"]
#     fig = go.Figure(go.Bar(
#         x=tc["Treatment"], y=tc["Count"],
#         marker=dict(color=tc["Count"], colorscale=TEAL_SCALE, showscale=False,
#                     line=dict(color="rgba(0,0,0,0)", width=0)),
#         text=tc["Count"], textposition="outside", textfont=dict(color=C_SEC, size=10),
#     ))
#     return apply_layout(fig, title="Treatment Volume", xaxis_tickangle=30, height=360)

# def fig_revenue(df):
#     if "Month" not in df.columns or "amount" not in df.columns:
#         return None
#     m = df.groupby("Month")["amount"].sum().reset_index().sort_values("Month")
#     fig = go.Figure(go.Scatter(
#         x=m["Month"], y=m["amount"], mode="lines+markers",
#         line=dict(width=2.5, color=C_TEAL),
#         marker=dict(size=7, color=C_MINT, line=dict(color=C_BG, width=2)),
#         fill="tozeroy", fillcolor="rgba(99,179,237,0.07)",
#     ))
#     apply_layout(fig, title="Monthly Revenue Trend", height=360)
#     fig.update_yaxes(tickprefix="$")
#     return fig

# def fig_payment(df):
#     PAL = {"Paid": C_MINT, "Pending": C_AMBER, "Failed": C_ROSE}
#     if "payment_status" in df.columns:
#         sc = df["payment_status"].value_counts()
#         colors = [PAL.get(str(s), C_VIOLET) for s in sc.index]
#     elif "status" in df.columns:
#         sc = df["status"].value_counts()
#         colors = [C_MINT, C_TEAL, C_ROSE, C_AMBER][: len(sc)]
#     else:
#         return None
#     fig = go.Figure(go.Pie(
#         labels=sc.index, values=sc.values, hole=0.55,
#         marker=dict(colors=colors, line=dict(color=C_BG, width=2)),
#         textinfo="percent", textfont=dict(size=11),
#     ))
#     fig.add_annotation(text="Status", x=0.5, y=0.5, showarrow=False,
#                        font=dict(size=11, color=C_MUTED))
#     return apply_layout(fig, title="Payment Distribution", height=360,
#                         legend=dict(orientation="v", x=1, y=0.5, bgcolor="rgba(0,0,0,0)"))

# def fig_gender(df):
#     if "gender" not in df.columns:
#         return None
#     gc = df["gender"].value_counts()
#     fig = go.Figure(go.Pie(
#         labels=gc.index, values=gc.values, hole=0.55,
#         marker=dict(colors=[C_TEAL, C_VIOLET, C_MINT], line=dict(color=C_BG, width=2)),
#         textinfo="percent", textfont=dict(size=11),
#     ))
#     fig.add_annotation(text="Gender", x=0.5, y=0.5, showarrow=False,
#                        font=dict(size=11, color=C_MUTED))
#     return apply_layout(fig, title="Gender Distribution", height=360)

# def fig_age(df):
#     if "Age" not in df.columns:
#         return None
#     mu = df["Age"].mean()
#     fig = go.Figure(go.Histogram(
#         x=df["Age"], nbinsx=22,
#         marker=dict(color=C_TEAL, opacity=0.8, line=dict(color=C_BG, width=0.5)),
#     ))
#     fig.add_vline(x=mu, line_dash="dot", line_color=C_AMBER, line_width=1.5,
#                   annotation_text=f"μ {mu:.1f}",
#                   annotation_font=dict(color=C_AMBER, size=11))
#     return apply_layout(fig, title="Age Distribution", height=360)

# def fig_doctors(df):
#     if "amount" not in df.columns:
#         return None
#     dcol = None
#     for col in df.columns:
#         if "doctor" in col.lower() and ("name" in col.lower() or "first_name" in col.lower()):
#             dcol = col; break
#     if not dcol and "first_name" in df.columns and "last_name" in df.columns:
#         df = df.copy()
#         df["_doc"] = df["first_name"] + " " + df["last_name"]
#         dcol = "_doc"
#     if not dcol:
#         return None
#     rev = df.groupby(dcol)["amount"].sum().sort_values(ascending=True).tail(10)
#     fig = go.Figure(go.Bar(
#         y=rev.index, x=rev.values, orientation="h",
#         marker=dict(color=rev.values, colorscale=MINT_SCALE, showscale=False,
#                     line=dict(color="rgba(0,0,0,0)", width=0)),
#         text=[f"${v:,.0f}" for v in rev.values],
#         textposition="outside", textfont=dict(color=C_SEC, size=10),
#     ))
#     apply_layout(fig, title="Top 10 Physicians by Revenue", height=400,
#                  margin=dict(l=130, r=40, t=52, b=20))
#     fig.update_xaxes(tickprefix="$")
#     return fig

# def fig_cost_dist(df):
#     if "treatment_type" not in df.columns or "amount" not in df.columns:
#         return None
#     top = df["treatment_type"].value_counts().head(8).index
#     palette = [C_TEAL, C_MINT, C_VIOLET, C_AMBER, C_ROSE, "#68d391", "#76e4f7", "#fbd38d"]
#     fig = go.Figure()
#     for i, t in enumerate(top):
#         c = palette[i % len(palette)]
#         r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
#         fig.add_trace(go.Box(
#             y=df[df["treatment_type"] == t]["amount"], name=t,
#             boxmean="sd", marker_color=c, line_color=c,
#             fillcolor=f"rgba({r},{g},{b},0.12)",
#         ))
#     apply_layout(fig, title="Cost Distribution by Treatment", height=420,
#                  showlegend=False,
#                  xaxis=dict(**BASE_LAYOUT["xaxis"], tickangle=30))
#     fig.update_yaxes(tickprefix="$")
#     return fig

# # ─────────────────────────────────────────────────────────────────────────────
# # CHART COLUMN HELPER
# # ─────────────────────────────────────────────────────────────────────────────

# def render_chart(col, subtitle, make_fig, df):
#     with col:
#         st.markdown(chart_subtitle(subtitle), unsafe_allow_html=True)
#         f = make_fig(df)
#         if f:
#             st.plotly_chart(f, use_container_width=True, config={"displayModeBar": False})

# # ─────────────────────────────────────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────────────────────────────────────

# def create_sidebar_filters(df):
#     with st.sidebar:
#         # Brand
#         st.markdown(
#             f'<div style="display:flex;align-items:center;gap:10px;padding:1.4rem 1.2rem 1rem;">'
#             f'<div style="width:36px;height:36px;flex-shrink:0;'
#             f'background:linear-gradient(135deg,{C_TEAL},{C_MINT});'
#             f'clip-path:polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);"></div>'
#             f'<div>'
#             f'<div style="font-family:DM Serif Display,serif;font-size:1.2rem;">Medic</div>'
#             f'<div style="font-size:.65rem;color:{C_MUTED};letter-spacing:.1em;text-transform:uppercase;">Analytics Platform</div>'
#             f'</div></div>',
#             unsafe_allow_html=True
#         )
#         sidebar_divider()

#         fdf = df.copy()

#         # Date
#         dcol = next((c for c in ["appointment_date","date","bill_date","treatment_date"] if c in df.columns), None)
#         if dcol:
#             sidebar_label("Date Range")
#             mn = pd.to_datetime(df[dcol]).min()
#             mx = pd.to_datetime(df[dcol]).max()
#             dr = st.date_input("", [mn, mx], min_value=mn, max_value=mx, label_visibility="collapsed")
#             if len(dr) == 2:
#                 mask = (pd.to_datetime(df[dcol]) >= pd.to_datetime(dr[0])) & \
#                        (pd.to_datetime(df[dcol]) <= pd.to_datetime(dr[1]))
#                 fdf = df[mask]
#             sidebar_divider()

#         if "treatment_type" in df.columns:
#             sidebar_label("Treatment")
#             opts = ["All"] + sorted(df["treatment_type"].dropna().unique().tolist())
#             sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_treat")
#             if sel != "All":
#                 fdf = fdf[fdf["treatment_type"] == sel]
#             sidebar_divider()

#         if "status" in df.columns:
#             sidebar_label("Appointment Status")
#             opts = ["All"] + sorted(df["status"].dropna().unique().tolist())
#             sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_status")
#             if sel != "All":
#                 fdf = fdf[fdf["status"] == sel]
#             sidebar_divider()

#         if "payment_status" in df.columns:
#             sidebar_label("Payment Status")
#             opts = ["All"] + sorted(df["payment_status"].dropna().unique().tolist())
#             sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_pay")
#             if sel != "All":
#                 fdf = fdf[fdf["payment_status"] == sel]
#             sidebar_divider()

#         if "amount" in df.columns:
#             sidebar_label("Cost Range")
#             lo, hi = float(df["amount"].min()), float(df["amount"].max())
#             rng = st.slider("", lo, hi, (lo, hi), format="$%.0f", label_visibility="collapsed")
#             fdf = fdf[(fdf["amount"] >= rng[0]) & (fdf["amount"] <= rng[1])]
#             sidebar_divider()

#         # Mini stats — build entirely as one safe string
#         total_r = fdf["amount"].sum()  if "amount"     in fdf.columns else 0
#         pt      = fdf["patient_id"].nunique() if "patient_id" in fdf.columns else "—"
#         n       = len(fdf)

#         st.markdown(
#             f'<div style="padding:.9rem 1.1rem;background:rgba(99,179,237,0.05);border-radius:10px;'
#             f'border:1px solid rgba(99,179,237,0.1);">'
#             f'<div style="font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:{C_MUTED};margin-bottom:8px;">Current View</div>'
#             f'<div style="font-size:.78rem;line-height:2;">'
#             f'Records<span style="color:{C_TEAL};font-family:DM Mono,monospace;float:right;">{n:,}</span><br>'
#             f'Patients<span style="color:{C_TEAL};font-family:DM Mono,monospace;float:right;">{pt}</span><br>'
#             f'Revenue<span style="color:{C_MINT};font-family:DM Mono,monospace;float:right;">${total_r:,.0f}</span>'
#             f'</div></div>',
#             unsafe_allow_html=True
#         )
#         st.markdown("<br>", unsafe_allow_html=True)
#         if st.button("↺  Reset Filters", use_container_width=True):
#             st.rerun()

#     return fdf

# # ─────────────────────────────────────────────────────────────────────────────
# # INSIGHTS
# # ─────────────────────────────────────────────────────────────────────────────

# def display_insights(df):
#     # Build lists of row strings, then join — never embed inside a wrapping f-string
#     rev, ptr, trt = [], [], []

#     if "amount" in df.columns:
#         rev = [
#             insight_row("Total Revenue",   f"${df['amount'].sum():,.0f}",    C_TEAL),
#             insight_row("Average Cost",    f"${df['amount'].mean():,.0f}",   C_TEAL),
#             insight_row("Median Cost",     f"${df['amount'].median():,.0f}", C_TEAL),
#             insight_row("Max Single Bill", f"${df['amount'].max():,.0f}",    C_AMBER),
#         ]

#     if "gender" in df.columns:
#         for g, c in df["gender"].value_counts().items():
#             ptr.append(insight_row(str(g), f"{c:,}  ({c/len(df)*100:.1f}%)", C_VIOLET))
#     if "Age" in df.columns:
#         ptr += [
#             insight_row("Avg Age",   f"{df['Age'].mean():.1f} yrs",                    C_VIOLET),
#             insight_row("Age Range", f"{df['Age'].min():.0f}–{df['Age'].max():.0f}",   C_VIOLET),
#         ]

#     if "treatment_type" in df.columns:
#         mode = df["treatment_type"].mode()
#         mc = str(mode.iloc[0]) if not mode.empty else "—"
#         trt.append(insight_row("Most Common",  mc,                                 C_MINT))
#         trt.append(insight_row("Unique Types", str(df["treatment_type"].nunique()), C_MINT))
#         if "amount" in df.columns:
#             top = str(df.groupby("treatment_type")["amount"].sum().idxmax())
#             trt.append(insight_row("Top Revenue", top, C_MINT))

#     def _card(dot, title, rows):
#         return card(card_header(title, dot) + "".join(rows))

#     c1, c2, c3 = st.columns(3)
#     with c1:
#         st.markdown(_card(C_TEAL,   "Revenue Insights",   rev), unsafe_allow_html=True)
#     with c2:
#         st.markdown(_card(C_VIOLET, "Patient Insights",   ptr), unsafe_allow_html=True)
#     with c3:
#         st.markdown(_card(C_MINT,   "Treatment Insights", trt), unsafe_allow_html=True)

# # ─────────────────────────────────────────────────────────────────────────────
# # MAIN
# # ─────────────────────────────────────────────────────────────────────────────

# def main():
#     now = datetime.now().strftime("%d %b %Y, %H:%M")

#     # ── Page header ───────────────────────────────────────────────────────────
#     st.markdown(
#         f'<div style="display:flex;align-items:flex-end;justify-content:space-between;'
#         f'margin-bottom:2.4rem;padding-bottom:1.4rem;border-bottom:1px solid {C_BORDER};">'

#         f'<div>'
#         f'<div style="font-family:DM Serif Display,serif;font-size:2.6rem;line-height:1.1;'
#         f'letter-spacing:-.02em;background:linear-gradient(120deg,{C_TEXT} 30%,{C_TEAL});'
#         f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
#         f'Healthcare Analytics</div>'
#         f'<div style="font-size:.78rem;color:{C_MUTED};letter-spacing:.07em;text-transform:uppercase;margin-top:.3rem;">'
#         f'Patient &middot; Treatment &middot; Financial Intelligence</div>'
#         f'</div>'

#         f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:8px;'
#         f'padding:.45rem .9rem;font-family:DM Mono,monospace;font-size:.74rem;color:{C_SEC};">'
#         f'<span class="live-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;'
#         f'background:{C_MINT};margin-right:7px;vertical-align:middle;"></span>'
#         f'Live &middot; {now}</div>'

#         f'</div>',
#         unsafe_allow_html=True
#     )

#     with st.spinner(""):
#         df = load_data()

#     if df is None or len(df) == 0:
#         st.warning("No data found. Run `python main.py` to populate the database.")
#         with st.expander("Getting started"):
#             st.markdown("1. Place CSV files in `data/`\n2. Run `python main.py`\n3. Refresh")
#         return

#     fdf = create_sidebar_filters(df)

#     create_kpi_cards(fdf)

#     # ── Volume & Revenue ──────────────────────────────────────────────────────
#     section_header("Volume &amp; Revenue")
#     c1, c2 = st.columns(2)
#     render_chart(c1, "By Treatment Type",  fig_treatment, fdf)
#     render_chart(c2, "Monthly Trend",      fig_revenue,   fdf)

#     # ── Demographics ──────────────────────────────────────────────────────────
#     section_header("Patient Demographics")
#     c1, c2, c3 = st.columns(3)
#     render_chart(c1, "Gender Split",   fig_gender,  fdf)
#     render_chart(c2, "Age Histogram",  fig_age,     fdf)
#     render_chart(c3, "Payment Status", fig_payment, fdf)

#     # ── Financial ─────────────────────────────────────────────────────────────
#     section_header("Financial Performance")
#     c1, c2 = st.columns(2)
#     render_chart(c1, "Physician Revenue Ranking", fig_doctors,   fdf)
#     render_chart(c2, "Cost Spread by Treatment",  fig_cost_dist, fdf)

#     # ── Insights ──────────────────────────────────────────────────────────────
#     section_header("Key Insights")
#     display_insights(fdf)

#     # ── Data Explorer ─────────────────────────────────────────────────────────
#     section_header("Data Explorer")
#     st.markdown(
#         f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;padding:1.5rem;">',
#         unsafe_allow_html=True
#     )
#     sc1, sc2, sc3 = st.columns([2, 3, 1])
#     with sc1:
#         search_col = st.selectbox("Column", fdf.columns)
#     with sc2:
#         search_term = st.text_input("Search", placeholder=f"Filter by {search_col}…")
#     with sc3:
#         page_size = st.selectbox("Rows / page", [10, 25, 50, 100])

#     ddf = (
#         fdf[fdf[search_col].astype(str).str.contains(search_term, case=False, na=False)]
#         if search_term else fdf
#     )
#     total_pages = max(1, (len(ddf) + page_size - 1) // page_size)
#     page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
#     start = (page_num - 1) * page_size
#     st.dataframe(ddf.iloc[start: start + page_size], use_container_width=True, hide_index=True)
#     st.download_button(
#         "⬇  Export CSV",
#         data=ddf.to_csv(index=False),
#         file_name=f"healthcare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#         mime="text/csv",
#     )
#     st.markdown("</div>", unsafe_allow_html=True)

#     # ── Footer ────────────────────────────────────────────────────────────────
#     st.markdown(
#         f'<div style="display:flex;justify-content:space-between;align-items:center;'
#         f'margin-top:3rem;padding-top:1.5rem;border-top:1px solid {C_BORDER};'
#         f'font-size:.72rem;color:{C_MUTED};letter-spacing:.05em;">'
#         f'<div style="font-family:DM Serif Display,serif;font-size:.9rem;color:{C_SEC};">&#x2B22; Medic Analytics</div>'
#         f'<div>Powered by Streamlit &amp; Plotly &middot; {now}</div>'
#         f'</div>',
#         unsafe_allow_html=True
#     )


# if __name__ == "__main__":
#     main()




import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
from pathlib import Path

# ── Make sure project root is on sys.path so pipeline imports work ─────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.load import query_database, get_db_path

st.set_page_config(
    page_title="Medic · Analytics",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-PIPELINE: run main.py when the database is missing or empty
# ─────────────────────────────────────────────────────────────────────────────

def _db_has_data() -> bool:
    """Return True if the database exists and the main table has at least one row."""
    db_path = get_db_path()
    if not db_path.exists():
        return False
    try:
        df = query_database()
        return df is not None and len(df) > 0
    except Exception:
        return False


def ensure_pipeline_has_run() -> bool:
    """
    If the database is empty, import and run the pipeline directly.
    Returns True when data is ready, False if it still failed after trying.
    """
    if _db_has_data():
        return True

    with st.status("⚙️ First run detected — building database…", expanded=True) as status:
        try:
            st.write("📂 Extracting CSV files…")
            # Import the pipeline modules directly (works on Streamlit Cloud
            # where subprocess calls may be restricted).
            import main as pipeline_main
            pipeline_main.run()          # call a run() function — see note below
            st.write("✅ Pipeline complete.")
            status.update(label="✅ Database ready!", state="complete", expanded=False)
            return _db_has_data()
        except AttributeError:
            # Fallback: if main.py has no run() function, execute it as a module
            try:
                st.write("↩️ Falling back to exec-based pipeline run…")
                main_path = PROJECT_ROOT / "main.py"
                exec(compile(main_path.read_text(), str(main_path), "exec"),  # noqa: S102
                     {"__name__": "__main__", "__file__": str(main_path)})
                status.update(label="✅ Database ready!", state="complete", expanded=False)
                return _db_has_data()
            except Exception as e:
                status.update(label="❌ Pipeline failed", state="error", expanded=True)
                st.error(f"Could not populate the database: {e}")
                st.info(
                    "**Manual fix:** Make sure your `data/` folder contains the CSV files "
                    "and re-deploy, or run `python main.py` locally and push the generated "
                    "`database/healthcare.db` file to your repo."
                )
                return False
        except Exception as e:
            status.update(label="❌ Pipeline failed", state="error", expanded=True)
            st.error(f"Could not populate the database: {e}")
            return False


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING  (cached so it only hits the DB once per session)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame | None:
    try:
        df = query_database()
        return df if df is not None and len(df) > 0 else None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS  (same dark theme as before)
# ─────────────────────────────────────────────────────────────────────────────

C_BG     = "#0a0d12"
C_CARD   = "#111520"
C_SUBTLE = "#161b27"
C_BORDER = "rgba(255,255,255,0.06)"
C_TEXT   = "#edf2f7"
C_SEC    = "#a0aec0"
C_MUTED  = "#4a5568"
C_TEAL   = "#63b3ed"
C_MINT   = "#4fd1c5"
C_AMBER  = "#f6ad55"
C_VIOLET = "#b794f4"
C_ROSE   = "#fc8181"

TEAL_SCALE = [[0, "#1a3a4a"], [0.5, "#2c7a99"], [1, C_TEAL]]
MINT_SCALE = [[0, "#1a4040"], [0.5, "#2c9999"], [1, C_MINT]]

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=C_SEC, size=11),
    title_font=dict(family="DM Serif Display", color=C_TEXT, size=15),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.05)"),
    margin=dict(l=20, r=20, t=52, b=20),
    hoverlabel=dict(bgcolor="#161b27", bordercolor="rgba(255,255,255,0.1)", font=dict(color=C_TEXT)),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=C_BORDER),
)

def apply_layout(fig, **kw):
    fig.update_layout(**{**BASE_LAYOUT, **kw})
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def insight_row(label, value, color=None):
    color = color or C_TEAL
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:.82rem;">'
        f'<span style="color:{C_SEC};">{label}</span>'
        f'<span style="font-family:DM Mono,monospace;font-size:.8rem;color:{color};">{value}</span>'
        f'</div>'
    )

def card(content, extra=""):
    return (
        f'<div style="background:{C_CARD};border:1px solid {C_BORDER};'
        f'border-radius:14px;padding:1.4rem 1.5rem;{extra}">{content}</div>'
    )

def card_header(title, dot_color):
    return (
        f'<div style="font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;'
        f'color:{C_MUTED};margin-bottom:1rem;display:flex;align-items:center;gap:6px;">'
        f'<div style="width:5px;height:5px;border-radius:50%;background:{dot_color};flex-shrink:0;"></div>'
        f'{title}</div>'
    )

def section_header(text):
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin:2rem 0 1rem;">'
        f'<span style="font-family:DM Serif Display,serif;font-size:1.2rem;color:{C_TEXT};">{text}</span>'
        f'<div style="flex:1;height:1px;background:{C_BORDER};"></div></div>',
        unsafe_allow_html=True
    )

def chart_subtitle(text):
    st.markdown(
        f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;'
        f'padding:1.2rem 1.4rem 0.3rem;">'
        f'<div style="font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:{C_MUTED};">'
        f'{text}</div></div>',
        unsafe_allow_html=True
    )

def sidebar_label(text):
    st.markdown(
        f'<div style="font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;'
        f'color:{C_MUTED};padding:.5rem 0 .2rem;">{text}</div>',
        unsafe_allow_html=True
    )

def sidebar_divider():
    st.markdown(
        f'<hr style="border:none;border-top:1px solid {C_BORDER};margin:.6rem 0;">',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────

def create_kpi_cards(df):
    n_patients = df["patient_id"].nunique() if "patient_id" in df.columns else len(df)
    revenue    = df["amount"].sum()  if "amount" in df.columns else 0
    avg_cost   = df["amount"].mean() if "amount" in df.columns else 0
    tc         = df["treatment_type"].value_counts() if "treatment_type" in df.columns else pd.Series()
    top_tx     = str(tc.index[0])[:22] if len(tc) else "—"
    completion = 0.0
    if "status" in df.columns and len(df):
        completion = len(df[df["status"] == "Completed"]) / len(df) * 100

    kpi_data = [
        (C_TEAL,   f"{n_patients:,}",   "Total Patients",     "↑ Active cohort"),
        (C_MINT,   f"${revenue:,.0f}",  "Total Revenue",      "Gross billings"),
        (C_AMBER,  f"${avg_cost:,.0f}", "Avg Treatment Cost", "Per encounter"),
        (C_VIOLET, top_tx,              "Top Treatment",      "By volume"),
    ]
    cols = st.columns(4)
    for col, (color, value, label, delta) in zip(cols, kpi_data):
        with col:
            st.markdown(
                f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:14px;padding:1.4rem 1.5rem;">'
                f'<div style="width:3px;height:36px;border-radius:2px;background:{color};margin-bottom:1rem;"></div>'
                f'<div style="font-family:DM Serif Display,serif;font-size:2rem;line-height:1;margin-bottom:.3rem;color:{C_TEXT};">{value}</div>'
                f'<div style="font-size:.72rem;color:{C_MUTED};letter-spacing:.06em;text-transform:uppercase;">{label}</div>'
                f'<div style="font-family:DM Mono,monospace;font-size:.72rem;margin-top:.6rem;color:{color};">{delta}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    pct = f"{completion:.1f}"
    st.markdown(
        f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:10px;'
        f'padding:1rem 1.5rem;margin:1rem 0 2rem;display:flex;align-items:center;gap:1.2rem;">'
        f'<div style="font-size:.72rem;color:{C_MUTED};letter-spacing:.07em;text-transform:uppercase;white-space:nowrap;min-width:200px;">Appointment Completion</div>'
        f'<div style="flex:1;height:4px;background:{C_SUBTLE};border-radius:2px;overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{C_TEAL},{C_MINT});border-radius:2px;"></div></div>'
        f'<div style="font-family:DM Mono,monospace;font-size:.8rem;color:{C_TEAL};min-width:40px;text-align:right;">{pct}%</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_treatment(df):
    if "treatment_type" not in df.columns:
        return None
    tc = df["treatment_type"].value_counts().head(10).reset_index()
    tc.columns = ["Treatment", "Count"]
    fig = go.Figure(go.Bar(
        x=tc["Treatment"], y=tc["Count"],
        marker=dict(color=tc["Count"], colorscale=TEAL_SCALE, showscale=False),
        text=tc["Count"], textposition="outside", textfont=dict(color=C_SEC, size=10),
    ))
    return apply_layout(fig, title="Treatment Volume", xaxis_tickangle=30, height=360)

def fig_revenue(df):
    if "Month" not in df.columns or "amount" not in df.columns:
        return None
    m = df.groupby("Month")["amount"].sum().reset_index().sort_values("Month")
    fig = go.Figure(go.Scatter(
        x=m["Month"], y=m["amount"], mode="lines+markers",
        line=dict(width=2.5, color=C_TEAL),
        marker=dict(size=7, color=C_MINT, line=dict(color=C_BG, width=2)),
        fill="tozeroy", fillcolor="rgba(99,179,237,0.07)",
    ))
    apply_layout(fig, title="Monthly Revenue Trend", height=360)
    fig.update_yaxes(tickprefix="$")
    return fig

def fig_payment(df):
    PAL = {"Paid": C_MINT, "Pending": C_AMBER, "Failed": C_ROSE}
    if "payment_status" in df.columns:
        sc = df["payment_status"].value_counts()
        colors = [PAL.get(str(s), C_VIOLET) for s in sc.index]
    elif "status" in df.columns:
        sc = df["status"].value_counts()
        colors = [C_MINT, C_TEAL, C_ROSE, C_AMBER][: len(sc)]
    else:
        return None
    fig = go.Figure(go.Pie(
        labels=sc.index, values=sc.values, hole=0.55,
        marker=dict(colors=colors, line=dict(color=C_BG, width=2)),
        textinfo="percent", textfont=dict(size=11),
    ))
    fig.add_annotation(text="Status", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=11, color=C_MUTED))
    return apply_layout(fig, title="Payment Distribution", height=360)

def fig_gender(df):
    if "gender" not in df.columns:
        return None
    gc = df["gender"].value_counts()
    fig = go.Figure(go.Pie(
        labels=gc.index, values=gc.values, hole=0.55,
        marker=dict(colors=[C_TEAL, C_VIOLET, C_MINT], line=dict(color=C_BG, width=2)),
        textinfo="percent", textfont=dict(size=11),
    ))
    fig.add_annotation(text="Gender", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=11, color=C_MUTED))
    return apply_layout(fig, title="Gender Distribution", height=360)

def fig_age(df):
    if "Age" not in df.columns:
        return None
    mu = df["Age"].mean()
    fig = go.Figure(go.Histogram(
        x=df["Age"], nbinsx=22,
        marker=dict(color=C_TEAL, opacity=0.8, line=dict(color=C_BG, width=0.5)),
    ))
    fig.add_vline(x=mu, line_dash="dot", line_color=C_AMBER, line_width=1.5,
                  annotation_text=f"μ {mu:.1f}",
                  annotation_font=dict(color=C_AMBER, size=11))
    return apply_layout(fig, title="Age Distribution", height=360)

def fig_doctors(df):
    if "amount" not in df.columns:
        return None
    dcol = None
    for col in df.columns:
        if "doctor" in col.lower() and ("name" in col.lower() or "first_name" in col.lower()):
            dcol = col; break
    if not dcol and "first_name" in df.columns and "last_name" in df.columns:
        df = df.copy()
        df["_doc"] = df["first_name"] + " " + df["last_name"]
        dcol = "_doc"
    if not dcol:
        return None
    rev = df.groupby(dcol)["amount"].sum().sort_values(ascending=True).tail(10)
    fig = go.Figure(go.Bar(
        y=rev.index, x=rev.values, orientation="h",
        marker=dict(color=rev.values, colorscale=MINT_SCALE, showscale=False),
        text=[f"${v:,.0f}" for v in rev.values],
        textposition="outside", textfont=dict(color=C_SEC, size=10),
    ))
    apply_layout(fig, title="Top 10 Physicians by Revenue", height=400,
                 margin=dict(l=130, r=40, t=52, b=20))
    fig.update_xaxes(tickprefix="$")
    return fig

def fig_cost_dist(df):
    if "treatment_type" not in df.columns or "amount" not in df.columns:
        return None
    top = df["treatment_type"].value_counts().head(8).index
    palette = [C_TEAL, C_MINT, C_VIOLET, C_AMBER, C_ROSE, "#68d391", "#76e4f7", "#fbd38d"]
    fig = go.Figure()
    for i, t in enumerate(top):
        c = palette[i % len(palette)]
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        fig.add_trace(go.Box(
            y=df[df["treatment_type"] == t]["amount"], name=t,
            boxmean="sd", marker_color=c, line_color=c,
            fillcolor=f"rgba({r},{g},{b},0.12)",
        ))
    apply_layout(fig, title="Cost Distribution by Treatment", height=420, showlegend=False)
    fig.update_yaxes(tickprefix="$")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART RENDER HELPER
# ─────────────────────────────────────────────────────────────────────────────

def render_chart(col, subtitle, make_fig, df):
    with col:
        chart_subtitle(subtitle)
        f = make_fig(df)
        if f:
            st.plotly_chart(f, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────

def create_sidebar_filters(df):
    with st.sidebar:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:1.4rem 1.2rem 1rem;">'
            f'<div style="width:36px;height:36px;flex-shrink:0;'
            f'background:linear-gradient(135deg,{C_TEAL},{C_MINT});'
            f'clip-path:polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);"></div>'
            f'<div>'
            f'<div style="font-family:DM Serif Display,serif;font-size:1.2rem;">Medic</div>'
            f'<div style="font-size:.65rem;color:{C_MUTED};letter-spacing:.1em;text-transform:uppercase;">Analytics Platform</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        sidebar_divider()
        fdf = df.copy()

        dcol = next((c for c in ["appointment_date","date","bill_date","treatment_date"] if c in df.columns), None)
        if dcol:
            sidebar_label("Date Range")
            mn = pd.to_datetime(df[dcol]).min()
            mx = pd.to_datetime(df[dcol]).max()
            dr = st.date_input("", [mn, mx], min_value=mn, max_value=mx, label_visibility="collapsed")
            if len(dr) == 2:
                mask = (pd.to_datetime(df[dcol]) >= pd.to_datetime(dr[0])) & \
                       (pd.to_datetime(df[dcol]) <= pd.to_datetime(dr[1]))
                fdf = df[mask]
            sidebar_divider()

        if "treatment_type" in df.columns:
            sidebar_label("Treatment")
            opts = ["All"] + sorted(df["treatment_type"].dropna().unique().tolist())
            sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_treat")
            if sel != "All":
                fdf = fdf[fdf["treatment_type"] == sel]
            sidebar_divider()

        if "status" in df.columns:
            sidebar_label("Appointment Status")
            opts = ["All"] + sorted(df["status"].dropna().unique().tolist())
            sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_status")
            if sel != "All":
                fdf = fdf[fdf["status"] == sel]
            sidebar_divider()

        if "payment_status" in df.columns:
            sidebar_label("Payment Status")
            opts = ["All"] + sorted(df["payment_status"].dropna().unique().tolist())
            sel = st.selectbox("", opts, label_visibility="collapsed", key="sb_pay")
            if sel != "All":
                fdf = fdf[fdf["payment_status"] == sel]
            sidebar_divider()

        if "amount" in df.columns:
            sidebar_label("Cost Range")
            lo, hi = float(df["amount"].min()), float(df["amount"].max())
            rng = st.slider("", lo, hi, (lo, hi), format="$%.0f", label_visibility="collapsed")
            fdf = fdf[(fdf["amount"] >= rng[0]) & (fdf["amount"] <= rng[1])]
            sidebar_divider()

        total_r = fdf["amount"].sum()  if "amount"     in fdf.columns else 0
        pt      = fdf["patient_id"].nunique() if "patient_id" in fdf.columns else "—"
        st.markdown(
            f'<div style="padding:.9rem 1.1rem;background:rgba(99,179,237,0.05);border-radius:10px;'
            f'border:1px solid rgba(99,179,237,0.1);">'
            f'<div style="font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:{C_MUTED};margin-bottom:8px;">Current View</div>'
            f'<div style="font-size:.78rem;line-height:2;">'
            f'Records<span style="color:{C_TEAL};font-family:DM Mono,monospace;float:right;">{len(fdf):,}</span><br>'
            f'Patients<span style="color:{C_TEAL};font-family:DM Mono,monospace;float:right;">{pt}</span><br>'
            f'Revenue<span style="color:{C_MINT};font-family:DM Mono,monospace;float:right;">${total_r:,.0f}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺  Reset Filters", use_container_width=True):
            st.rerun()
    return fdf


# ─────────────────────────────────────────────────────────────────────────────
# INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────

def display_insights(df):
    rev, ptr, trt = [], [], []

    if "amount" in df.columns:
        rev = [
            insight_row("Total Revenue",   f"${df['amount'].sum():,.0f}",    C_TEAL),
            insight_row("Average Cost",    f"${df['amount'].mean():,.0f}",   C_TEAL),
            insight_row("Median Cost",     f"${df['amount'].median():,.0f}", C_TEAL),
            insight_row("Max Single Bill", f"${df['amount'].max():,.0f}",    C_AMBER),
        ]
    if "gender" in df.columns:
        for g, c in df["gender"].value_counts().items():
            ptr.append(insight_row(str(g), f"{c:,}  ({c/len(df)*100:.1f}%)", C_VIOLET))
    if "Age" in df.columns:
        ptr += [
            insight_row("Avg Age",   f"{df['Age'].mean():.1f} yrs",                  C_VIOLET),
            insight_row("Age Range", f"{df['Age'].min():.0f}–{df['Age'].max():.0f}", C_VIOLET),
        ]
    if "treatment_type" in df.columns:
        mode = df["treatment_type"].mode()
        mc = str(mode.iloc[0]) if not mode.empty else "—"
        trt.append(insight_row("Most Common",  mc,                                 C_MINT))
        trt.append(insight_row("Unique Types", str(df["treatment_type"].nunique()), C_MINT))
        if "amount" in df.columns:
            trt.append(insight_row("Top Revenue",
                                   str(df.groupby("treatment_type")["amount"].sum().idxmax()),
                                   C_MINT))

    def _card(dot, title, rows):
        return card(card_header(title, dot) + "".join(rows))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_card(C_TEAL,   "Revenue Insights",   rev), unsafe_allow_html=True)
    with c2:
        st.markdown(_card(C_VIOLET, "Patient Insights",   ptr), unsafe_allow_html=True)
    with c3:
        st.markdown(_card(C_MINT,   "Treatment Insights", trt), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # ── 1. Guarantee data exists before anything renders ─────────────────────
    if not ensure_pipeline_has_run():
        st.stop()   # halt rendering cleanly; error already shown above

    # ── 2. Load data ──────────────────────────────────────────────────────────
    df = load_data()
    if df is None or len(df) == 0:
        st.error("Database is still empty after running the pipeline. "
                 "Check that your CSV files are committed to the repo inside `data/`.")
        st.stop()

    now = datetime.now().strftime("%d %b %Y, %H:%M")

    # ── 3. Page header ────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;align-items:flex-end;justify-content:space-between;'
        f'margin-bottom:2.4rem;padding-bottom:1.4rem;border-bottom:1px solid {C_BORDER};">'
        f'<div>'
        f'<div style="font-family:DM Serif Display,serif;font-size:2.6rem;line-height:1.1;'
        f'letter-spacing:-.02em;background:linear-gradient(120deg,{C_TEXT} 30%,{C_TEAL});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
        f'Healthcare Analytics</div>'
        f'<div style="font-size:.78rem;color:{C_MUTED};letter-spacing:.07em;text-transform:uppercase;margin-top:.3rem;">'
        f'Patient &middot; Treatment &middot; Financial Intelligence</div>'
        f'</div>'
        f'<div style="background:{C_CARD};border:1px solid {C_BORDER};border-radius:8px;'
        f'padding:.45rem .9rem;font-family:DM Mono,monospace;font-size:.74rem;color:{C_SEC};">'
        f'Live &middot; {now}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    fdf = create_sidebar_filters(df)
    create_kpi_cards(fdf)

    section_header("Volume &amp; Revenue")
    c1, c2 = st.columns(2)
    render_chart(c1, "By Treatment Type", fig_treatment, fdf)
    render_chart(c2, "Monthly Trend",     fig_revenue,   fdf)

    section_header("Patient Demographics")
    c1, c2, c3 = st.columns(3)
    render_chart(c1, "Gender Split",   fig_gender,  fdf)
    render_chart(c2, "Age Histogram",  fig_age,     fdf)
    render_chart(c3, "Payment Status", fig_payment, fdf)

    section_header("Financial Performance")
    c1, c2 = st.columns(2)
    render_chart(c1, "Physician Revenue Ranking", fig_doctors,   fdf)
    render_chart(c2, "Cost Spread by Treatment",  fig_cost_dist, fdf)

    section_header("Key Insights")
    display_insights(fdf)

    section_header("Data Explorer")
    sc1, sc2, sc3 = st.columns([2, 3, 1])
    with sc1:
        search_col = st.selectbox("Column", fdf.columns)
    with sc2:
        search_term = st.text_input("Search", placeholder=f"Filter by {search_col}…")
    with sc3:
        page_size = st.selectbox("Rows / page", [10, 25, 50, 100])

    ddf = (
        fdf[fdf[search_col].astype(str).str.contains(search_term, case=False, na=False)]
        if search_term else fdf
    )
    total_pages = max(1, (len(ddf) + page_size - 1) // page_size)
    page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    start = (page_num - 1) * page_size
    st.dataframe(ddf.iloc[start: start + page_size], use_container_width=True, hide_index=True)
    st.download_button(
        "⬇  Export CSV",
        data=ddf.to_csv(index=False),
        file_name=f"healthcare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

    st.markdown(
        f'<div style="display:flex;justify-content:space-between;margin-top:3rem;'
        f'padding-top:1.5rem;border-top:1px solid {C_BORDER};'
        f'font-size:.72rem;color:{C_MUTED};">'
        f'<div style="font-family:DM Serif Display,serif;font-size:.9rem;color:{C_SEC};">&#x2B22; Medic Analytics</div>'
        f'<div>Powered by Streamlit &amp; Plotly &middot; {now}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()