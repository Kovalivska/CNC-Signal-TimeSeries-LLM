# LLM-gesteuerte Analyse von CNC-Maschinendaten

> Eine iterative Reise zur Validierung einer "Zero-Algorithm"-Strategie

[![Status](https://img.shields.io/badge/Status-Ready%20for%20Production-green)](.)
[![Framework](https://img.shields.io/badge/Framework-LangChain-blue)](https://langchain.com)
[![Model](https://img.shields.io/badge/Tested%20Model-llama3.2%3A1b-orange)](.)

---

## 🆕 Wichtiger Hinweis zum letzten Testlauf

Im Rahmen des letzten Testlaufs haben wir in erster Linie die logische Schlüssigkeit und strukturelle Richtigkeit der Modellantworten bewertet, wobei ein Vertrauensscore nahe 100% erreicht wurde. Wichtig ist zu betonen, dass in dieser Phase **keine strikte numerische Validierung** durchgeführt wurde – das heißt, wir haben die vom Modell berechneten Zahlen nicht mit Referenzwerten verglichen.  
➡️ Dies ist unser nächster kritischer Schritt: Jetzt, da das Modell gelernt hat, korrekt zu argumentieren, müssen wir messen, wie genau es rechnen kann.

---

## 🎯 Projektübersicht

Dieses Projekt validiert einen revolutionären **"Zero-Algorithm"-Ansatz** zur Analyse von CNC-Maschinendaten mithilfe von Large Language Models (LLMs). Das Ziel ist es, komplexe Zeitreihendaten durch Anfragen in natürlicher Sprache zugänglich zu machen, ohne auf vordefinierte Algorithmen angewiesen zu sein.

### Die Kernfrage
> **Können wir Maschinendaten ausschließlich mit einem LLM analysieren, ohne hartcodierte Geschäftslogik zu verwenden?**

### Ziele
- 📊 Direkte Beantwortung von Fragen in natürlicher Sprache (z. B. „Was war der längste Zyklus?“)  
- 🔧 Universeller Ansatz ohne vordefinierte Analysealgorithmen  
- ⚡ Validierung durch reproduzierbares A/B-Testing  

---

## 🚀 Phase 2 – Korrigierte Ergebnisse & A/B-Testing

Nach der Identifizierung eines kritischen Fehlers im Datenschema wurde dieser behoben.  
Dies führte zu einer vollständigen Neubewertung des *"Pure LangChain Zero-Algorithm"*-Ansatzes.

### Die Korrektur
- **Datenschema-Korrektur**: Anpassung der Prompts an die realen Spalten (`pgm_STRING`, `exec_STRING`, `ctime_REAL`)  
- **Chain of Thought (CoT)**: Erweiterung der Prompts mit schrittweiser Argumentationslogik  
- **Präzise Variablenbeschreibung**: Explizite Erklärung jeder Datenspalte für maximalen Kontext  

### A/B-Testing: Expert vs. Universal
- **Ansatz A – Expert Domain**: LLM als CNC-Spezialist  
- **Ansatz B – Universal**: LLM als objektiver Datenanalyst ohne Fachwissen  

**Ergebnisse:**  
- Vertrauensscore: von ~0% → ~99–100%  
- Stabilität: alle Tests fehlerfrei, Antwortzeiten 22–28 Sekunden  
- Sieger: **Universal-Ansatz** in 100% der Tests  

➡️ Die Null-Hypothese (Expertenwissen schlägt Universal) wurde **verworfen**.

### Wichtigste Erkenntnisse
1. **Kontext ist entscheidend, nicht nur Expertise**  
2. **Struktur schlägt simuliertes Wissen**  
3. **Chain of Thought funktioniert auch bei kleinen Modellen (llama3.2:1b)**  

---

## 📈 Technischer Status

- ✅ **"Pure LangChain Zero-Algorithm" validiert** – LLM entwickelt eigenständig Strategien  
- ✅ **113.000+ CNC-Datensätze** korrekt verarbeitet  
- ✅ **A/B-Testing Framework** voll einsatzfähig  

---

## 🔮 Phase 3 – Nächste Schritte

Das Framework ist bereit für den nächsten Sprung:  
- Test mit **Premium-LLMs** (GPT-4o, Claude)  
- Fokus: **numerische Validierung** → Vergleich von Modell-Berechnungen mit Referenzwerten  
- Ziel: Messen, wie genau das LLM nicht nur denkt, sondern auch rechnet  

---
