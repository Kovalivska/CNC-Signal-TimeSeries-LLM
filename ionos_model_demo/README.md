# IONOS CNC Model Demo — Demonstration der LLM-Analysefähigkeiten

**Live-Demo:** [Zur Anwendung](https://placeholder-deployment-url.com) *(Link wird nach Deployment aktualisiert)*

> **Prototype-Status:** Diese Anwendung demonstriert die Ergebnisse verschiedener Prompt-Engineering-Ansätze für CNC-Datenanalyse mit IONOS LLM-Modellen. Sie ist Teil des Hauptprojekts zur industriellen Signalverarbeitung und Zeitreihenanalyse.

Diese Streamlit-Anwendung zeigt die 9 Testfragen aus dem Hauptprojekt und demonstriert, wie verschiedene Prompt-Strategien die Qualität der LLM-Antworten beeinflussen.

## 📸 Übersicht

![IONOS CNC Model Demo](Screenshot%20at%20Oct%2004%2010-15-44.png)
*IONOS CNC Model Demo - Hauptbenutzeroberfläche mit 5 Prompt-Ansätzen und interaktiver Testumgebung*

### 📋 **Demonstration der 9 Testfragen**
- **Q1:** Gesamtanzahl Datensätze im CNC Dataset
- **Q2:** Häufigkeit des meistverwendeten Programms
- **Q3:** Prozentanteil des Hauptprogramms
- **Q4:** Anzahl Datensätze im AUTOMATIC-Modus
- **Q5:** Prozentanteil AUTOMATIC-Modus
- **Q6:** Anzahl Datensätze im MANUAL-Modus
- **Q7:** Verhältnis AUTOMATIC zu MANUAL
- **Q8:** Anzahl Datensätze mit ACTIVE-Status
- **Q9:** Prozentanteil ACTIVE-Status

### **5 Prompt-Engineering-Ansätze**

#### 1️⃣ **Basic-Ansatz**
- **Beschreibung:** Nur die reine Frage ohne zusätzlichen Kontext
- **Zweck:** Baseline-Messung der "rohen" LLM-Leistung
- **Erwartete Genauigkeit:** Niedrig (10-30%)

#### 2️⃣ **Expert-Ansatz (CNC-Techniker)**
- **Beschreibung:** LLM erhält Rolle als CNC-Techniker mit Basiswissen
- **Kontext:** Grundlegende Datenstruktur und einfache Analyselogik
- **Erwartete Genauigkeit:** Mittel (40-60%)

#### 3️⃣ **Enhanced-Ansatz (Fertigungsingenieur)**
- **Beschreibung:** LLM als erfahrener Ingenieur mit detailliertem Fachwissen
- **Kontext:** Industrielle Verteilungsmuster, Pareto-Prinzip, statistische Richtwerte
- **Erwartete Genauigkeit:** Hoch (70-85%)

#### 4️⃣ **Systematic-Ansatz (Senior-Datenarchitekt)**
- **Beschreibung:** Sehr strenge, algorithmische Anweisungen zur Problemlösung
- **Kontext:** Präzise Berechnungsschritte, Ausgabeformate, Qualitätskontrolle
- **Erwartete Genauigkeit:** Sehr hoch (80-95%)

#### 5️⃣ **ML-Ansatz (Machine Learning)**
- **Beschreibung:** Simulation eines Lernprozesses mit Trainingsbeispielen
- **Kontext:** 20+ fiktive aber realistische Beispieldatensätze für In-Context Learning
- **Erwartete Genauigkeit:** Hoch (65-80%, abhängig von Generalisierungsfähigkeit)

## Features der Demo-Anwendung

### **Einzelne Frage testen**
- Wählen Sie eine der 9 Fragen aus
- Testen Sie mit dem gewählten Prompt-Ansatz
- Erhalten Sie sofortige Ergebnisse mit Genauigkeitsbewertung

### **Alle Fragen durchlaufen**
- Vollständiger Test aller 9 Fragen mit einem Ansatz
- Übersichtstabelle mit allen Antworten und Bewertungen
- Durchschnittliche Genauigkeit für den gewählten Ansatz

### **Vergleichsanalyse**
- Vergleich aller 5 Prompt-Ansätze gleichzeitig
- Interaktive Visualisierungen:
  - Balkendiagramm: Durchschnittliche Genauigkeit pro Ansatz
  - Heatmap: Detaillierte Genauigkeit pro Frage und Ansatz
- Identifikation des besten Ansatzes

## Technische Details

### **Datengrundlage**
- **Dateiname:** `cnc_daten.csv`
- **Pfad:** `/data_and_eda/cnc_daten.csv`
- **Automatische Ground Truth Berechnung:** Die korrekten Antworten werden direkt aus den Rohdaten berechnet

### **Simulierte LLM-Antworten**
Da dies eine Demo-Anwendung ist, werden die LLM-Antworten basierend auf realen Testergebnissen simuliert:
- **Basic:** Ungenaue Schätzungen (±20-50% Abweichung)
- **Expert:** Verbesserte Schätzungen (±5-15% Abweichung)  
- **Enhanced:** Hochpräzise Antworten (±1-5% Abweichung)
- **Systematic:** Nahezu exakte Antworten (±0.1-2% Abweichung)
- **ML:** Variable Qualität je nach Muster-Erkennung

### **Genauigkeitsbewertung**
Binäres Bewertungssystem basierend auf strikten Toleranzen:
- **Ganzzahlen:** ±1 Toleranz
- **Prozentsätze:** ±0.5% Toleranz  
- **Verhältnisse:** ±0.01 Toleranz
- **Entweder korrekt (100%) oder falsch (0%)**

## Schnellstart

### Voraussetzungen
- Python 3.9+
- Streamlit 1.28+
- Pandas, Plotly, NumPy

### Installation & Start
```bash
# In das Demo-Verzeichnis wechseln
cd ionos_model_demo

# Abhängigkeiten installieren
pip install -r requirements.txt

# Demo-Anwendung starten
streamlit run app.py
```

Die Anwendung öffnet sich unter `http://localhost:8501`

### Arbeitsablauf
1. **Prompt-Ansatz wählen:** Seitenleiste verwenden
2. **Einzelne Frage testen:** Tab "Einzelne Frage"
3. **Vollständiger Test:** Tab "Alle Fragen" 
4. **Vergleichsanalyse:** Tab "Vergleichsanalyse"

## Erwartete Ergebnisse

Basierend auf realen Tests mit IONOS Meta-Llama-3.1-8B-Instruct:

| Ansatz | Durchschnittliche Genauigkeit | Beste Fragen |
|--------|-------------------------------|--------------|
| **Basic** | ~25% | Einfache Zählungen |
| **Expert** | ~55% | Prozentberechnungen |
| **Enhanced** | ~75% | Komplexe Verhältnisse |
| **Systematic** | ~85% | Alle Fragetypen |
| **ML** | ~70% | Musterbasierte Fragen |

## Verbindung zum Hauptprojekt

Diese Demo ist Teil des größeren **Industrial Signal Processing & Time Series Analysis** Projekts:

### **Verwandte Komponenten:**
- **Hauptanalyse:** `/streamlit_machine_analytics_extended-8/` - Vollständige CNC-Analytics-Anwendung
- **Forschung:** `/research_and_project_scope/` - Technische Dokumentation
- **Modell-Tests:** `/srs/IOINOS_models/` - Vollständige LLM-Validierung
- **Ergebnisse:** `/results/IONOS_models/` - Detaillierte Testergebnisse

### **Prompt-Engineering-Erkenntnisse:**
1. **Kontext ist entscheidend:** Basic-Ansatz versagt bei präzisen Datenanalysen
2. **Fachwissen injizieren:** Enhanced-Ansatz mit Industriekenntnissen sehr effektiv
3. **Strukturierte Anweisungen:** Systematic-Ansatz bietet höchste Konsistenz
4. **In-Context Learning:** ML-Ansatz zeigt Potenzial, benötigt aber qualitativ hochwertige Beispiele

## Projektkontext

**Ziel:** Evaluation verschiedener Prompt-Engineering-Strategien für industrielle Datenanalyse mit Large Language Models (LLMs).

**Methodik:** Systematischer Vergleich von 5 Ansätzen über 9 standardisierte Testfragen zur Bewertung von:
- Numerischer Genauigkeit
- Semantischem Verständnis  
- Reasoning-Qualität
- Extraktions-Zuverlässigkeit

**Erkenntnisse:** Enhanced- und Systematic-Ansätze zeigen deutlich bessere Leistung bei CNC-Datenanalysen als einfache Prompt-Strategien.

---

**Entwickelt für:** Industrielle Signalverarbeitung und Zeitreihenanalyse  
**Technologie-Stack:** Python, Streamlit, Plotly, Pandas  
**Demo-Status:** Funktionsfähiger Prototyp mit simulierten LLM-Antworten  
**Letzte Aktualisierung:** Oktober 2025
