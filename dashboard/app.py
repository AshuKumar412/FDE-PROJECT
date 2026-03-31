# """
# Healthcare Analytics Dashboard - Elegant & Interactive
# With modern design, animations, and rich visualizations
# """
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# from datetime import datetime
# import sys
# import os

# # Add project root to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pipeline.load import query_database

# # ============================================================================
# # PAGE CONFIGURATION
# # ============================================================================
# st.set_page_config(
#     page_title="Healthcare Analytics Dashboard",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================================
# # CUSTOM CSS FOR BEAUTIFUL DESIGN
# # ============================================================================
# st.markdown("""
# <style>
#     /* Import Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     /* Main container styling */
#     .main {
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Animated gradient header */
#     @keyframes gradient {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }
    
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
#         background-size: 200% 200%;
#         animation: gradient 10s ease infinite;
#         padding: 2rem;
#         border-radius: 20px;
#         margin-bottom: 2rem;
#         text-align: center;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.1);
#     }
    
#     .main-header h1 {
#         color: white;
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin: 0;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
    
#     .main-header p {
#         color: rgba(255,255,255,0.9);
#         font-size: 1.1rem;
#         margin-top: 0.5rem;
#     }
    
#     /* KPI Cards with hover effects */
#     @keyframes slideUp {
#         from {
#             opacity: 0;
#             transform: translateY(30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }
    
#     .kpi-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 20px;
#         color: white;
#         text-align: center;
#         margin: 0.5rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         transition: all 0.3s ease;
#         animation: slideUp 0.5s ease-out;
#     }
    
#     .kpi-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 8px 25px rgba(0,0,0,0.15);
#     }
    
#     .kpi-value {
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin: 0.5rem 0;
#     }
    
#     .kpi-label {
#         font-size: 1rem;
#         opacity: 0.9;
#         letter-spacing: 0.5px;
#     }
    
#     .kpi-icon {
#         font-size: 2rem;
#         margin-bottom: 0.5rem;
#     }
    
#     /* Chart containers */
#     .chart-container {
#         background: white;
#         border-radius: 20px;
#         padding: 1rem;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#         transition: all 0.3s ease;
#     }
    
#     .chart-container:hover {
#         box-shadow: 0 5px 20px rgba(0,0,0,0.1);
#     }
    
#     /* Sidebar styling */
#     .css-1d391kg {
#         background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
#     }
    
#     /* Filter section */
#     .filter-section {
#         background: white;
#         border-radius: 15px;
#         padding: 1rem;
#         margin-bottom: 1rem;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#     }
    
#     /* Insights box */
#     .insight-box {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         border-radius: 15px;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         border-left: 4px solid #667eea;
#     }
    
#     /* Metric cards */
#     .metric-card {
#         background: white;
#         border-radius: 15px;
#         padding: 1rem;
#         text-align: center;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#     }
    
#     /* Status badges */
#     .badge-success {
#         background: #28a745;
#         color: white;
#         padding: 0.25rem 0.75rem;
#         border-radius: 20px;
#         font-size: 0.85rem;
#     }
    
#     .badge-warning {
#         background: #ffc107;
#         color: #333;
#         padding: 0.25rem 0.75rem;
#         border-radius: 20px;
#         font-size: 0.85rem;
#     }
    
#     .badge-danger {
#         background: #dc3545;
#         color: white;
#         padding: 0.25rem 0.75rem;
#         border-radius: 20px;
#         font-size: 0.85rem;
#     }
    
#     /* Data table styling */
#     .dataframe {
#         border-radius: 15px;
#         overflow: hidden;
#     }
    
#     /* Loading animation */
#     @keyframes pulse {
#         0% { opacity: 0.6; }
#         50% { opacity: 1; }
#         100% { opacity: 0.6; }
#     }
    
#     .loading {
#         animation: pulse 1.5s ease-in-out infinite;
#     }
    
#     /* Custom scrollbar */
#     ::-webkit-scrollbar {
#         width: 8px;
#         height: 8px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: #f1f1f1;
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: #888;
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: #555;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================================
# # DATA LOADING FUNCTION
# # ============================================================================
# @st.cache_data(ttl=3600)
# def load_data():
#     """Load data from database with caching"""
#     try:
#         df = query_database()
#         if df is None or len(df) == 0:
#             st.warning("No data found. Please run the pipeline first.")
#             return None
#         return df
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return None

# # ============================================================================
# # VISUALIZATION FUNCTIONS
# # ============================================================================
# def create_kpi_metrics(df):
#     """Create animated KPI metrics with icons"""
#     col1, col2, col3, col4 = st.columns(4)
    
#     # Calculate metrics
#     total_patients = df['patient_id'].nunique() if 'patient_id' in df.columns else len(df)
#     total_revenue = df['amount'].sum() if 'amount' in df.columns else 0
#     avg_cost = df['amount'].mean() if 'amount' in df.columns else 0
    
#     # Treatment count
#     treatment_counts = df['treatment_type'].value_counts() if 'treatment_type' in df.columns else pd.Series()
#     most_common = treatment_counts.index[0] if len(treatment_counts) > 0 else "N/A"
    
#     # Appointment completion rate
#     if 'status' in df.columns:
#         completed = len(df[df['status'] == 'Completed'])
#         completion_rate = (completed / len(df)) * 100 if len(df) > 0 else 0
#     else:
#         completion_rate = 0
    
#     with col1:
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-icon">👥</div>
#                 <div class="kpi-value">{total_patients:,}</div>
#                 <div class="kpi-label">Total Patients</div>
#                 <div style="font-size:0.8rem; opacity:0.8;">Active Records</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-icon">💰</div>
#                 <div class="kpi-value">${total_revenue:,.0f}</div>
#                 <div class="kpi-label">Total Revenue</div>
#                 <div style="font-size:0.8rem; opacity:0.8;">Year to Date</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-icon">📊</div>
#                 <div class="kpi-value">${avg_cost:,.0f}</div>
#                 <div class="kpi-label">Average Cost</div>
#                 <div style="font-size:0.8rem; opacity:0.8;">Per Treatment</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-icon">🏆</div>
#                 <div class="kpi-value" style="font-size:1.5rem;">{most_common[:15]}</div>
#                 <div class="kpi-label">Most Common</div>
#                 <div style="font-size:0.8rem; opacity:0.8;">Treatment Type</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     # Show completion rate in a separate row
#     st.markdown(f"""
#         <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
#                     border-radius: 15px; padding: 0.5rem; margin: 0.5rem 0; text-align: center;">
#             <span style="color: white;">✅ Appointment Completion Rate: </span>
#             <strong style="color: white; font-size: 1.2rem;">{completion_rate:.1f}%</strong>
#             <div style="background: rgba(255,255,255,0.2); border-radius: 10px; margin-top: 5px;">
#                 <div style="background: white; width: {completion_rate}%; height: 5px; border-radius: 10px;"></div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# def create_treatment_chart(df):
#     """Create interactive treatment distribution chart"""
#     if 'treatment_type' not in df.columns:
#         return None
    
#     treatment_counts = df['treatment_type'].value_counts().reset_index()
#     treatment_counts.columns = ['Treatment', 'Count']
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Bar(
#         x=treatment_counts['Treatment'],
#         y=treatment_counts['Count'],
#         marker=dict(
#             color=treatment_counts['Count'],
#             colorscale='Viridis',
#             showscale=True,
#             colorbar=dict(title="Count")
#         ),
#         text=treatment_counts['Count'],
#         textposition='outside',
#         hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
#     ))
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Treatment Distribution Analysis</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         xaxis_title="Treatment Type",
#         yaxis_title="Number of Patients",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=450,
#         showlegend=False,
#         hovermode='x unified'
#     )
    
#     return fig

# def create_monthly_revenue_chart(df):
#     """Create animated monthly revenue trend"""
#     if 'Month' not in df.columns or 'amount' not in df.columns:
#         return None
    
#     monthly = df.groupby('Month')['amount'].agg(['sum', 'mean', 'count']).reset_index()
#     monthly = monthly.sort_values('Month')
    
#     fig = make_subplots(specs=[[{"secondary_y": True}]])
    
#     # Revenue line
#     fig.add_trace(
#         go.Scatter(
#             x=monthly['Month'],
#             y=monthly['sum'],
#             name='Total Revenue',
#             mode='lines+markers',
#             line=dict(width=3, color='#667eea'),
#             marker=dict(size=8, color='#764ba2', symbol='circle'),
#             fill='tozeroy',
#             fillcolor='rgba(102, 126, 234, 0.2)',
#             hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
#         ),
#         secondary_y=False
#     )
    
#     # Appointment count
#     fig.add_trace(
#         go.Bar(
#             x=monthly['Month'],
#             y=monthly['count'],
#             name='Appointments',
#             marker=dict(color='rgba(240, 147, 251, 0.6)'),
#             hovertemplate='<b>%{x}</b><br>Appointments: %{y}<extra></extra>'
#         ),
#         secondary_y=True
#     )
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Monthly Revenue & Appointment Trends</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         xaxis_title="Month",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=450,
#         hovermode='x unified',
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1
#         )
#     )
    
#     fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
#     fig.update_yaxes(title_text="Number of Appointments", secondary_y=True)
    
#     return fig

# def create_payment_status_chart(df):
#     """Create donut chart for payment status"""
#     if 'payment_status' not in df.columns:
#         return None
    
#     status_counts = df['payment_status'].value_counts()
    
#     colors = {
#         'Paid': '#28a745',
#         'Pending': '#ffc107',
#         'Failed': '#dc3545'
#     }
    
#     fig = go.Figure(data=[go.Pie(
#         labels=status_counts.index,
#         values=status_counts.values,
#         hole=0.4,
#         marker=dict(colors=[colors.get(s, '#667eea') for s in status_counts.index]),
#         textinfo='label+percent',
#         textposition='outside',
#         hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
#     )])
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Payment Status Distribution</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         height=400,
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=-0.2)
#     )
    
#     return fig

# def create_doctor_performance_chart(df):
#     """Create horizontal bar chart for doctor performance"""
#     if 'amount' not in df.columns:
#         return None
    
#     # Find doctor name column
#     doctor_col = None
#     for col in df.columns:
#         if 'doctor' in col.lower() and ('name' in col.lower() or 'first_name' in col.lower()):
#             doctor_col = col
#             break
    
#     if not doctor_col and 'first_name' in df.columns and 'last_name' in df.columns:
#         df['doctor_name'] = df['first_name'] + ' ' + df['last_name']
#         doctor_col = 'doctor_name'
    
#     if not doctor_col:
#         return None
    
#     doctor_revenue = df.groupby(doctor_col)['amount'].sum().sort_values(ascending=True).tail(10)
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Bar(
#         y=doctor_revenue.index,
#         x=doctor_revenue.values,
#         orientation='h',
#         marker=dict(
#             color=doctor_revenue.values,
#             colorscale='Plasma',
#             colorbar=dict(title="Revenue ($)")
#         ),
#         text=doctor_revenue.values,
#         textposition='outside',
#         hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
#     ))
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Top 10 Doctors by Revenue</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         xaxis_title="Revenue ($)",
#         yaxis_title="Doctor",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=450,
#         margin=dict(l=150)
#     )
    
#     return fig

# def create_gender_chart(df):
#     """Create gender distribution chart"""
#     if 'gender' not in df.columns:
#         return None
    
#     gender_counts = df['gender'].value_counts()
    
#     fig = go.Figure(data=[go.Pie(
#         labels=gender_counts.index,
#         values=gender_counts.values,
#         marker=dict(colors=['#667eea', '#764ba2']),
#         textinfo='label+percent',
#         hole=0.3,
#         hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
#     )])
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Gender Distribution</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         height=400,
#         showlegend=True
#     )
    
#     return fig

# def create_age_chart(df):
#     """Create age distribution histogram"""
#     if 'Age' not in df.columns:
#         return None
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Histogram(
#         x=df['Age'],
#         nbinsx=20,
#         marker=dict(
#             color='#667eea',
#             line=dict(color='white', width=1)
#         ),
#         hovertemplate='Age: %{x}<br>Count: %{y}<extra></extra>'
#     ))
    
#     # Add mean line
#     mean_age = df['Age'].mean()
#     fig.add_vline(x=mean_age, line_dash="dash", line_color="red",
#                   annotation_text=f"Mean: {mean_age:.1f}", annotation_position="top")
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Age Distribution of Patients</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         xaxis_title="Age",
#         yaxis_title="Number of Patients",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=400,
#         bargap=0.05
#     )
    
#     return fig

# def create_appointment_status_chart(df):
#     """Create appointment status chart"""
#     if 'status' not in df.columns:
#         return None
    
#     status_counts = df['status'].value_counts()
    
#     colors = {
#         'Completed': '#28a745',
#         'Scheduled': '#17a2b8',
#         'Cancelled': '#dc3545',
#         'No-show': '#ffc107'
#     }
    
#     fig = go.Figure(data=[go.Bar(
#         x=status_counts.index,
#         y=status_counts.values,
#         marker=dict(color=[colors.get(s, '#667eea') for s in status_counts.index]),
#         text=status_counts.values,
#         textposition='auto',
#         hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
#     )])
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Appointment Status Overview</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         xaxis_title="Status",
#         yaxis_title="Number of Appointments",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=400
#     )
    
#     return fig

# def create_treatment_cost_chart(df):
#     """Create box plot for treatment costs"""
#     if 'treatment_type' not in df.columns or 'amount' not in df.columns:
#         return None
    
#     fig = go.Figure()
    
#     treatments = df['treatment_type'].value_counts().head(8).index
#     for treatment in treatments:
#         treatment_data = df[df['treatment_type'] == treatment]['amount']
#         fig.add_trace(go.Box(
#             y=treatment_data,
#             name=treatment,
#             boxmean='sd',
#             marker_color='#667eea'
#         ))
    
#     fig.update_layout(
#         title=dict(
#             text="<b>Treatment Cost Distribution by Type</b>",
#             x=0.5,
#             font=dict(size=20, color='#333')
#         ),
#         yaxis_title="Cost ($)",
#         xaxis_title="Treatment Type",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=450,
#         showlegend=False
#     )
    
#     return fig

# # ============================================================================
# # SIDEBAR WITH ADVANCED FILTERS
# # ============================================================================
# def create_sidebar_filters(df):
#     """Create interactive sidebar with filters"""
#     with st.sidebar:
#         # Logo and title
#         st.markdown("""
#             <div style="text-align: center; padding: 1rem;">
#                 <div style="font-size: 3rem;">🏥</div>
#                 <h2 style="color: #667eea;">Healthcare Analytics</h2>
#                 <p style="color: #666;">Interactive Dashboard</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         # Date range filter
#         st.markdown("### 📅 Date Range")
#         date_col = None
#         for col in ['appointment_date', 'date', 'created_at', 'bill_date']:
#             if col in df.columns:
#                 date_col = col
#                 break
        
#         if date_col:
#             min_date = pd.to_datetime(df[date_col]).min()
#             max_date = pd.to_datetime(df[date_col]).max()
            
#             date_range = st.date_input(
#                 "Select Date Range",
#                 [min_date, max_date],
#                 min_value=min_date,
#                 max_value=max_date
#             )
            
#             if len(date_range) == 2:
#                 mask = (pd.to_datetime(df[date_col]) >= pd.to_datetime(date_range[0])) & \
#                        (pd.to_datetime(df[date_col]) <= pd.to_datetime(date_range[1]))
#                 filtered_df = df[mask]
#             else:
#                 filtered_df = df
#         else:
#             filtered_df = df
        
#         st.markdown("---")
        
#         # Advanced filters
#         st.markdown("### 🔍 Advanced Filters")
        
#         # Treatment type filter
#         if 'treatment_type' in filtered_df.columns:
#             treatments = ['All'] + sorted(filtered_df['treatment_type'].dropna().unique().tolist())
#             selected_treatment = st.selectbox("💊 Treatment Type", treatments)
#             if selected_treatment != 'All':
#                 filtered_df = filtered_df[filtered_df['treatment_type'] == selected_treatment]
        
#         # Status filter
#         if 'status' in filtered_df.columns:
#             statuses = ['All'] + sorted(filtered_df['status'].dropna().unique().tolist())
#             selected_status = st.selectbox("📌 Appointment Status", statuses)
#             if selected_status != 'All':
#                 filtered_df = filtered_df[filtered_df['status'] == selected_status]
        
#         # Payment status filter
#         if 'payment_status' in filtered_df.columns:
#             payments = ['All'] + sorted(filtered_df['payment_status'].dropna().unique().tolist())
#             selected_payment = st.selectbox("💳 Payment Status", payments)
#             if selected_payment != 'All':
#                 filtered_df = filtered_df[filtered_df['payment_status'] == selected_payment]
        
#         # Doctor filter
#         doctor_col = None
#         for col in filtered_df.columns:
#             if 'doctor' in col.lower() and ('name' in col.lower() or 'first_name' in col.lower()):
#                 doctor_col = col
#                 break
#         if not doctor_col and 'first_name' in filtered_df.columns and 'last_name' in filtered_df.columns:
#             filtered_df['doctor_name'] = filtered_df['first_name'] + ' ' + filtered_df['last_name']
#             doctor_col = 'doctor_name'
        
#         if doctor_col:
#             doctors = ['All'] + sorted(filtered_df[doctor_col].dropna().unique().tolist())
#             selected_doctor = st.selectbox("👨‍⚕️ Doctor", doctors)
#             if selected_doctor != 'All':
#                 filtered_df = filtered_df[filtered_df[doctor_col] == selected_doctor]
        
#         # Cost range filter
#         if 'amount' in filtered_df.columns:
#             st.markdown("### 💰 Cost Range")
#             min_cost = float(filtered_df['amount'].min())
#             max_cost = float(filtered_df['amount'].max())
            
#             cost_range = st.slider(
#                 "Select Cost Range",
#                 min_cost,
#                 max_cost,
#                 (min_cost, max_cost)
#             )
            
#             filtered_df = filtered_df[(filtered_df['amount'] >= cost_range[0]) & 
#                                       (filtered_df['amount'] <= cost_range[1])]
        
#         st.markdown("---")
        
#         # Statistics summary
#         st.markdown("### 📊 Current View")
#         total_patients = filtered_df['patient_id'].nunique() if 'patient_id' in filtered_df.columns else 'N/A'
#         total_revenue = filtered_df['amount'].sum() if 'amount' in filtered_df.columns else 0
#         st.info(f"""
#         **Records:** {len(filtered_df):,}
#         **Patients:** {total_patients}
#         **Revenue:** ${total_revenue:,.2f}
#         """)
        
#         # Reset button
#         if st.button("🔄 Reset All Filters", use_container_width=True):
#             st.rerun()
        
#         return filtered_df

# # ============================================================================
# # INSIGHTS SECTION
# # ============================================================================
# def display_insights(df):
#     """Display key insights in a beautiful format"""
#     st.markdown("### 💡 Key Insights & Analytics")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         # Revenue insights
#         if 'amount' in df.columns:
#             st.markdown("""
#                 <div class="insight-box">
#                     <h4>💰 Revenue Insights</h4>
#                 </div>
#             """, unsafe_allow_html=True)
            
#             total = df['amount'].sum()
#             avg = df['amount'].mean()
#             median = df['amount'].median()
            
#             st.metric("Total Revenue", f"${total:,.2f}")
#             st.metric("Average Transaction", f"${avg:,.2f}")
#             st.metric("Median Transaction", f"${median:,.2f}")
    
#     with col2:
#         # Patient insights
#         st.markdown("""
#             <div class="insight-box">
#                 <h4>👥 Patient Insights</h4>
#             </div>
#         """, unsafe_allow_html=True)
        
#         if 'gender' in df.columns:
#             gender_counts = df['gender'].value_counts()
#             for gender, count in gender_counts.items():
#                 percentage = (count / len(df)) * 100
#                 st.write(f"**{gender}:** {count:,} ({percentage:.1f}%)")
        
#         if 'Age' in df.columns:
#             st.write(f"**Average Age:** {df['Age'].mean():.1f} years")
#             st.write(f"**Age Range:** {df['Age'].min():.0f} - {df['Age'].max():.0f} years")
    
#     with col3:
#         # Treatment insights
#         if 'treatment_type' in df.columns:
#             st.markdown("""
#                 <div class="insight-box">
#                     <h4>💊 Treatment Insights</h4>
#                 </div>
#             """, unsafe_allow_html=True)
            
#             most_common = df['treatment_type'].mode()[0] if len(df['treatment_type'].mode()) > 0 else "N/A"
#             treatment_count = df['treatment_type'].nunique()
            
#             st.write(f"**Most Common:** {most_common}")
#             st.write(f"**Unique Treatments:** {treatment_count}")
            
#             if 'amount' in df.columns:
#                 top_treatment = df.groupby('treatment_type')['amount'].sum().idxmax()
#                 st.write(f"**Highest Revenue:** {top_treatment}")

# # ============================================================================
# # MAIN DASHBOARD
# # ============================================================================
# def main():
#     """Main dashboard function"""
    
#     # Header
#     st.markdown("""
#         <div class="main-header">
#             <h1>🏥 Healthcare Analytics Dashboard</h1>
#             <p>Comprehensive Patient, Treatment & Financial Analytics</p>
#             <p style="font-size: 0.9rem;">Real-time Insights | Interactive Visualizations | Data-Driven Decisions</p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Load data
#     with st.spinner("Loading healthcare data..."):
#         df = load_data()
    
#     if df is None or len(df) == 0:
#         st.warning("⚠️ No data found. Please run the pipeline first: `python main.py`")
        
#         # Instructions
#         with st.expander("📖 How to get started"):
#             st.markdown("""
#                 1. **Place your CSV files** in the `C:\\FED-PROJECT\\Project dataset\\data\\` folder
#                 2. **Run the ETL pipeline:** `python main.py`
#                 3. **Refresh this dashboard**
                
#                 ### Expected files:
#                 - appointments.csv
#                 - billing.csv
#                 - doctors.csv
#                 - patients.csv
#                 - treatments.csv
#             """)
#         return
    
#     # Apply filters
#     filtered_df = create_sidebar_filters(df)
    
#     # KPI Metrics
#     create_kpi_metrics(filtered_df)
    
#     st.markdown("---")
    
#     # Row 1: Treatment Distribution and Monthly Revenue
#     col1, col2 = st.columns(2)
    
#     with col1:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             treatment_fig = create_treatment_chart(filtered_df)
#             if treatment_fig:
#                 st.plotly_chart(treatment_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             revenue_fig = create_monthly_revenue_chart(filtered_df)
#             if revenue_fig:
#                 st.plotly_chart(revenue_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     # Row 2: Payment Status and Doctor Performance
#     col1, col2 = st.columns(2)
    
#     with col1:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             payment_fig = create_payment_status_chart(filtered_df)
#             if payment_fig:
#                 st.plotly_chart(payment_fig, use_container_width=True, config={'displayModeBar': True})
#             else:
#                 appointment_fig = create_appointment_status_chart(filtered_df)
#                 if appointment_fig:
#                     st.plotly_chart(appointment_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             doctor_fig = create_doctor_performance_chart(filtered_df)
#             if doctor_fig:
#                 st.plotly_chart(doctor_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     # Row 3: Age Distribution and Gender
#     col1, col2 = st.columns(2)
    
#     with col1:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             age_fig = create_age_chart(filtered_df)
#             if age_fig:
#                 st.plotly_chart(age_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         with st.container():
#             st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#             gender_fig = create_gender_chart(filtered_df)
#             if gender_fig:
#                 st.plotly_chart(gender_fig, use_container_width=True, config={'displayModeBar': True})
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     # Row 4: Treatment Cost Distribution
#     with st.container():
#         st.markdown('<div class="chart-container">', unsafe_allow_html=True)
#         cost_fig = create_treatment_cost_chart(filtered_df)
#         if cost_fig:
#             st.plotly_chart(cost_fig, use_container_width=True, config={'displayModeBar': True})
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Insights Section
#     st.markdown("---")
#     display_insights(filtered_df)
    
#     # Data Table Section
#     st.markdown("---")
#     st.markdown("### 📋 Detailed Data View")
    
#     # Search
#     if len(filtered_df.columns) > 0:
#         search_col = st.selectbox("Search in column:", filtered_df.columns)
#         search_term = st.text_input(f"🔍 Search in {search_col}:", placeholder="Type to search...")
        
#         if search_term:
#             mask = filtered_df[search_col].astype(str).str.contains(search_term, case=False, na=False)
#             display_df = filtered_df[mask]
#             st.info(f"Found {len(display_df)} matching records")
#         else:
#             display_df = filtered_df
        
#         # Show dataframe with pagination
#         page_size = st.selectbox("Rows per page:", [10, 25, 50, 100])
#         page_number = st.number_input("Page", min_value=1, value=1)
        
#         start_idx = (page_number - 1) * page_size
#         end_idx = start_idx + page_size
        
#         st.dataframe(
#             display_df.iloc[start_idx:end_idx],
#             use_container_width=True,
#             height=400
#         )
        
#         # Download button
#         csv = display_df.to_csv(index=False)
#         st.download_button(
#             label="📥 Download Data as CSV",
#             data=csv,
#             file_name=f"healthcare_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
    
#     # Footer
#     st.markdown("---")
#     st.markdown("""
#         <div style="text-align: center; padding: 2rem; color: #666;">
#             <p>🏥 Healthcare Analytics Dashboard | Powered by Streamlit & Plotly</p>
#             <p style="font-size: 0.8rem;">Data-driven insights for better healthcare decisions</p>
#         </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

















"""
Healthcare Analytics Dashboard - Complete Working Code
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.load import query_database

# Page configuration
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 600;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .kpi-icon {
        font-size: 1.5rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
    }
    .sidebar-header h3 {
        margin: 0.5rem 0;
    }
    
    /* Insights box */
    .insight-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Progress bar */
    .progress-container {
        background: rgba(102,126,234,0.2);
        border-radius: 10px;
        padding: 0.2rem;
        margin: 0.5rem 0;
    }
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        padding: 0.3rem;
        text-align: center;
        color: white;
        font-size: 0.8rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #666;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Info message */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    """Load data from database with caching"""
    try:
        df = query_database()
        if df is None or len(df) == 0:
            return None
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_kpi_cards(df):
    """Create KPI metric cards"""
    # Calculate metrics
    total_patients = df['patient_id'].nunique() if 'patient_id' in df.columns else len(df)
    total_revenue = df['amount'].sum() if 'amount' in df.columns else 0
    avg_cost = df['amount'].mean() if 'amount' in df.columns else 0
    
    # Treatment count
    treatment_counts = df['treatment_type'].value_counts() if 'treatment_type' in df.columns else pd.Series()
    most_common = treatment_counts.index[0] if len(treatment_counts) > 0 else "N/A"
    
    # Completion rate
    if 'status' in df.columns:
        completed = len(df[df['status'] == 'Completed'])
        completion_rate = (completed / len(df)) * 100 if len(df) > 0 else 0
    else:
        completion_rate = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-value">{total_patients:,}</div>
                <div class="kpi-label">Total Patients</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-value">${total_revenue:,.0f}</div>
                <div class="kpi-label">Total Revenue</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📊</div>
                <div class="kpi-value">${avg_cost:,.0f}</div>
                <div class="kpi-label">Average Cost</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🏆</div>
                <div class="kpi-value" style="font-size:1.2rem">{most_common[:20]}</div>
                <div class="kpi-label">Most Common</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Completion rate progress bar
    st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {completion_rate}%">
                Appointment Completion: {completion_rate:.1f}%
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_treatment_chart(df):
    """Create treatment distribution chart"""
    if 'treatment_type' not in df.columns:
        return None
    
    treatment_counts = df['treatment_type'].value_counts().head(10).reset_index()
    treatment_counts.columns = ['Treatment', 'Count']
    
    fig = go.Figure(data=[go.Bar(
        x=treatment_counts['Treatment'],
        y=treatment_counts['Count'],
        marker=dict(
            color=treatment_counts['Count'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Count")
        ),
        text=treatment_counts['Count'],
        textposition='outside'
    )])
    
    fig.update_layout(
        title="Treatment Distribution",
        xaxis_title="Treatment Type",
        yaxis_title="Number of Patients",
        height=400,
        showlegend=False,
        xaxis_tickangle=45
    )
    
    return fig

def create_monthly_revenue_chart(df):
    """Create monthly revenue chart"""
    if 'Month' not in df.columns or 'amount' not in df.columns:
        return None
    
    monthly = df.groupby('Month')['amount'].sum().reset_index()
    monthly = monthly.sort_values('Month')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly['Month'],
        y=monthly['amount'],
        mode='lines+markers',
        name='Revenue',
        line=dict(width=3, color='#667eea'),
        marker=dict(size=8, color='#764ba2'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        height=400
    )
    
    return fig

def create_payment_chart(df):
    """Create payment status chart"""
    if 'payment_status' in df.columns:
        status_counts = df['payment_status'].value_counts()
        
        colors = {
            'Paid': '#28a745',
            'Pending': '#ffc107',
            'Failed': '#dc3545'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.3,
            marker=dict(colors=[colors.get(s, '#667eea') for s in status_counts.index]),
            textinfo='label+percent'
        )])
        
        fig.update_layout(title="Payment Status Distribution", height=400)
        return fig
    elif 'status' in df.columns:
        status_counts = df['status'].value_counts()
        
        fig = go.Figure(data=[go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker=dict(color=['#28a745', '#17a2b8', '#dc3545', '#ffc107']),
            text=status_counts.values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Appointment Status",
            xaxis_title="Status",
            yaxis_title="Count",
            height=400
        )
        return fig
    
    return None

def create_gender_chart(df):
    """Create gender distribution chart"""
    if 'gender' not in df.columns:
        return None
    
    gender_counts = df['gender'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=gender_counts.index,
        values=gender_counts.values,
        hole=0.3,
        marker=dict(colors=['#667eea', '#764ba2']),
        textinfo='label+percent'
    )])
    
    fig.update_layout(title="Gender Distribution", height=400)
    return fig

def create_age_chart(df):
    """Create age distribution chart"""
    if 'Age' not in df.columns:
        return None
    
    fig = go.Figure(data=[go.Histogram(
        x=df['Age'],
        nbinsx=20,
        marker=dict(color='#667eea', line=dict(color='white', width=1))
    )])
    
    mean_age = df['Age'].mean()
    fig.add_vline(
        x=mean_age,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_age:.1f}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Age Distribution of Patients",
        xaxis_title="Age (Years)",
        yaxis_title="Number of Patients",
        height=400
    )
    
    return fig

def create_doctor_chart(df):
    """Create doctor performance chart"""
    if 'amount' not in df.columns:
        return None
    
    # Find doctor name column
    doctor_col = None
    for col in df.columns:
        if 'doctor' in col.lower() and ('name' in col.lower() or 'first_name' in col.lower()):
            doctor_col = col
            break
    
    if not doctor_col and 'first_name' in df.columns and 'last_name' in df.columns:
        df['doctor_name'] = df['first_name'] + ' ' + df['last_name']
        doctor_col = 'doctor_name'
    
    if not doctor_col:
        return None
    
    doctor_revenue = df.groupby(doctor_col)['amount'].sum().sort_values(ascending=True).tail(10)
    
    fig = go.Figure(data=[go.Bar(
        y=doctor_revenue.index,
        x=doctor_revenue.values,
        orientation='h',
        marker=dict(color=doctor_revenue.values, colorscale='Plasma'),
        text=doctor_revenue.values,
        textposition='outside'
    )])
    
    fig.update_layout(
        title="Top 10 Doctors by Revenue",
        xaxis_title="Revenue ($)",
        yaxis_title="Doctor",
        height=450,
        margin=dict(l=120)
    )
    
    return fig

def create_cost_chart(df):
    """Create treatment cost distribution chart"""
    if 'treatment_type' not in df.columns or 'amount' not in df.columns:
        return None
    
    top_treatments = df['treatment_type'].value_counts().head(8).index
    
    fig = go.Figure()
    for treatment in top_treatments:
        treatment_data = df[df['treatment_type'] == treatment]['amount']
        fig.add_trace(go.Box(
            y=treatment_data,
            name=treatment,
            boxmean='sd',
            marker_color='#667eea'
        ))
    
    fig.update_layout(
        title="Treatment Cost Distribution by Type",
        yaxis_title="Cost ($)",
        xaxis_title="Treatment Type",
        height=450,
        showlegend=False,
        xaxis_tickangle=45
    )
    
    return fig

def create_sidebar_filters(df):
    """Create sidebar filters"""
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <h3>🏥 Healthcare Analytics</h3>
                <p>Interactive Dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        filtered_df = df.copy()
        
        # Date filter
        date_col = None
        for col in ['appointment_date', 'date', 'bill_date', 'treatment_date']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            st.markdown("### 📅 Date Range")
            min_date = pd.to_datetime(df[date_col]).min()
            max_date = pd.to_datetime(df[date_col]).max()
            
            date_range = st.date_input(
                "Select Range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                mask = (pd.to_datetime(df[date_col]) >= pd.to_datetime(date_range[0])) & \
                       (pd.to_datetime(df[date_col]) <= pd.to_datetime(date_range[1]))
                filtered_df = df[mask]
            
            st.markdown("---")
        
        # Treatment filter
        if 'treatment_type' in df.columns:
            st.markdown("### 💊 Treatment Type")
            treatments = ['All'] + sorted(df['treatment_type'].dropna().unique().tolist())
            selected = st.selectbox("Select Treatment", treatments)
            if selected != 'All':
                filtered_df = filtered_df[filtered_df['treatment_type'] == selected]
            st.markdown("---")
        
        # Status filter
        if 'status' in df.columns:
            st.markdown("### 📌 Appointment Status")
            statuses = ['All'] + sorted(df['status'].dropna().unique().tolist())
            selected = st.selectbox("Select Status", statuses)
            if selected != 'All':
                filtered_df = filtered_df[filtered_df['status'] == selected]
            st.markdown("---")
        
        # Payment filter
        if 'payment_status' in df.columns:
            st.markdown("### 💳 Payment Status")
            payments = ['All'] + sorted(df['payment_status'].dropna().unique().tolist())
            selected = st.selectbox("Select Payment Status", payments)
            if selected != 'All':
                filtered_df = filtered_df[filtered_df['payment_status'] == selected]
            st.markdown("---")
        
        # Cost filter
        if 'amount' in df.columns:
            st.markdown("### 💰 Cost Range")
            min_cost = float(df['amount'].min())
            max_cost = float(df['amount'].max())
            
            cost_range = st.slider(
                "Select Range ($)",
                min_cost,
                max_cost,
                (min_cost, max_cost),
                format="$%.0f"
            )
            
            filtered_df = filtered_df[(filtered_df['amount'] >= cost_range[0]) & 
                                      (filtered_df['amount'] <= cost_range[1])]
            st.markdown("---")
        
        # Statistics summary
        st.markdown("### 📊 Current View")
        total_records = len(filtered_df)
        total_patients = filtered_df['patient_id'].nunique() if 'patient_id' in filtered_df.columns else 'N/A'
        total_revenue = filtered_df['amount'].sum() if 'amount' in filtered_df.columns else 0
        
        st.info(f"""
        **Records:** {total_records:,}
        **Patients:** {total_patients}
        **Revenue:** ${total_revenue:,.2f}
        """)
        
        # Reset button
        if st.button("🔄 Reset All Filters", use_container_width=True):
            st.rerun()
        
        return filtered_df

def display_insights(df):
    """Display key insights"""
    st.markdown("### 💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'amount' in df.columns:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("**💰 Revenue Insights**")
            st.metric("Total Revenue", f"${df['amount'].sum():,.2f}")
            st.metric("Average Cost", f"${df['amount'].mean():,.2f}")
            st.metric("Median Cost", f"${df['amount'].median():,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**👥 Patient Insights**")
        
        if 'gender' in df.columns:
            for gender, count in df['gender'].value_counts().items():
                pct = (count / len(df)) * 100
                st.write(f"{gender}: {count:,} ({pct:.1f}%)")
        
        if 'Age' in df.columns:
            st.write(f"**Avg Age:** {df['Age'].mean():.1f} years")
            st.write(f"**Age Range:** {df['Age'].min():.0f} - {df['Age'].max():.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if 'treatment_type' in df.columns:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("**💊 Treatment Insights**")
            
            most_common = df['treatment_type'].mode()[0] if len(df['treatment_type'].mode()) > 0 else "N/A"
            st.write(f"**Most Common:** {most_common}")
            st.write(f"**Unique Treatments:** {df['treatment_type'].nunique()}")
            
            if 'amount' in df.columns:
                top_revenue = df.groupby('treatment_type')['amount'].sum().idxmax()
                st.write(f"**Top Revenue:** {top_revenue}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏥 Healthcare Analytics Dashboard</h1>
            <p>Comprehensive Patient, Treatment & Financial Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df is None or len(df) == 0:
        st.warning("⚠️ No data found. Please run the pipeline first: `python main.py`")
        
        with st.expander("📖 How to get started"):
            st.markdown("""
                1. Place your CSV files in the `data/` folder
                2. Run: `python main.py`
                3. Refresh this dashboard
            """)
        return
    
    # Apply filters
    filtered_df = create_sidebar_filters(df)
    
    # KPI Cards
    create_kpi_cards(filtered_df)
    
    st.markdown("---")
    
    # Row 1: Treatment and Revenue Charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            treatment_fig = create_treatment_chart(filtered_df)
            if treatment_fig:
                st.plotly_chart(treatment_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            revenue_fig = create_monthly_revenue_chart(filtered_df)
            if revenue_fig:
                st.plotly_chart(revenue_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Payment and Gender Charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            payment_fig = create_payment_chart(filtered_df)
            if payment_fig:
                st.plotly_chart(payment_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            gender_fig = create_gender_chart(filtered_df)
            if gender_fig:
                st.plotly_chart(gender_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Age and Doctor Charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            age_fig = create_age_chart(filtered_df)
            if age_fig:
                st.plotly_chart(age_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            doctor_fig = create_doctor_chart(filtered_df)
            if doctor_fig:
                st.plotly_chart(doctor_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 4: Cost Distribution Chart
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        cost_fig = create_cost_chart(filtered_df)
        if cost_fig:
            st.plotly_chart(cost_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights Section
    st.markdown("---")
    display_insights(filtered_df)
    
    # Data Table Section
    st.markdown("---")
    st.markdown("### 📋 Data Preview")
    
    # Search functionality
    search_col = st.selectbox("Search column:", filtered_df.columns)
    search_term = st.text_input(f"Search in {search_col}:", placeholder="Type to search...")
    
    if search_term:
        mask = filtered_df[search_col].astype(str).str.contains(search_term, case=False, na=False)
        display_df = filtered_df[mask]
        st.success(f"Found {len(display_df)} records")
    else:
        display_df = filtered_df
    
    # Pagination
    page_size = st.selectbox("Rows per page:", [10, 25, 50, 100])
    total_pages = max(1, (len(display_df) + page_size - 1) // page_size)
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(display_df.iloc[start_idx:end_idx], use_container_width=True)
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"healthcare_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>🏥 Healthcare Analytics Dashboard | Powered by Streamlit & Plotly</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

