# 📱 Com instal·lar el Joc de la Granota a l'iPhone

## Opció 1: Instal·lar GRATIS amb GitHub Pages (Recomanat) ⭐

### Pas 1: Puja els fitxers a GitHub
1. Crea un repositori nou a GitHub (https://github.com/new)
   - Nom: `joc-granota`
   - Marca "Public"
   - Clica "Create repository"

2. Puja els fitxers:
   ```
   git clone https://github.com/TU_USER/joc-granota.git
   cd joc-granota
   ```
   - Copia els arxius `index.html` i `manifest.json` a aquesta carpeta
   
3. Puja a GitHub:
   ```
   git add .
   git commit -m "Afegir joc de la granota"
   git push origin main
   ```

4. Activa GitHub Pages:
   - Vai a Settings → Pages
   - Source: selecciona "main"
   - Clica "Save"
   - Espera 1-2 minuts

5. La URL será: `https://TU_USER.github.io/joc-granota/`

---

### Pas 2: Instal·lar a l'iPhone

1. **Obri Safari** a l'iPhone
2. **Entra** a la URL: `https://TU_USER.github.io/joc-granota/`
3. Clica el botó **"Compartir"** (icona de quadrat amb fletxa) ↗️
4. Busca i clica **"Afegir a la pantalla d'inici"**
5. Li pose un nom (ex: "Granota")
6. Clica **"Afegir"** a la cantonada superior dreta

✅ **Llestos!** Tindrà una icona al home screen com una app normal!

---

## Opció 2: Usar Netlify (Encara més fàcil)

1. Vai a https://app.netlify.com
2. Clica "Add new site" → "Deploy manually"
3. Arrossega els arxius `index.html` i `manifest.json`
4. Espera que es processi
5. Obri la URL a l'iPhone i segueix Pas 2 de dalt

---

## Opció 3: Usar un servidor local (Per a desenvolupament)

Si vols provar localment:

```bash
# Instal·lar Python Simple HTTP Server
python3 -m http.server 8000
```

Llavors obri `http://localhost:8000/index.html` al navegador

---

## Troubleshooting

❌ **No apareix el botó "Afegir a la pantalla d'inici"?**
- Assegura't que tens Safari actualitzat
- Intenta en mode privat
- Obri des de Safari (no des de Chrome)

❌ **La URL no carrega?**
- Espera 5 minuts més després d'activar GitHub Pages
- Comprova que els arxius estan al repositori

❌ **El joc no té so?**
- Els sons es generen dinàmicament (sin dependencies externes)
- Comprova que el volum del telèfon estigui activat

---

## Controls

🎮 **Teclat (si jugues desde PC):**
- ⬆️ Fletxa amunt / W
- ⬇️ Fletxa avall / S
- ⬅️ Fletxa esquerra / A
- ➡️ Fletxa dreta / D
- ESPAI = Reiniciar

📱 **Móvil:**
- Botones de flexetes a la pantalla

---

## Què puc fer amb la web app instal·lada?

✅ Funciona offline (després de la primera càrrega)
✅ Sense necessitat d'App Store
✅ Sense publicitat
✅ Funciona en qualsevol navegador
✅ Ocupa molt poc espai
✅ Es pot eliminar com qualsevol altra app

---

¡Diverteix-te jugant! 🐸🎮
