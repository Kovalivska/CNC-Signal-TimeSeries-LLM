# Project Scope: LLM-driven Machine Data Analysis

## Ziel
Mini-Mockup LLM driven Machine Data Analysis

## Unterziel
Validierung Aufwände und Leistungsfähigkeit des Ansatzes

## Vorschlag zum Vorgehen

### 1. Datenbasis
- Als Datenbasis gelten die CNC Daten
- Wähle die Daten einer Maschine aus


### 2. Mockup-Entwicklung
Baue das Mockup so, dass Fragen über Zykluszeiten und Betriebszeiten gestellt werden können:

**Beispielhafte Fragen:**
- Wie lange waren die Zykluszeiten heute / in der letzten Stunde?
- Was war der längste / kürzeste Zyklus?
- Wann war der längste / kürzeste Zyklus?
- Wie lange war die Anlage im Auto-Modus?
- [weitere Fragen zur Validierung der LLM-Funktionsweise]

**Relevante Variablen für die Beantwortung:**
- `pgm` = Program
- `mode` = Betriebsmodus  
- `exec` = Zustand

### 3. Testing und Validierung
- Teste den Aufbau: Wie genau kann das System die Fragen beantworten?
- Wo scheitert es mehr, wo weniger?

### 4. Skalierung (falls erfolgreich)
1. Validiere das Vorgehen für die beiden anderen Maschinen
   - Erst für eine Maschine für sich
   - Dann alle Maschinen zusammen (z.B. Fragen wie: "welche Maschine hat die längste Zykluszeit?")

2. Daten-Simulation
   - Ggf. Daten simulieren, um einen Monat abzubilden
   - Erneut das Prinzip validieren

## Wichtige Anforderungen
- Ein Prinzip / eine kleinste Instanz entwickeln
- Muss nicht perfekt funktionieren
- Ziel: Vorgehen erproben und Aufwand abschätzen
- **Wichtig:** Ein richtiges LLM muss zum Einsatz kommen
- **Wichtig:** Fragen dürfen NICHT vorkonfiguriert in Algorithmen gegossen werden

## Erwartete Ergebnisse
- Validierung der Machbarkeit des LLM-Ansatzes
- Aufwandsschätzung für das Ausrollen
- Bewertung der Funktionsfähigkeit des angedachten Vorgehens