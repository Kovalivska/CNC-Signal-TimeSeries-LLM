#  Research & Project Scope

**Phase 2: Forschungsplanung und Projektdefinition**

Dieser Ordner dokumentiert die **zweite Phase** des Industrial Signal Processing & Time Series Analysis Projekts: die strategische Planung, Forschungsmethodik und Definition des Projektumfangs bas
###  Erkenntnisse zur Technologie-Wahl:
1. **Ollama** optimal für:
   - Batch-Analysen mit sensitiven Daten
   - Offline-Betrieb
   - Volle Datenkontrolle

2. **Cloud-APIs** optimal für:
   - Interaktive Explorationen
   - Schnellere Response-Zeiten
   - State-of-the-Art Performance

###  Fokus des Projekts:
1. **Prompt Engineering** - Optimierung von Analyse-Prompts
2. **LLM-Vergleich** - Ollama vs. Cloud-APIs für Produktionsdaten
3. **Nicht-algorithmischer Ansatz** - Analyse ohne traditionelle ML-Algorithmen
4. **Praktikabilitätsbewertung** - Grenzen und Möglichkeiten dokumentierenErkenntnissen aus der explorativen Datenanalyse (Phase 1).

---



##  Projektdokumente

### 01-scope.md
**Projektumfang und Zielsetzung**
- Definierte Projektziele und Grenzen
- Stakeholder-Anforderungen
- Erfolgs- und Abbruchkriterien
- Projektrahmen und Constraints

### 02-technical-research-analysis.md
**Technische Forschungsanalyse**
- State-of-the-Art Technologien evaluiert
- Wissenschaftliche Literaturrecherche
- Methodische Ansätze für CNC-Datenanalyse
- Technologie-Stack Entscheidungen

### 03-decisions.md
**Strategische Entscheidungen**
- Architekturentscheidungen dokumentiert
- Tool- und Framework-Auswahl begründet
- Trade-offs und Kompromisse erklärt
- Risikobewertung und Mitigation

### 04-tasks.md
**Aufgabenplanung und Roadmap**
- Detaillierte Aufgabenliste
- Zeitplanung und Meilensteine
- Ressourcenzuweisung
- Abhängigkeiten und kritische Pfade

---

##  Wissenschaftliche Grundlagen

### DeepSQA-2021.pdf
**Deep Learning für Time Series Quality Assessment**
- Methoden für Zeitreihen-Qualitätsbewertung
- Deep Learning Architekturen
- Anwendung auf Industriedaten

### LLMs for Time Serie-2024.pdf
**Large Language Models für Zeitreihenanalyse**
- Aktuelle Forschung zu LLMs in Time Series
- Prompt Engineering Techniken
- Praktische Anwendungsfälle

---

**Status:**  Phase 2 abgeschlossen - Projekt an Auftraggeber übergeben  
**Vorherige Phase:** 📂 [`/data_and_eda/`](../data_and_eda/) (Abgeschlossen)  
**Nächste Phase:** 📂 [`/srs/`](../srs/) (Abgeschlossen)

---

*Von Forschungsfragen zu praktischen Lösungen - Projekt erfolgreich abgeschlossen! *jektplanung**, um:
1.  Forschungsziele und -fragen zu definieren
2.  Methodische Ansätze für Datenanalyse zu entwickeln
3.  Machine Learning Architekturen zu konzipieren
4.  Projektumfang und Roadmap festzulegen
5.  Technologie-Stack und Tools zu evaluieren

**Vorherige Phase:** [`/data_and_eda/`](../data_and_eda/) - Explorative Datenanalyse  
**Nächste Phase:** [`/srs/`](../srs/) - Schrittweise Implementierung und Experimentierung

---

## 📁 Ordnerstruktur

```
research_and_project_scope/
│
├── README.md                                # Diese Datei - Projektdokumentation
│
├── 📋 PROJEKTDEFINITION
│   ├── 01-scope.md                         # Projektumfang und Zielsetzung
│   ├── 02-technical-research-analysis.md   # Technische Forschungsanalyse
│   ├── 03-decisions.md                     # Strategische Entscheidungen
│   └── 04-tasks.md                         # Aufgabenplanung und Roadmap
│
└──  WISSENSCHAFTLICHE LITERATUR
    ├── DeepSQA-2021.pdf                    # Deep Learning für Time Series
    └── LLMs for Time Serie-2024.pdf        # LLMs für Zeitreihenanalyse
```

---

## 🔬 Hauptforschungsziel

**Zentrale Forschungsfrage:** Kann ein **nicht-algorithmischer Prompt-Engineering-Ansatz** mit LLMs (Large Language Models) zur effektiven Analyse von CNC-Produktionsdaten eingesetzt werden?

**Innovative Methodik:**
-  Nutzung von Natural Language Prompts statt traditioneller Algorithmen
-  Vergleich lokaler (Ollama) vs. Cloud-basierter (IONOS/OpenAI) LLM-Modelle
-  Iterative Prompt-Optimierung für verschiedene Analyse-Tasks
-  Evaluation der Praktikabilität für reale Produktionsumgebungen

**Untersuchte Anwendungsfälle:**
1. **Datenverständnis** - Explorative Analyse durch Prompts
2. **Mustererkennung** - Pattern Discovery ohne explizite Algorithmen
3. **Berichtsgenerierung** - Automatische Insights aus Rohdaten
4. **Anomalie-Identifikation** - Erkennung ungewöhnlicher Betriebszustände

---

##  Technologie-Evaluierung

### Ansatz 1: **Lokale LLM-Modelle (Ollama)**

**Vorteile:**
-  Datenschutz - Keine Daten verlassen lokale Infrastruktur
-  Keine API-Kosten
-  Offline-Verfügbarkeit
-  Volle Kontrolle über Modelle

**Herausforderungen:**
-  Höhere Hardware-Anforderungen (GPU)
-  Langsamere Inferenz-Geschwindigkeit
-  Begrenzte Modellauswahl

**Use Cases:**
-  Sensitive Produktionsdaten
-  Batch-Verarbeitung großer Datenmengen
-  Domänenspezifische Fine-Tuning Modelle

---

### Ansatz 2: **Cloud-basierte APIs (OpenAI, IONOS)**

**Vorteile:**
-  State-of-the-Art Modellleistung
-  Schnelle Inferenz
-  Keine lokale Hardware-Investition
-  Regelmäßige Modell-Updates

**Herausforderungen:**
-  Laufende API-Kosten
-  Datenschutz-Überlegungen
-  Internet-Abhängigkeit
-  Rate Limits

**Use Cases:**
-  Natural Language Interfaces
-  Automatische Berichtsgenerierung
-  Conversational AI für Anlagensteuerung

---

##  Datenmodellierungs-Strategie

### Phase 2.1: Feature Engineering

**Ziel:** Aussagekräftige Features aus Rohdaten extrahieren

**Geplante Features:**
1. **Zeitbasierte Features**
   - Stunde, Tag, Woche, Monat
   - Schicht-Zuordnung (Tag/Nacht)
   - Arbeitstag vs. Wochenende

2. **Aggregierte Features**
   - Rolling Mean/Std (verschiedene Fenstergrößen)
   - Zykluszeit-Variabilität
   - Programmwechsel-Häufigkeit

3. **Status-Übergangs-Features**
   - Anzahl Status-Wechsel pro Stunde
   - Dauer in jedem Status
   - Sequentielle Muster

4. **Lag Features**
   - Vorherige Zykluszeiten
   - Historische Rüstzeiten
   - Zeitverzögerte Sensormessungen

---

### Phase 2.2: Modell-Architektur

**Baseline-Modelle:**
-  Linear Regression (Benchmark)
-  Random Forest (Feature Importance)
-  XGBoost (High Performance)

**Fortgeschrittene Modelle:**
-  LSTM/GRU (Sequence Learning)
-  Transformer-basierte Modelle
-  Ensemble Methods

**Evaluation-Metriken:**
-  MAE, RMSE für Regression
-  Precision, Recall für Klassifikation
-  F1-Score, AUC-ROC
-  Inference Time (Real-Time Anforderungen)

---

##  Projektumfang

### In-Scope (Phase 2 + 3):
-  Entwicklung von Prototyp-Modellen
-  Evaluierung verschiedener Ansätze
-  Dokumentation der Methodik
-  Proof-of-Concept Implementierungen
-  Vergleich lokaler vs. Cloud-basierter Lösungen

### Out-of-Scope (Zukünftige Phasen):
-  Produktions-Deployment
-  Integration in bestehende MES-Systeme
-  Echtzeit-Streaming-Pipeline (nur Konzept)
-  Multi-Maschinen-Orchestrierung

---

## 📈 Implementierungs-Roadmap

### Meilenstein 1: Forschungsplanung ✅ (Abgeschlossen)
-  Forschungsfragen definiert (01-scope.md)
-  Methodische Ansätze dokumentiert (02-technical-research-analysis.md)
-  Technologie-Stack evaluiert
-  Strategische Entscheidungen getroffen (03-decisions.md)
-  Aufgaben und Roadmap definiert (04-tasks.md)

### Meilenstein 2: Experimentelle Entwicklung ✅ (Abgeschlossen → `/srs/`)
-  Prompt Engineering für verschiedene Use Cases
-  Vergleich Ollama vs. OpenAI/IONOS APIs
-  Entwicklung von Analyse-Notebooks
-  Iterative Verfeinerung der Ansätze
-  Alle Experimente dokumentiert

### Meilenstein 3: Praktikabilitäts-Bewertung ✅ (Abgeschlossen)
-  Grenzen des Prompt-Engineering-Ansatzes identifiziert
-  Vor- und Nachteile dokumentiert
-  Best Practices für Produktionsdaten-Analyse
-  Empfehlungen für zukünftige Anwendungen

### Meilenstein 4: Projektabschluss ✅ (Abgeschlossen)
-  End-to-End Pipeline entwickelt
-  Interactive Dashboard erstellt
-  Vollständige Dokumentation
-  Projekt an Auftraggeber übergeben

---

##  Verbindung zu anderen Phasen

###  Input aus Phase 1 (`/data_and_eda/`)
-  Datenstruktur und -qualität verstanden
-  Geschäftslogik für CNC-Maschinen definiert
-  Einschränkungen identifiziert (z.B. fehlende Sensoren)
- 💡Handlungsempfehlungen für Erweiterungen

### Output für Phase 3 (`/srs/`)
-  Klar definierte Forschungsfragen
-  Technologie-Entscheidungen getroffen
-  Use Cases priorisiert
-  Evaluation-Kriterien festgelegt

---

##  Wichtige Erkenntnisse aus dieser Phase

###  Strategische Entscheidungen:
1. **Hybrid-Ansatz:** Kombination aus lokalen Ollama-Modellen und Cloud-APIs
2. **Iterative Entwicklung:** Schrittweise Experimente in Phase 3 (`/srs/`)
3. **Fokus auf Praxistauglichkeit:** Reale Geschäftsprobleme lösen
4. **Dokumentation:** Jeder Schritt wird nachvollziehbar dokumentiert

### 💡 Erkenntnisse zur Technologie-Wahl:
1. **Ollama** optimal für:
   - Batch-Analysen mit sensitiven Daten
   - Offline-Betrieb
   - Domänenspezifisches Fine-Tuning

2. **Cloud-APIs** optimal für:
   - Interaktive Explorationen
   - Natural Language Interfaces
   - State-of-the-Art Performance

###  Priorisierte Use Cases:
1. **High Priority:** Anomaly Detection (schneller ROI)
2. **Medium Priority:** Predictive Maintenance (benötigt mehr Daten)
3. **Long-term:** Time Series Forecasting (komplex, hoher Nutzen)

---

##  Nächste Schritte → Phase 3

Die Planungen aus dieser Phase werden in der nächsten Phase umgesetzt:

** `/srs/` (Step-by-Step Research & Solutions)**
-  Experimentelle Notebooks für jeden Use Case
-  Prompt Engineering für verschiedene Analysen
-  Vergleichsstudien: Ollama vs. IONOS/OpenAI
-  Iterative Verfeinerung der Ansätze
-  Dokumentation aller Experimente und Learnings

**Experimentelle Bereiche:**
1. **Prompt Engineering**
   - Optimale Prompts für Datenanalyse
   - Few-Shot Learning Beispiele
   - Chain-of-Thought Reasoning
   - Iterative Prompt-Verfeinerung

2. **LLM-Vergleiche**
   - Lokale Llama/Mistral Modelle (Ollama)
   - OpenAI GPT-3.5/4
   - IONOS AI APIs
   - Leistungs- und Kostenanalyse

3. **Analyse-Workflows**
   - Daten-Preprocessing mit Prompts
   - Explorative Datenanalyse
   - Pattern Discovery
   - Ergebnis-Visualisierung

---

##  Technische Anforderungen

### Hardware (für lokale Entwicklung):
- **CPU:** ≥8 Kerne empfohlen
- **RAM:** ≥16GB (32GB empfohlen für LLMs)
- **GPU:** NVIDIA GPU mit ≥8GB VRAM (für Ollama)
- **Speicher:** ≥100GB freier Speicherplatz

### Software-Stack:
```python
# Core Libraries
python>=3.9
jupyter>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Deep Learning
torch>=2.0.0              # PyTorch
tensorflow>=2.13.0        # Alternative: TensorFlow

# Time Series
statsmodels>=0.14.0       # ARIMA, SARIMA
prophet>=1.1.0            # Facebook Prophet
pmdarima>=2.0.0           # Auto-ARIMA

# LLM Integration
ollama>=0.1.0             # Lokale LLMs
openai>=1.0.0             # OpenAI API
langchain>=0.1.0          # LLM Orchestration

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
streamlit>=1.28.0         # Interactive Apps
```

---

##  Weiterführende Ressourcen

### Forschungsliteratur:
1. **Predictive Maintenance:**
   - "Machine Learning for Predictive Maintenance" (Schwabauer et al.)
   - "A Review of Predictive Maintenance Methods" (Lee et al.)

2. **Time Series Analysis:**
   - "Forecasting: Principles and Practice" (Hyndman & Athanasopoulos)
   - "Time Series Analysis with Python" (Peixeiro)

3. **Anomaly Detection:**
   - "Outlier Detection with LSTMs" (Malhotra et al.)
   - "Deep Learning for Anomaly Detection" (Chalapathy & Chawla)

### Tools & Frameworks:
- **Ollama Documentation:** https://ollama.ai/docs
- **Scikit-learn:** https://scikit-learn.org
- **PyTorch:** https://pytorch.org
- **LangChain:** https://python.langchain.com

---

##  Projektteam & Kontakt

**Research Lead:** Svitlana Kovalivska, Ph.D.  
**Projekt:** Industrial Signal Processing & Time Series Analysis  
**Institution:** Data Coffee GmbH 
**Zeitraum:** Phase 2 - Research & Planning (Abgeschlossen)

---

##  Versionierung

| Version | Datum | Beschreibung |
|---------|-------|--------------|
| 2.0 | 2025-09-08 | Initiale Forschungsplanung |
| 2.1 | 2025-09-10 | Technologie-Evaluierung dokumentiert |
| 2.2 | 2025-10-01 | Use Cases priorisiert und definiert |

---

**Status:**  Phase 2 abgeschlossen  
**Vorherige Phase:**  [`/data_and_eda/`](../data_and_eda/) (Abgeschlossen)  
**Nächste Phase:**  [`/srs/`](../srs/) (In Entwicklung)

---

*Von Forschungsfragen zu praktischen Lösungen - Eine datengetriebene Reise *
