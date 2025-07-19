# Automated Book Publication Workflow

This project automates the process of fetching text from a URL or image, rewriting it using an AI-based system, and refining it through human input with version tracking and feedback integration.

 **Web Scraping & Screenshots**
- **Image OCR**
- **AI Chapter Spinning**
- **Human-in-the-Loop Editing**
- **Version Control & Search**
- **Feedback System**


### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pustak_ai.git
cd pustak_ai

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

pip install -r requirements.txt

 Install Tesseract OCR
Download from official site

Add it to your system's PATH after installation.

streamlit run streamlit_app.py
