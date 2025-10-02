# Flask File Upload Demo

Detta projekt visar hur man hanterar filuppladdningar med Flask och ett HTML-formulär.

## Funktioner
- Ladda upp filer via ett webbformulär
- Filer sparas i mappen `uploads`
- Flash-meddelanden visar status för uppladdning
- `.gitignore` exkluderar uppladdade filer från versionshantering

## Kom igång

1. Installera beroenden:
```
    pip install -r requirements.txt
   ```
   eller
   ```
py -m pip install -r requirements.txt
   ```
2. Starta servern:
```
python app.py
   ```
   eller 
   ```
py app.py
   ```
3. Öppna webbläsaren och gå till `http://localhost:5000` eller `http://127.0.0.1:5000`


## Noteringar
- Endast vissa filtyper tillåts (se `ALLOWED_EXTENSIONS` i `app.py`).
- Mappen `uploads` är ignorerad av Git förutom `.gitkeep`-filen.