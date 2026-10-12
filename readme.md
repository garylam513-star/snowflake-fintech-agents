# 💳 snowflake-fintech-agents: Credit Card Fault Ingestion Platform

An enterprise-grade, cloud-native Fintech application built on top of the **Snowflake Data Cloud** using **Python 3.10** and **Streamlit in Snowflake (SiS)**. This platform simulates a real-time high-velocity credit card transactional feed, ingesting records safely while leveraging a **Multi-Agent Architecture** to autonomously screen, analyze, flag, and log systemic faults and fraudulent activities directly within the cloud ledger data stream.

---

## 🏗️ System Architecture & Framework Design

The application divides workflows into distinct data engineering, predictive detection, and narrative analytic layers. Instead of utilizing traditional rigid ETL workflows, data lands inside a secure Snowflake cluster while background agents orchestrate operations on top of the streaming frames.

```text
       [ Local Virtual Data Feed ] ─── (500 Row Streaming CSV Payload)
                     │
                     ▼
  ┌─────────────────────────────────────────────────────────────┐
  │      Snowflake-Fintech-Agents Ingestion Platform (UI)       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │             FINTECH_APP_DB (Snowflake Data Cloud)           │
  └──────┬───────────────────────────────────────────────┬──────┘
         │                                               │
         ▼                                               ▼
┌─────────────────────────────────┐             ┌─────────────────────────────────┐
│ 🕵️ Agent Alpha: Risk Detector    │             │ 🔍 Agent Beta: AI Analyst       │
│ (Low-latency heuristic scanning)│ ── Handoff ─► (Cognitive context assessment)    │
└─────────────────────────────────┘             └────────────────┬────────────────┘
                                                                 │
                                                                 ▼
                                                ┌─────────────────────────────────┐
                                                │ 📊 Threat Executive Matrix      │
                                                │ (KPI Banners, Multi-Axis Charts)│
                                                └─────────────────────────────────┘
```

### 🤖 Multi-Agent Role Breakdown

1. **🕵️ Agent Alpha (The Risk Detector)**
   * **Role:** High-throughput processing and low-latency anomaly screening.
   * **Task:** Automatically evaluates incoming data payloads. It scans for transactional velocity spikes, out-of-bounds charges (e.g., ticket amounts performing above standard deviation parameters like `AMOUNT > $1500`), or explicit telemetry exception signals (`IS_FRAUD = 1`). Isolates risky rows instantly and feeds them to the investigation tier.
   
2. **🔍 Agent Beta (The AI Cognitive Analyst)**
   * **Role:** Contextual enrichment, risk evaluation, and reasoning execution.
   * **Task:** Receives the anomalies isolated by Agent Alpha. It runs risk evaluation rules, scores the transaction danger levels on a scale from `0` to `100`, assigns an operational security disposition (`REJECT & FREEZE` or `FLAG FOR REVIEW`), and generates an automated threat summary report explaining the risk vectors.

---

## 📂 Repository Workspace Structure

The project directory is structured cleanly to separate offline asset engines from cloud schema definitions and application logic:

```text
snowflake-fintech-agents/
├── data/
│   └── mock_credit_card_transactions.csv  # 500-Row synthetic transaction stream data
├── sql/
│   └── setup.sql                          # Database context and table ledger schema
├── app.py                                 # Main Streamlit Cloud Dashboard Source Code
├── generate_data.py                       # Python Fake-Data stream generation runtime
└── requirements.txt                       # Python dependency constraints manifest
```

---

## 💻 Technical Implementation Details

### 1. Database Configuration (`sql/setup.sql`)
```sql
CREATE OR REPLACE DATABASE FINTECH_APP_DB;
CREATE OR REPLACE WAREHOUSE FINTECH_WH WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;

USE DATABASE FINTECH_APP_DB;
USE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE CREDIT_CARD_TRANSACTIONS (
    TRANSACTION_ID NUMBER,
    TIMESTAMP TIMESTAMP_NTZ,
    CARD_NUMBER STRING,
    CARD_TYPE STRING,
    HOLDER_NAME STRING,
    MERCHANT_NAME STRING,
    MERCHANT_CATEGORY STRING,
    AMOUNT NUMBER(10, 2),
    CURRENCY STRING,
    IS_FRAUD NUMBER(1, 0)
);
```

### 2. Stream Generation Engine (`generate_data.py`)
Creates highly authentic personal identity data and normal spending profiles, interspersed with luxury expenditure spikes and fraud vectors across a localized 500-row tracking frame.
```python
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_credit_card_data(num_rows=500, filename="data/mock_credit_card_transactions.csv"):
    card_types = ["Visa", "Mastercard", "AMEX", "Discover"]
    currencies = ["USD", "EUR", "GBP", "CAD"]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "TRANSACTION_ID", "TIMESTAMP", "CARD_NUMBER", "CARD_TYPE", 
            "HOLDER_NAME", "MERCHANT_NAME", "MERCHANT_CATEGORY", 
            "AMOUNT", "CURRENCY", "IS_FRAUD"
        ])
        
        start_time = datetime.now() - timedelta(hours=24)
        for i in range(num_rows):
            tx_id = 1000000000 + i
            tx_time = start_time + timedelta(seconds=i * random.randint(10, 60))
            
            is_fraud = 1 if random.random() < 0.03 else 0
            amount = round(random.uniform(1500.00, 5000.00), 2) if is_fraud else round(random.uniform(5.50, 150.00), 2)
            
            writer.writerow([
                tx_id, tx_time.strftime("%Y-%m-%d %H:%M:%S"), fake.credit_card_number(),
                random.choice(card_types), fake.name(), 
                fake.company() + " " + random.choice(["Store", "Inc", "LLC"]),
                random.choice(["Retail", "Groceries", "Entertainment", "Travel", "Gas"]),
                amount, random.choice(currencies), is_fraud
            ])
            
    print(f"📊 Success! Generated {num_rows} transactions in '{filename}'.")

if __name__ == "__main__":
    generate_credit_card_data(num_rows=500)
```

---

## 📊 Dashboard Visualizations & Execution Breakdown

When the `mock_credit_card_transactions.csv` data stream lands on the cloud control panel interface, it generates a comprehensive diagnostic workspace:

### 1. Ingestion Control Metrics Banner
* **Batch Records Assessed:** Displays exactly `500` processed inputs dynamically.
* **Total Asset Velocity:** Real-time aggregated financial processing values across the file.
* **Simulated Anomalies:** Total raw counter of basic threat profiles found.

### 2. Multi-Agent Logs Output Panel
* Shows a step-by-step progress timeline of **Agent Alpha** isolating anomalies.
* Renders **Agent Beta** summary markdown cards displaying reasoning insights, risk assessments, and remediation strategies inside chatbot message logs.

### 3. Threat Assessment Executive Matrix
* **Executive Security KPIs:** Tracking panels displaying Total Faults Isolated, Max Single Breach Attempt Value, and Average Fraud Ticket Costs.
* **Agent Beta Disposition Strategy:** Vertical bar chart breaking down enforcement allocations (`REJECT & FREEZE` vs `FLAG FOR REVIEW`).
* **Risk Exposure by Card Network:** Horizontally mapped distribution charts showing financial exposure risk cross-referenced with Visa, Mastercard, AMEX, or Discover profiles.
* **Global Ingestion Volumes by Currency Type:** Fluid area chart mapping payment currencies processed in the current data batch.
* **High-Risk Value Variance:** Precise line trend chart tracking extreme transaction variances.
* **Centralized Threat Mitigation Ledger:** A management data frame tracking transaction IDs, vendor labels, exact pricing data, and risk classifications.

---

## 🚀 Quick-Start Execution Guide

Follow these sequential steps on your local **Ubuntu environment** to establish database frameworks and run the analytics interface:

### 1. Install Workspace Dependencies Localy
```bash
# Clone and enter the repository folder
cd snowflake-fintech-agents/

# Install the Python package libraries explicitly
python3 -m pip install -r requirements.txt
```

### 2. Populate the Mock Streaming Pipeline Data
```bash
# Execute the data generator script to populate your 500 rows
python3 generate_data.py
```

### 3. Initialize Cloud Data Schemes
* Connect to your Snowflake Web UI (Snowsight).
* Spin up a new **SQL Worksheet** and execute the entire queries block written in `sql/setup.sql`.

### 4. Create and Initialize the Cloud Streamlit Workspace
1. In Snowflake, click on **Projects** ➔ **Streamlit** on the left menu sidebar.
2. Click **+ Streamlit**, assign `Snowflake-Fintech-Agents` as the App Title, select `FINTECH_WH` as the warehouse engine, and point the path to `FINTECH_APP_DB.PUBLIC`.
3. Clear the boilerplate screen contents completely and paste your local **`app.py`** script source file.
4. Open the **Packages** configuration dropdown bar at the top of the app interface editor, search for **`pandas`**, and add it to your active dependencies.
5. Click **Run** in the upper-right menu.
6. Drag and drop your local `data/mock_credit_card_transactions.csv` dataset right into the upload landing card, and hit **Run Pipeline & Sync to Snowflake**!
