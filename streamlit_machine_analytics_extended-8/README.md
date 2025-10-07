# CNC Maschinen-Analytics (Offline) — Datenanalyse-Tool für die Fertigungsindustrie

**🚀 Live-Demo:** [Zur Anwendung](https://cnc-signal-timeseries-llm-7m5vzvnyzxrl9gww7wrar4.streamlit.app/) 

> **🔬 Prototyp-Hinweis:** Diese Anwendung ist ein funktionsfähiger Prototyp für ein zukünftiges Hauptprojekt. Die finale Version wird nach Abschluss der Prompt-Engineering-Entwicklung für das Hauptprojekt verfügbar sein.

Diese Streamlit-Anwendung bietet eine **vollständig offline** Analyse von CNC-Maschinendaten mit intelligenter Metriken-Berechnung und Visualisierung. Das Tool ist speziell für die industrielle Signalverarbeitung und Zeitreihenanalyse von Fertigungsanlagen entwickelt, mit **Anwendungspotenzial für Anomalieerkennung** und **Überwachung kritischer Systeme**.

## 📸 Anwendungsbeispiele

![Hauptdashboard](results/Screenshot%20at%20Oct%2004%2008-50-08.png)
*Hauptbenutzeroberfläche mit Datenupload und Filteroptionen*

![Zeitreihen-Visualisierung](results/Screenshot%20at%20Oct%2004%2008-59-25.png)
*Dynamische Zeitreihen-Darstellung mit Multi-Achsen-Skalierung*

![KPI-Analyse](results/Screenshot%20at%20Oct%2004%2008-59-47.png)
*Schichtbasierte KPI-Berichte mit SQL-Dokumentation*

![Zykluszeit-Analyse](results/Screenshot%20at%20Oct%2004%2009-21-13.png)
*Automatische Zykluszeit-Erkennung und Produktivitätsanalyse*

## Funktionen

###  **Sicherheit & Datenschutz**
- **Vollständig offline**: Keine Datenübertragung an externe Server
- **On-Premise-Deployment**: Vollständige Kontrolle über sensible Produktionsdaten
- **Anomalieerkennung**: Statistische Ausreißer-Identifikation für Sicherheitsüberwachung
- **Risikobewertung**: Automatische Erkennung ungewöhnlicher Maschinenverhaltensweisen

### **Datenunterstützung**
- Mehrere Dateiformate: CSV, Parquet, JSON, JSONL
- Automatische Zeitstempel-Parsing und Zeitzonenbehandlung
- Unterstützung für 90+ vordefinierte CNC/SPS-Signalfelder
- Dynamische Schema-Erkennung und Spaltenanalyse

### 🔧 **Hauptmetriken & Analytics**
- **Zykluszeit-Analyse**: Automatische Erkennung abgeschlossener Teile durch mehrere Methoden
- **Rüstzeit-Analyse**: Sowohl explizite Modus-Erkennung als auch heuristische Lückenanalyse
- **Produktionsleistung**: Teilezählung und Durchsatzanalyse
- **Schichtbasierte KPIs**: 3-Schicht-Analyse (06-14, 14-22, 22-06)
- **Dynamische Zeitreihen**: Top-K variabelste numerische Signale mit Anomalieerkennung

### 🎯 **Voreingestellte Abfragen**
- Durchschnittliche Zykluszeit-Berechnung
- Rüstzeit-Analyse pro Maschine
- Produktionsleistungs-Ranking
- Schichtbasierte KPI-Berichte
- Dynamische Zeitreihen-Visualisierung
- Anpassbare Metriken-Auswahl

### 🌐 **Mehrsprachige Unterstützung**
Frage-Parsing unterstützt deutsche, englische und russische Schlüsselwörter für intuitive Abfragen.

Die Anwendung unterstützt 90+ vordefinierte CNC/SPS-Signalfelder einschließlich:

```yaml
Kernfelder:
  - name: Maschinenidentifikator
  - time: UTC-Zeitstempel
  
Ausführungssignale:
  - exec_program_completed_BOOL: Programmabschlussstatus
  - exec_STRING: Ausführungsstatustext
  - exec_active_BOOL, exec_ready_BOOL, exec_stopped_BOOL: Maschinenzustände
  
Modus & Rüstung:
  - mode_STRING: Betriebsmodus (inkl. SETUP/RÜST-Erkennung)
  - mode_automatic_BOOL, mode_manual_BOOL: Modus-Flags
  - pgm_STRING: Programmidentifikator
  
Prozessparameter:
  - 30+ REAL/LREAL-Felder: Temperaturen, Positionen, Zeiten, Geschwindigkeiten
  - 20+ STRING-Felder: Statuscodes, Bedingungen, Gesundheitsindikatoren
  - 15+ BOOL-Felder: Binäre Zustandsflags
```

*Siehe `/resources/dictionary.md` für vollständige Feldbeschreibungen.*

## Algorithmus-Details

### Zykluszeit-Erkennung
Die Anwendung verwendet einen dreistufigen Ansatz zur Erkennung abgeschlossener Fertigungszyklen:

1. **Steigende Flanken-Erkennung**: Überwacht `exec_program_completed_BOOL` für Zustandsübergänge (False → True)
2. **Text-Muster-Erkennung**: Durchsucht `exec_STRING` nach Abschluss-Schlüsselwörtern (`COMPLETED|END|FINISH`)
3. **Programm-Wechsel-Fallback**: Erkennt Programmübergänge in `pgm_STRING`, wenn explizite Signale nicht verfügbar sind

Zykluszeiten werden als Zeitstempel-Differenzen zwischen aufeinanderfolgenden Ereignissen berechnet, mit **IQR-basierter Ausreißer-Filterung** zur Entfernung von Datenanomalien.

### Rüstzeit-Analyse
- **Explizite Modus-Erkennung**: Identifiziert zusammenhängende Intervalle, in denen `mode_STRING` Rüst-Schlüsselwörter enthält (`SETUP|RÜST|RUEST`)
- **Heuristische Lücken-Analyse**: Erkennt lange Leerlaufperioden (≥5 Minuten) um Programmwechsel oder Zustandsübergänge
- **Multi-Maschinen-Unterstützung**: Verfolgt Rüstvorgänge pro einzelner Maschine

### Dynamische Metriken-Entdeckung
Identifiziert automatisch die relevantesten numerischen Signale durch:
- Filterung nach numerischen Datentypen und SPS-Namenskonventionen (`_REAL`, `_LREAL`, `_BOOL`, etc.)
- Bewertung von Spalten nach Änderungshäufigkeit über die Zeit
- Ranking nach Variabilität zur Hervorhebung der informativsten Prozessparameter

**Anwendung für Sicherheitsmonitoring:** Diese Techniken können für Anomalieerkennung und Zustandsüberwachung kritischer Systeme adaptiert werden.

## Schnellstart

### Voraussetzungen
- Python 3.9+
- Erforderliche Pakete: `streamlit`, `pandas`, `duckdb`, `pyarrow`, `pytz`

### Installation & Start
```bash
# Projekt klonen oder herunterladen
cd streamlit_machine_analytics_extended-8

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
streamlit run app.py
```

Die Anwendung öffnet sich in Ihrem Browser unter `http://localhost:8502`

### Arbeitsablauf
1. **Daten hochladen**: CSV/Parquet/JSON-Dateien per Drag & Drop in der Seitenleiste
2. **Filter anwenden**: Maschinen und Datumsbereiche auswählen
3. **Analyse wählen**:
   - Voreingestellte Abfragen für häufige Analysen verwenden
   - Freitext-Fragen auf Deutsch/Englisch/Russisch stellen
   - Dynamische Zeitreihen-Visualisierung erkunden
4. **Ergebnisse betrachten**: Interaktive Diagramme, SQL-Abfragen und Datentabellen

## Technische Architektur

### Datenverarbeitungs-Pipeline
```mermaid
graph LR
    A[Rohdateien] → B[pandas DataFrame]
    B → C[Zeitstempel-Parsing]
    C → D[Ereignis-Erkennung]
    D → E[DuckDB-Tabellen]
    E → F[SQL-Analytics]
    F → G[Streamlit-Visualisierung]
```

### In-Memory-Datenbank
- **DuckDB** für hochperformante analytische Abfragen ohne externe Verbindungen
- Drei registrierte Tabellen:
  - `events`: Roh-Telemetriedaten
  - `part_events`: Erkannte Zyklusabschlüsse
  - `setup_intervals`: Rüst-/Umstellungsperioden

### Ereignis-Erkennungsalgorithmen
- **Statistische Ausreißer-Entfernung**: IQR-basierte Filterung für Zykluszeiten
- **Zustandsmaschinen-Analyse**: Erkennung von Boolean-Signal-Übergängen
- **Text-Mining**: Regex-Musterabgleich für Statuscodes
- **Zeitlücken-Analyse**: Heuristische Erkennung von Rüstperioden

**Sicherheitsrelevanz:** Offline-Verarbeitung und statistische Anomalieerkennung bieten Grundlagen für sicherheitskritische Anwendungen.

## Beispiel-Abfragen

### Voreingestellte Fragen (Deutsch)
- "Durchschnittliche Zykluszeit" → Durchschnittliche Zykluszeit-Berechnung
- "Gesamte Rüstzeit" → Gesamte Rüstzeit-Analyse
- "Meiste Produktion" → Top-produzierende Maschinen
- "KPIs pro Schicht" → Schichtbasierte Leistungsmetriken

### Freitext-Fragen
```text
Deutsch: "Wie lange ist die durchschnittliche Zykluszeit?"
Englisch: "What is the average cycle time?"
Russisch: "Какое среднее время цикла?"
```

### Dynamische Zeitreihen
- **Top-5 Auto-Auswahl**: Identifiziert automatisch die variabelsten Metriken
- **Benutzerdefinierte Auswahl**: Wählen Sie bis zu 10 spezifische Parameter
- **Aggregationsebenen**: Roh, 10s, 1min, 1h, 1Tag, 1Woche

## Konfiguration & Anpassung

### Erkennungsschwellenwerte ändern
```python
# In app.py
THRESHOLD_S = 5 * 60  # Rüst-Erkennungsschwelle (Sekunden)
DEFAULT_TZ = "Europe/Berlin"  # Zeitzone für Schichtberechnung
```

### Neue voreingestellte Abfragen hinzufügen
Bearbeiten Sie `/templates/presets.json`:
```json
{
  "name": "Ihre benutzerdefinierte Abfrage",
  "id": "custom_query_id"
}
```

### Datenschema erweitern
Die Anwendung erkennt automatisch neue numerische/boolean Spalten nach SPS-Namenskonventionen:
- `*_REAL`, `*_LREAL`: Fließkomma-Werte
- `*_BOOL`: Boolean-Flags
- `*_STRING`: Text-/kategorische Daten

## Deployment-Optionen

### Lokale Entwicklung
```bash
streamlit run app.py --server.port 8502
```

### Produktions-Deployment
1. **Docker-Container**:
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8502
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

2. **Streamlit Cloud**: Zu GitHub pushen und über streamlit.io deployen
3. **Lokales Netzwerk**: `--server.address 0.0.0.0` für LAN-Zugriff verwenden

## Leistung & Einschränkungen

### Empfohlene Datengrößen
- **Optimal**: < 1M Zeilen pro Sitzung
- **Gute Leistung**: 1-10M Zeilen (möglicherweise Aggregation erforderlich)
- **Große Datensätze**: Vor-Filterung nach Datum/Maschine in Betracht ziehen

### Speicherverbrauch
- Rohdaten in pandas DataFrame gehalten
- DuckDB bietet effiziente analytische Abfragen
- Zeitreihen-Resampling reduziert Speicher-Footprint

## Fehlerbehebung

### Häufige Probleme
1. **Fehlende Zeitstempel**: Sicherstellen, dass `time`-Spalte existiert und parsbar ist
2. **Keine Maschinennamen**: Überprüfen, dass `name`-Spalte Maschinenidentifikatoren enthält
3. **Leere Ergebnisse**: Datumsfilter und Datenverfügbarkeit prüfen
4. **Leistung**: Datengrößenbeschränkungen und Aggregationsoptionen berücksichtigen

### Debug-Modus
`st.write()`-Anweisungen hinzufügen, um Zwischendaten zu inspizieren:
```python
st.write("Teile erkannt:", len(parts))
st.write("Rüst-Intervalle:", len(setups))
```

## Projektinformationen

### Versionshistorie
- **v8**: Erweiterte Analytics mit dynamischen Metriken, Schichtanalyse und mehrsprachiger Unterstützung
- **Fokus**: Offline CNC-Datenanalyse und -visualisierung
- **Technologie-Stack**: Python, Streamlit, DuckDB, pandas, pytz

### Verwandte Komponenten
Dieses Tool ist Teil eines größeren **Industrial Signal Processing & Time Series Analysis** Projekts:
- **Datenverarbeitung**: `/data_and_eda/` - Explorative Datenanalyse-Notebooks
- **Forschung**: `/research_and_project_scope/` - Technische Dokumentation und Analyse-Ansätze
- **Ergebnisse**: `/results/` - Ausgaben verschiedener analytischer Modelle
- **Tests**: `/tests/` - Validierungs- und Test-Skripte
- **🤖 IONOS Model Demo**: [`/ionos_model_demo/`](../ionos_model_demo/) - **NEU!** Streamlit-Demo der LLM-Prompt-Engineering-Ergebnisse

### 🤖 IONOS Model Demo — LLM-Prompt-Engineering Demonstration

![IONOS Model Demo](../ionos_model_demo/Screenshot%20at%20Oct%2004%2010-15-44.png)

**Neue Streamlit-Anwendung zur Demonstration der Prompt-Engineering-Ergebnisse**

📂 **Demo-Verzeichnis:** [`/ionos_model_demo/`](../ionos_model_demo/)  
🚀 **Direktstart:** `cd ionos_model_demo && streamlit run app.py`

**Funktionen:**
- 🎯 **9 CNC-Testfragen** aus dem Hauptprojekt
- 🧠 **5 Prompt-Ansätze**: Basic, Expert, Enhanced, Systematic, ML
- 📊 **Interaktive Vergleichsanalyse** aller Prompt-Strategien
- 📈 **Visualisierungen**: Balkendiagramme und Heatmaps für Genauigkeitsvergleiche
- 🎨 **Benutzerfreundliche UI** mit breiter Sidebar für vollständige Prompt-Anzeige

**Ergebnisse:** Enhanced- und Systematic-Ansätze zeigen 75-85% Genauigkeit bei CNC-Datenanalysen, während Basic-Ansatz nur 25% erreicht.

### Zukünftige Erweiterungen
- [ ] PDF/PNG-Export-Funktionalität
- [ ] Integration mit lokalen LLM-Modellen (Ollama/llama.cpp)
- [ ] Erweiterte Anomalie-Erkennung mit Machine Learning
- [ ] Echtzeit-Datenstreaming-Unterstützung
- [ ] Benutzerdefinierte Dashboard-Vorlagen
- [ ] Multi-Tenant-Deployment-Optionen
- [ ] Anwendung der Techniken für Sicherheitsmonitoring

---
**Lizenz**: MIT  
 
**Letzte Aktualisierung**: Oktober 2025
