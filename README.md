# AquaMind AI

**AI-powered predictive water network intelligence for early leak-risk detection, anomaly monitoring, and smarter utility operations.**

AquaMind AI is a browser-based prototype designed to demonstrate how pressure and flow data can be transformed into actionable operational intelligence for water utilities.

The current prototype uses **synthetic hydraulic data** to demonstrate the complete workflow from sensing and monitoring to anomaly detection, leak-risk assessment, and operator recommendations.

> **Current Stage:** Functional prototype / Pre-pilot  
> **Data:** Synthetic hydraulic data  
> **Next Milestone:** Validation using real utility data and a controlled field pilot

---

## Project Links

### Live Prototype

[Open AquaMind AI Live Demo](https://aquamindai.streamlit.app/)

### GitHub Repository

[Open AquaMind AI Repository](https://github.com/xmohamedtariq/AquaMind-AI)

### Run Locally

After starting the application with:

```bash
python -m streamlit run app.py

---

## The Problem

Water utilities can experience hidden leaks and abnormal hydraulic behavior before failures become visible.

Conventional monitoring systems often provide raw measurements or threshold-based alerts, while operators need earlier and more actionable information.

AquaMind AI explores how pressure and flow signals can support:

- Early anomaly detection
- Leak-risk prioritization
- Zone-level monitoring
- Faster operator response
- Predictive water network management

---

## The AquaMind AI Approach

The prototype follows a simple operational workflow:

### 1. Sense

Collect or receive water-network measurements such as:

- Pressure
- Flow rate
- Zone information
- Time-series hydraulic behavior

### 2. Analyze

Process the signals to identify:

- Abnormal pressure patterns
- Unexpected flow behavior
- Potential leak-risk conditions
- Network anomalies

### 3. Act

Provide operators with:

- Risk indicators
- Affected-zone information
- Operational alerts
- Recommended response actions

---

## Current Prototype

The current AquaMind AI dashboard is implemented as an interactive **Streamlit** application.

It demonstrates:

- Multi-zone water network monitoring
- Pressure and flow visualization
- Simulated leak scenarios
- Pressure surge scenarios
- Leak-risk indicators
- Anomaly alerts
- Operator recommendations
- Historical signal visualization

The prototype currently uses **synthetic data** and should not be interpreted as a field-validated commercial deployment.

---

## Technology Stack

| Component | Technology |
|---|---|
| Application | Python |
| User Interface | Streamlit |
| Data Processing | Pandas |
| Numerical Processing | NumPy |
| Visualization | Plotly |
| Current Data Source | Synthetic hydraulic data |

---

## Run AquaMind AI Locally

### 1. Clone the repository

```bash
git clone https://github.com/xmohamedtariq/AquaMind-AI.git
