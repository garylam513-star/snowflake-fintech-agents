import streamlit as st
import pandas as pd
import time
from snowflake.snowpark.context import get_active_session

# App landing layer parameters
st.set_page_config(page_title="Snowflake-Fintech-Agents", layout="wide")
st.title("💳 Snowflake-Fintech-Agents: Credit Card Fault Ingestion Platform")

if 'analysis_reports' not in st.session_state:
    st.session_state.analysis_reports = []
if 'full_data_cache' not in st.session_state:
    st.session_state.full_data_cache = None

st.header("1. Upload Stream Payload to Cloud Engine")
uploaded_file = st.file_uploader("Drag and drop your 'mock_credit_card_transactions.csv' file here", type=["csv"])

if uploaded_file is not None:
    # Read raw dataframe payload from memory stream buffer
    df = pd.read_csv(uploaded_file)
    st.session_state.full_data_cache = df
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Batch Records Assessed", f"{len(df):,}")
    m2.metric("Total Asset Velocity", f"\${df['AMOUNT'].sum():,.2f}")
    m3.metric("Simulated Anomalies", f"{df['IS_FRAUD'].sum()}")
    
    st.dataframe(df.head(5), use_container_width=True)
    st.header("2. Initialize Multi-Agent Cloud Runtime")
    
    if st.button("🏃 Run Pipeline & Sync to Snowflake"):
        # 🤖 Agent Alpha: Risk Heuristics Layer
        with st.status("🕵️ [Agent Alpha: Risk Detector] Active...", expanded=True) as status:
            st.write("Scanning cloud memory payload for anomalous transaction clusters...")
            time.sleep(1)
            flagged_faults = df[(df['AMOUNT'] > 1500) | (df['IS_FRAUD'] == 1)].copy()
            st.dataframe(flagged_faults[['TRANSACTION_ID', 'HOLDER_NAME', 'MERCHANT_NAME', 'AMOUNT']], use_container_width=True)
            status.update(label="🕵️ Agent Alpha: Screening Complete. Anomaly vectors passed to Agent Beta.", state="complete")
        
        # 🤖 Agent Beta: AI Cognitive Analyst Enrichment Layer
        st.subheader("🔍 Agent Beta: AI Cognitive Analyst Reports")
        st.session_state.analysis_reports = []
        
        for index, row in flagged_faults.head(3).iterrows():
            with st.chat_message("assistant", avatar="🔍"):
                risk_score = 95 if row['AMOUNT'] > 2000 else 78
                report_text = f"**CRITICAL THREAT EVALUATION:** Account holder `{row['HOLDER_NAME']}` processed a **\${row['AMOUNT']}** charge at *'{row['MERCHANT_NAME']}'*. Threat deviation rating calculated at **{risk_score}/100**."
                st.write(report_text)
                st.session_state.analysis_reports.append({
                    "TX_ID": row['TRANSACTION_ID'], "Holder": row['HOLDER_NAME'],
                    "Merchant": row['MERCHANT_NAME'], "Amount": row['AMOUNT'],
                    "Risk Score": risk_score, "Disposition": "REJECT & FREEZE" if risk_score > 90 else "FLAG FOR REVIEW",
                    "Card Type": row['CARD_TYPE'], "Currency": row['CURRENCY']
                })
        
        # 💾 Secure Cloud Native Upload
        with st.spinner("💾 Committing streaming log array directly to Snowflake Cloud Ledger..."):
            try:
                session = get_active_session()
                df.columns = [col.upper() for col in df.columns]
                snowpark_df = session.create_dataframe(df)
                snowpark_df.write.mode("append").save_as_table("FINTECH_APP_DB.PUBLIC.CREDIT_CARD_TRANSACTIONS")
                st.success(f"🎉 Cloud Sync complete! Data appended securely to table `CREDIT_CARD_TRANSACTIONS`.")
            except Exception as e:
                st.error(f"Snowflake Cloud Storage Error: {e}")

# =====================================================================
# 📊 UPGRADED THREAT ASSESSMENT EXECUTIVE MATRIX
# =====================================================================
if st.session_state.analysis_reports and st.session_state.full_data_cache is not None:
    st.markdown("---")
    st.header("📊 Threat Assessment Executive Matrix")
    
    # 1. Transform session states to structured metrics
    report_df = pd.DataFrame(st.session_state.analysis_reports)
    full_df = st.session_state.full_data_cache
    
    # 2. Executive Global Security KPI Banner Row
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Faults Isolated", len(report_df), delta="Requires Review", delta_color="inverse")
    kpi2.metric("Max Single Breach Attempt", f"\${report_df['Amount'].max():,.2f}")
    kpi3.metric("Avg Fraud Ticket Cost", f"\${report_df[report_df['Risk Score'] > 90]['Amount'].mean():,.2f}")
    
    # 3. Analytics Chart Layout Split Grid (Top Row)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("⚖️ Agent Beta Disposition Strategy")
        # Visual breakdown of security responses (Reject & Freeze vs Flag for Review)
        st.bar_chart(report_df['Disposition'].value_counts(), color="#FF4B4B", use_container_width=True)
        
    with chart_col2:
        st.subheader("💳 Risk Exposure by Card Network")
        # Aggregated financial loss volumes based on specific card brand networks
        card_distribution = report_df.groupby('Card Type')['Amount'].sum()
        st.bar_chart(card_distribution, color="#29B5E8", use_container_width=True)

    # 4. Analytics Chart Layout Split Grid (Bottom Row)
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.subheader("💱 Global Ingestion Volumes by Currency Type")
        # Evaluates currency processing volume across the entire 500-record batch
        currency_distribution = full_df.groupby('CURRENCY')['AMOUNT'].sum()
        st.area_chart(currency_distribution, color="#00D4B2", use_container_width=True)
        
    with chart_col4:
        st.subheader("📈 High-Risk Transaction Value Variance")
        # Distributes the exact financial ranges of anomalies being caught by the agents
        st.line_chart(report_df.set_index('TX_ID')['Amount'], color="#FF9F1C", use_container_width=True)

    # 5. Master Incident Logs Data Table Row
    st.subheader("📋 Centralized Threat Mitigation Ledger")
    st.dataframe(
        report_df[['TX_ID', 'Holder', 'Merchant', 'Amount', 'Card Type', 'Currency', 'Risk Score', 'Disposition']], 
        use_container_width=True, 
        hide_index=True
    )
