# 🚀 Solution Ultra-Rapide : ngrok (5 minutes)

Si vous voulez partager votre dashboard **immédiatement** sans créer de compte GitHub, utilisez **ngrok**.

## Étapes (5 minutes)

### 1️⃣ Télécharger ngrok (1 minute)

1. Allez sur [ngrok.com/download](https://ngrok.com/download)
2. Téléchargez la version Windows
3. Extrayez l'archive où vous voulez (ex: `C:\ngrok\`)

### 2️⃣ Créer un compte ngrok (2 minutes)

1. Allez sur [ngrok.com](https://ngrok.com)
2. Cliquez sur "Sign up" (gratuit)
3. Entrez votre email
4. Vérifiez votre email
5. Notez votre **authtoken** (vous le trouverez sur le dashboard)

### 3️⃣ Configurer ngrok (1 minute)

Ouvrez PowerShell ou Invite de commandes et exécutez :

```bash
# Aller dans le dossier ngrok
cd C:\ngrok

# Configurer votre token (remplacez VOTRE_TOKEN)
.\ngrok.exe authtoken VOTRE_TOKEN
```

### 4️⃣ Lancer votre application (1 minute)

**Terminal 1** - Lancer Streamlit :
```bash
cd D:\python_work\bob-enquete
python -m streamlit run scripts/app_simulation_interactive.py
```

**Terminal 2** - Lancer ngrok :
```bash
cd C:\ngrok
.\ngrok.exe http 8501
```

### 5️⃣ Partager l'URL ✅

ngrok affichera quelque chose comme :
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8501
```

**Copiez cette URL** (`https://abc123.ngrok.io`) et partagez-la avec vos collègues !

---

## ⚠️ Points Importants

### Limitations ngrok Gratuit

- ✅ URL gratuite mais **change à chaque redémarrage**
- ✅ Limite de **40 connexions par minute**
- ✅ Votre ordinateur doit être **allumé et connecté**
- ✅ Parfait pour **tester et partager temporairement**

### Pour une URL Fixe

Si vous voulez une URL permanente, vous avez deux options :

1. **Plan ngrok payant** (~10$/mois) → URL fixe
2. **Utiliser Railway/Render** (gratuit) → URL permanente

---

## 🎯 Utilisation Quotidienne

Pour utiliser ngrok régulièrement :

1. **Créer un script batch** `lancer_ngrok.bat` :

```batch
@echo off
echo Lancement de Streamlit...
start cmd /k "cd /d D:\python_work\bob-enquete && python -m streamlit run scripts/app_simulation_interactive.py"

timeout /t 5

echo Lancement de ngrok...
start cmd /k "cd /d C:\ngrok && ngrok.exe http 8501"

echo.
echo Application en cours de demarrage...
echo L'URL ngrok sera affichee dans la fenetre ngrok
pause
```

2. **Double-cliquez** sur `lancer_ngrok.bat`
3. **Copiez l'URL** depuis la fenêtre ngrok
4. **Partagez** avec vos collègues

---

## 🔒 Sécurité

- ✅ ngrok utilise HTTPS (sécurisé)
- ✅ Par défaut, l'URL est publique (toute personne avec le lien peut accéder)
- ✅ Pour une URL privée, utilisez le plan payant ou Railway/Render

---

## 📞 Alternative : Créer GitHub (2 minutes)

Si vous préférez une solution permanente :

1. Créez un compte GitHub : [github.com/join](https://github.com/join)
2. Suivez `DEPLOIEMENT_RAPIDE.md`
3. Votre dashboard sera en ligne **permanentement** et gratuitement

---

**Bon partage ! 🚀**


