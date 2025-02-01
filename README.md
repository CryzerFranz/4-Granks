# 4 Granks (4 Gewinnt mit Gestenerkennung)

## Beschreibung
"4 Granks" ist eine erweiterte Version des klassischen Spiels "4 Gewinnt", das mit Handgestensteuerung über eine Webcam gespielt werden kann. Das Spiel verwendet **OpenCV** und **Mediapipe** zur Handerkennung und **Pygame** zur Darstellung und Spiellogik.

## Voraussetzungen
Damit das Programm ausgeführt werden kann, müssen folgende Abhängigkeiten installiert sein:

### Systemvoraussetzungen
- Betriebssystem: Windows, macOS oder Linux
- Python 3.7 oder höher
- Eine funktionierende Webcam

### Python-Bibliotheken
Installiere die benötigten Bibliotheken mit folgendem Befehl:
```sh
pip install pygame opencv-python mediapipe numpy
```

## Installation & Ausführung
1. Klone oder lade das Repository herunter.
2. Stelle sicher, dass alle Abhängigkeiten installiert sind.
3. Starte das Spiel mit folgendem Befehl:
   ```sh
   python main.py
   ```

## Steuerung & Spielablauf
- **Handgestensteuerung:**
  - **Zeigefinger nach oben halten:** Auswahl einer Spalte.
  - **Hand öffnen:** Platziere einen Spielstein in der ausgewählten Spalte.
  
- **Alternative Steuerung:**
  - Mit der Maus kann das Spiel geschlossen werden (Schließen-Button oben rechts).
  - Falls das Spiel vorbei ist, kann es über den "Neu"-Button neugestartet werden.

## Features
- **Handerkennung mit Mediapipe** zur Steuerung des Spiels.
- **Flüssige Animationen** für das Einwerfen der Spielsteine.
- **Einfaches und intuitives UI** mit Pygame.
- **Zwei-Spieler-Modus** (abwechselnde Züge).

## Bekannte Probleme
- Falls die Webcam nicht erkannt wird, überprüfe, ob sie von anderen Programmen blockiert wird.
- Wenn die Hand nicht erkannt wird, erhöhe die Beleuchtung oder halte die Hand näher an die Kamera.

## Entwickler
- **Autor:** [Christophe Paleyron, Luis Schulte, Jonas Geißendörfer]
- **Lizenz:** Open Source

