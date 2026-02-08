# Esports Oracle Made for Gemini 3 Hackathon

A multimodal AI scouting agent for Dota 2 that provides deep strategic insights by combining visual recognition, real-time data, and patch-aware reasoning. **Designed for professional analytics, not gambling.**

---

## Key Features

* **Vision Analysis:** Recognizes all 10 heroes from a live draft screenshot.
* **Hard Data:** Fetches real-time team stats (win rates, GPM, duration) via OpenDota API.
* **Meta-Intelligence:** Reads latest patch notes to identify nerfed or buffed heroes.

---

## Installation

1. **Clone the repo:**
```bash
git clone https://github.com/yourusername/esports-oracle.git
cd esports-oracle
```
2. **Install dependencies:**
```bash
pip install -r requirements.txt
```
3. **Set up Environment:**
Create a `.env` file and add your key:
```text
GEMINI_API_KEY=your_actual_key_here

```
4. **Run the App:**
```bash
streamlit run app.py
```



---

## Project Structure

* `app.py`: Streamlit frontend interface.
* `src/gemini_agent.py`: Multimodal agent logic and prompt engineering.
* `src/dota_client.py`: OpenDota API integration and data pre-processing.
* `data/patch_notes.txt`: Knowledge base for current game meta.

---

