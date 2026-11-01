ElectroLab Suite: οδηγίες εγκατάστασης ως εφαρμογή κινητού

1) Εγκατάσταση ως PWA (Android και iPhone, χωρίς κατάστημα εφαρμογών)
   - Ανέβασε ΟΛΟΚΛΗΡΟ τον φάκελο σε δωρεάν HTTPS hosting (Netlify Drop, GitHub Pages ή Cloudflare Pages).
   - Άνοιξε τη διεύθυνση από το κινητό.
   - Android (Chrome): μενού ⋮ → «Εγκατάσταση εφαρμογής».
   - iPhone (Safari): Κοινοποίηση → «Προσθήκη στην αρχική οθόνη».
   - Μετά την πρώτη φόρτωση με internet, η εφαρμογή ανοίγει και χωρίς σύνδεση (cache).

2) APK για Android (για Play Store ή απευθείας εγκατάσταση)
   - Εύκολος τρόπος: μπες στο pwabuilder.com, γράψε τη διεύθυνση του hosting και διάλεξε Android.
   - Εναλλακτικά με Capacitor: βάλε τα αρχεία σε φάκελο www και τρέξε
       npm i @capacitor/core @capacitor/cli @capacitor/android
       npx cap init ElectroLab gr.electrolab.app --web-dir www
       npx cap add android
       npx cap open android   (Build → Build APK στο Android Studio)

3) iOS (App Store): χρειάζεται Mac με Xcode και λογαριασμό Apple Developer.
   Ίδια διαδικασία με Capacitor (@capacitor/ios).

Σημείωση: το Three.js και το Chart.js φορτώνονται από CDN. Για εφαρμογή που δουλεύει offline από την πρώτη εκτέλεση,
κατέβασε τα δύο αρχεία στον φάκελο και άλλαξε τα src στο index.html.
