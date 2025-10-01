Verstanden.

### **Gesamtfazit und vergleichende Analyse (Notebook 6 & 7)**

#### **Einleitung**
6-phase3_Numerical_Accuracy_Evaluation.ipynb

7-phase3_Numerical_Accuracy_Evaluation.ipynb

Die durchgeführten Experimente in den Notebooks `6-phase3` und
`7-phase3` dokumentieren eine systematische Untersuchung zur numerischen
Genauigkeit lokaler Sprachmodelle. Die Analyse entwickelte sich von der
Evaluierung leichter, stabiler Modelle hin zum Einsatz
leistungsfähigerer, aber ressourcenintensiverer Architekturen. Der
Vergleich beider Phasen liefert entscheidende Einblicke in das
Zusammenspiel von Modellkomplexität, Prompt-Engineering und den
limitierenden Faktoren lokaler Hardware.

#### **Beschreibung der Methodik: Modelle, Fragen und Prompts**

Die Experimente basieren auf einem iterativen Ansatz zur Verbesserung
der numerischen Genauigkeit. Es wurden unterschiedliche Modelle,
Fragenkataloge und Prompt-Strategien systematisch getestet.

**1. Verwendete Modelle:** 

* **Notebook 6 (Leichte Modelle):** \*
`ollama_expert (llama3.2:1b)` \* `ollama_universal (llama3.2:1b)` 
* **Notebook 7 (Leistungsstarke Modelle):** \* `mistral:7b-instruct` (7
Mrd. Parameter) \* `llama2:13b` (13 Mrd. Parameter)
 
------------------------------------------------------------------------

#### **Analyse des Fragenkatalogs und dessen Entwicklung**

Im Laufe der Experimente wurden zwei unterschiedliche Arten von
Fragenkatalogen verwendet, deren Komplexität sich für ein Sprachmodell
fundamental unterscheidet.

**Katalog 1: Offene, analytische Fragen (Ursprünglicher Ansatz)** 
* **Liste der Fragen:** 
1. `basic_statistics`: "Wie viele Datensätze
enthält das CNC Dataset insgesamt und welche Spalten sind verfügbar?"
2. `program_analysis`: "Identifiziere die 3 häufigsten Programme
(pgm_STRING) im Dataset und gib ihre prozentuale Verteilung an." 
3. `mode_efficiency`: "Vergleiche die Effizienz zwischen AUTOMATIC und
MANUAL Modus..." 
4. `execution_analysis`: "Analysiere die Ausführungszustände (exec_STRING). Wie hoch ist der Anteil der ACTIVE Zustände?" 
5. `comprehensive`: "Erstelle eine Übersicht: Gesamtanzahl Datensätze, häufigstes Programm, dominanter Modus und Anteil aktiver Zustände." \

* **Analyse der Komplexität (HOCH):** Diese Fragen sind
qualitativ und erfordern vom Modell ein mehrstufiges, analytisches
Denken. Eine einzelne Frage verlangt oft mehrere Rechenschritte,
Interpretationen ("Vergleiche die Effizienz") und die Generierung einer
zusammenfassenden Textantwort. Dies erhöht die kognitive Last auf das
Modell und die Wahrscheinlichkeit für Fehler erheblich.

**Katalog 2: Präzise, atomare Fragen (Finaler Ansatz)** 
* **Liste der Fragen:** 
1. `q1_total_records`: "Wie viele Datensätze enthält das CNC Dataset GENAU? Antworte nur mit der Zahl." (Erwartet: `113855`).

2.`q2_top_program_count`: "Wie oft kommt das Programm '...' GENAU im
Dataset vor? Antworte nur mit der Zahl." (Erwartet: `63789`).

3.`q3_top_program_percentage`: "Welchen GENAUEN Prozentsatz macht das
Programm '...' aus? ..." (Erwartet: `56.0`).
 
4.`q4_automatic_count`:"...mode_STRING = 'AUTOMATIC'?... (Erwartet: `77295`)

5.`q5_automatic_percentage`:"...Prozentsatz... 'AUTOMATIC'?... (Erwartet:
`67.9`)

6. `q6_manual_count`: "...mode_STRING = 'MANUAL'?... (Erwartet:
`36560`) 

7. `q7_auto_manual_ratio`:"...Verhältnis...AUTOMATIC zu
MANUAL...?" (Erwartet: `2.11`) 

8. `q8_active_count`: "...exec_STRING = 'ACTIVE'?... (Erwartet: `40908`)

9. `q9_active_percentage`:"...Prozentsatz... 'ACTIVE'?... (Erwartet:
`35.9`) 
*  **Analyse der Komplexität (NIEDRIG):** Diese Fragen sind
quantitativ und atomar. Jede Frage ist eine einzelne,
unmissverständliche Rechenaufgabe. Durch die Zerlegung komplexer
Analysen in einfache, präzise Einzelschritte und die strikte Vorgabe des
Ausgabeformats ("Antworte nur mit der Zahl") wird die Aufgabe für das
LLM drastisch vereinfacht.

**Vergleichendes Fazit:** Der Übergang von offenen zu atomaren Fragen
ist ein entscheidender Schritt im Prompt-Engineering. Er reduziert die
Komplexität für das Modell, minimiert Interpretationsspielräume und
führt zu deutlich zuverlässigeren und maschinell validierbaren
Ergebnissen.

------------------------------------------------------------------------

#### **Die Prompt-Strategien**

-   **Ansatz 1: Basic Prompts (Baseline):** Minimalistische, direkte
    Fragen ohne zusätzlichen Kontext. Dient als Grundlinie, um die
    "rohe" Fähigkeit der Modelle zu messen.
-   **Ansatz 2: "Klassische" Experten-Prompts:** Zuweisung einer
    Expertenrolle und Bereitstellung eines reichhaltigen Datenkontextes
    (allgemeine Statistiken).
-   **Ansatz 3: Verbesserte / Analytische Experten-Prompts:**
    Kombination aus reichem Kontext und einer expliziten,
    algorithmischen Anleitung (Chain-of-Thought-Ansatz).

------------------------------------------------------------------------

### **Vergleichende Analyse der Experimente (Notebook 6 vs. Notebook 7)**

#### **Gesamtanalyse**

Der zentrale Unterschied zwischen den beiden Testläufen liegt im Einsatz
unterschiedlicher lokaler Sprachmodelle. Im ersten Notebook
(`6-phase3...`) wurden leichtere Modelle (`llama3.2:1b`) verwendet, die
stabil, aber mit begrenzter Genauigkeit operierten. Im zweiten Notebook
(`7-phase3...`) wurde zu leistungsfähigeren, aber anspruchsvolleren
Modellen (`mistral:7b-instruct` und `llama2:13b`) gewechselt. Dieser
Wechsel führte zu fundamental unterschiedlichen Ergebnissen und deckte
kritische Limitationen der lokalen Hardware auf.

#### **Schritt 1: Ausgangssituation und erste Erkenntnisse (Notebook 6)**

-   **Verwendete Modelle:** `ollama_expert (llama3.2:1b)` und
    `ollama_universal (llama3.2:1b)`.
-   **Ergebnisse:**
    -   Beide Modelle liefen stabil und mit hoher Geschwindigkeit
        (durchschnittlich 15-20 Sekunden pro Antwort).
    -   Die Genauigkeit war stark von der Qualität des Prompts abhängig.
        Mit einfachen "Basic"-Prompts war die Genauigkeit gering
        (11-22%).
    -   Durch den Einsatz verbesserter "Enhanced Expert"-Prompts stieg
        die Genauigkeit signifikant auf **67-89%** an.
-   **Schlussfolgerung dieser Phase:** Es wurde bereits hier
    ersichtlich, dass Prompt-Engineering ein entscheidender Faktor für
    den Erfolg ist. Selbst kleinere lokale Modelle können bei korrekter
    Aufgabenstellung zufriedenstellende Ergebnisse liefern.

#### **Schritt 2: Einsatz leistungsfähigerer lokaler Modelle (Notebook 7)**

-   **Verwendete Modelle:** `mistral:7b-instruct` (7 Milliarden
    Parameter) und `llama2:13b` (13 Milliarden Parameter).
-   **Ergebnisse:**
    -   **Totalausfall von `llama2:13b`:** Das leistungsstärkste Modell
        (`llama2:13b`) konnte keine einzige Frage beantworten und endete
        bei allen Tests mit einem `Read timed out`-Fehler.
    -   **Bedingter Erfolg von `mistral:7b-instruct`:** Dieses Modell
        erwies sich als funktionsfähig und erreichte mit den optimierten
        "Expert Prompts" eine **perfekte Genauigkeit von 100%**. Dies
        geschah jedoch zulasten einer erheblich reduzierten Performance.
-   **Schlussfolgerung dieser Phase:** Der Leistungsunterschied ist
    gravierend. Während im ersten Test beide Modelle funktionierten,
    versagte im zweiten das stärkere Modell vollständig, was in direktem
    Zusammenhang mit den Hardware-Limitationen des lokalen Systems
    steht.

------------------------------------------------------------------------

### **Analyse der Performance-Probleme und Modellausfälle**

Die beobachteten Leistungsengpässe bestätigen die technischen
Limitationen bei der lokalen Ausführung großer Sprachmodelle.

-   **Hohe Ressourcenauslastung:** Die Ausführung einer Testzelle über
    **56 Minuten** sowie die allgemeine Verlangsamung des Systems sind
    auf die enormen Anforderungen der Modelle an die Systemressourcen
    zurückzuführen:
    -   **Arbeitsspeicher (RAM/VRAM):** Das `llama2:13b`-Modell benötigt
        bereits über 7,4 GB Speicher nur für seine Gewichte. Bei
        unzureichendem Arbeitsspeicher nutzt das Betriebssystem die
        Auslagerungsdatei (Swap) auf der Festplatte, was zu einer
        drastischen Verlangsamung führt.
    -   **Rechenleistung (CPU/GPU):** Die Verarbeitung eines Requests
        durch ein großes Modell stellt eine hochintensive
        Rechenoperation dar, die die Hardware über längere Zeit
        vollständig auslastet.
-   **Ursache für den Ausfall von `llama2:13b`:** Das Modell konnte
    innerhalb des Zeitlimits von 120 Sekunden keine Antwort generieren,
    da das lokale System nicht in der Lage war, ein Modell dieser Größe
    effizient zu verarbeiten.

------------------------------------------------------------------------

### **Finale Schlussfolgerungen**

Die Analyse beider Experimente führt zu folgenden Erkenntnissen:

-   **Leistungsfähigere lokale Modelle führen nicht zwangsläufig zu
    besseren Ergebnissen.** Das leistungsstärkste Modell (`llama2:13b`)
    erwies sich aufgrund von Hardware-Beschränkungen als unbrauchbar.
    `mistral:7b-instruct` zeigte zwar eine exzellente Genauigkeit, litt
    jedoch unter inakzeptabel langen Antwortzeiten.
-   **Eine Erhöhung der Komplexität lokaler Modelle ist ohne adäquate
    Hardware nicht sinnvoll.** Die limitierenden Faktoren sind primär:
    -   Arbeitsspeicher (RAM/VRAM)
    -   Prozessor- und Grafikkartenleistung (CPU/GPU)
    -   Inakzeptable Ausführungszeiten
    -   Hohes Risiko von Instabilität und Fehlschlägen
-   **Implikationen für API-basierte Modelle:** Das Experiment
    demonstriert klar den praktischen Vorteil von **Premium-Modellen,
    die über eine API zugänglich sind**. Diese Modelle laufen auf
    hochspezialisierter Server-Hardware und eliminieren die lokalen
    Performance-Engpässe. Die Fortsetzung der Arbeit mit API-Modellen
    ist daher der logische nächste Schritt.
