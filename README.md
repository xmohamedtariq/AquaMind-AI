# AquaMind AI

**AI-powered predictive water network intelligence for early leak-risk detection, anomaly monitoring, and smarter utility operations.**

AquaMind AI is a functional browser-based prototype that demonstrates how pressure and flow signals can be transformed into operational intelligence for water utilities. The current version uses **synthetic hydraulic data** to simulate normal operation, pressure surge, and potential leak conditions.

> Current stage: prototype demonstration. Next milestone: validation with real utility data and a bounded field pilot.

---

## Live Demo

Add your Streamlit link here after deployment:

```text
https://YOUR-APP-NAME.streamlit.app
```

## Project Repository

```text
https://github.com/YOUR-USERNAME/AquaMind-AI
```

---

## What AquaMind AI Demonstrates

- Real-time style dashboard for pressure and flow monitoring
- Synthetic water-network scenarios: normal operation, simulated leak, pressure surge
- Zone-level anomaly signaling
- Leak-risk prioritization
- Operator-focused recommendations
- A clear Sense -> Analyze -> Act workflow

---

## Prototype Screenshot

![AquaMind AI Dashboard Preview](assets/dashboard-preview.png)

---

## Why It Matters

Water networks often collect sensor data, but operational decisions may still arrive late. AquaMind AI aims to act as a predictive intelligence layer on top of existing pressure and flow monitoring, helping operators identify abnormal patterns earlier and respond with clearer actions.

---

## How It Works

1. **Sense** - reads pressure and flow patterns from a water-network zone.
2. **Analyze** - detects abnormal hydraulic behavior using a prototype anomaly logic.
3. **Act** - translates the insight into a risk level and recommended operator action.

---

## Run Locally

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Deployment on Streamlit Community Cloud

1. Create a public GitHub repository named `AquaMind-AI`.
2. Upload `app.py`, `requirements.txt`, `README.md`, `.gitignore`, and the `assets/` folder.
3. Go to Streamlit Community Cloud.
4. Create a new app from this repository.
5. Set the main file path to `app.py`.
6. Choose a clear URL such as `aquamind-ai.streamlit.app` if available.

---

## Transparency Notice

This prototype currently uses synthetic data. It does **not** claim field-validated accuracy, commercial deployment, or real utility performance yet. The next milestone is a real-world pilot with utility data to measure detection precision, false alarms, lead time, localization error, and operator response usefulness.

---

## Founder

**Mohammed Tariq Al-Saqqaf**  
Founder & Lead Innovator - AquaMind AI  
Mechatronics engineering, sensing, control systems, and AI prototype execution.

---

## License

For evaluation, pitch review, and prototype demonstration purposes.
