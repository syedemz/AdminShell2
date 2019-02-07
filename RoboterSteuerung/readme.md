Im Ordner "RoboterSteuerung" werden die verschiedenen Versionen der
Robotersteuerung gesammelt. Diese sind nicht in der Verwaltungsschale
angesiedelt, weil sie damit zunächst nichts zutung
haben.

## Versionen:

### 1. Robotersteuerung_v1_inc_AS
  - Anmeldung in RM - Add (localhost:40000): Erika Mustermann (Passwort: 123)
  - beinhaltet eine ältere Version der Verwaltungsschale und funktioniert nur
  damit!
  - entspricht dem Stand von Thomas Präsentation
  - Kommunikation von AS zu Robotersteuerung in beide Richtungen
  - Robotersteuerung nutzt zum Teil die zeroMQ Kommunikation

### 2. Robotersteuerung_v2
  - funktioniert auch ohne AS
  - Schnittstelle zur AS:
      - Kommunikation AS -> Robotersteuerung über Port 60111
      - bisher keine Kommunikation RoboterSteuerung -> AS
      - Schnittstelle erwartet Motorwinkeln - Anweisungen: XX YY ... ... ...

### 3. Robotersteuerung_v3 -> in Progress
  - neu aufgebaute v1.  
  - in Arbeit, bisher nur eingeschränkt nutzbar
  - Ziele:
      - Vereinfachung
      - Entfernung nicht genutzter Teile
      - eindeutige Benennung der  Signale, Variablen, ...
      - Eingliederung der Arduino Schnittstelle in Motorsteuerung
