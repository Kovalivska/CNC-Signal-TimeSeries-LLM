#!/usr/bin/env python3
"""
IONOS Model Demo - Project Structure Overview
"""

PROJECT_STRUCTURE = """
ionos_model_demo/
├── app.py                 # Hauptanwendung - Streamlit Demo
├── requirements.txt       # Python-Abhängigkeiten
├── README.md             # Vollständige Projektdokumentation (Deutsch)
├── start_demo.sh         # Einfacher Starter (./start_demo.sh)
└── project_overview.py   # Diese Übersichtsdatei

ZWECK:
Demonstration der 9 Testfragen aus dem Hauptprojekt mit 5 verschiedenen
Prompt-Engineering-Ansätzen für IONOS LLM-Modelle.

FEATURES:
✅ 9 CNC-Datenanalyse Testfragen
✅ 5 Prompt-Ansätze (Basic, Expert, Enhanced, Systematic, ML)
✅ Interaktive Streamlit-Oberfläche
✅ Einzelne Frage testen
✅ Alle Fragen durchlaufen
✅ Vergleichsanalyse mit Visualisierungen
✅ Simulierte LLM-Antworten basierend auf realen Testergebnissen
✅ Automatische Ground Truth Berechnung aus CNC-Daten

DATENQUELLE:
/data_and_eda/cnc_daten.csv (6.107 Datensätze, automatisch geladen)

SCHNELLSTART:
1. cd ionos_model_demo
2. pip install -r requirements.txt
3. ./start_demo.sh
4. Browser öffnet http://localhost:8501
"""

QUESTION_MAPPING = {
    "q1_total_records": "Gesamtanzahl Datensätze im CNC Dataset",
    "q2_top_program_count": "Häufigkeit des meistverwendeten Programms",
    "q3_top_program_percentage": "Prozentanteil des Hauptprogramms",
    "q4_automatic_count": "Anzahl Datensätze im AUTOMATIC-Modus",
    "q5_automatic_percentage": "Prozentanteil AUTOMATIC-Modus",
    "q6_manual_count": "Anzahl Datensätze im MANUAL-Modus",
    "q7_auto_manual_ratio": "Verhältnis AUTOMATIC zu MANUAL",
    "q8_active_count": "Anzahl Datensätze mit ACTIVE-Status",
    "q9_active_percentage": "Prozentanteil ACTIVE-Status"
}

PROMPT_APPROACHES = {
    "basic": "Nur die reine Frage ohne Kontext",
    "expert": "CNC-Techniker mit Basiswissen",
    "enhanced": "Fertigungsingenieur mit Fachwissen",
    "systematic": "Senior-Datenarchitekt mit strikten Anweisungen", 
    "ml": "Machine Learning mit Trainingsbeispielen"
}

if __name__ == "__main__":
    print("🤖 IONOS CNC Model Demo - Projektübersicht")
    print("=" * 50)
    print(PROJECT_STRUCTURE)
    print("\n📋 Die 9 Testfragen:")
    for q_id, description in QUESTION_MAPPING.items():
        print(f"  {q_id}: {description}")
    
    print("\n🧠 Die 5 Prompt-Ansätze:")
    for approach, description in PROMPT_APPROACHES.items():
        print(f"  {approach}: {description}")
    
    print("\n🚀 Zum Starten: ./start_demo.sh")
    print("📖 Vollständige Dokumentation: README.md")
