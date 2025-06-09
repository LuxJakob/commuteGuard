# commuteGuard

Ein tapferer kleiner Cronjob, der täglich seinen Dienst tut: Wetterlage checken, Bahnchaos prüfen, und dir dann eine Mail schicken – damit du weißt, ob du heute einen Regenschirm brauchst oder lieber gleich zu Hause bleibst.

Features:
- Wetterbericht direkt in dein Postfach
- Bahnstatus (aka "Lohnt es sich schon loszulaufen?")

## Step 1 - Activate Virtual Environment

```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

## Step 2 - Install the required python modules

```bash
pip install -r requirements.txt
```

## Step 3 - Run the project

Go into the project, view the available spiders, run the project.

```bash
python3 src/main.py
```
