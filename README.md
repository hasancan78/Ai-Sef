# 👨‍🍳 AIŞef - Yapay Zeka Destekli Aşçıbaşı

AIŞef, elinizdeki malzemelere göre yaratıcı tarifler üreten, bu tarifleri favorilerinize eklemenizi, PDF olarak indirmenizi ve sesli (TTS) olarak dinlemenizi sağlayan yeni nesil bir web uygulamasıdır.

## 🌟 Özellikler
* 🧠 **Yapay Zeka Destekli Tarif:** Sadece elinizdeki malzemeleri (örn: tavuk, krema, mantar) yazın, size özel harika tarifler önersin.
* 🗣️ **Sesli Asistan:** Tariflerinizi okurken elleriniz hamurda mı? AIŞef tarifleri sizin için yüksek sesle okur! (Türkçe & İngilizce).
* 🎨 **Tema Seçenekleri:** 🔥 Kızıl Tutku, 🌌 Gece Mavisi, ☀️ Aydınlık ve 💖 Neon Fuşya.
* 💾 **Akıllı Favoriler:** Beğendiğiniz tarifleri tek tıkla kaydedin. Akıllı kategorizasyon sistemi tarifleri "Tatlı", "Kahvaltı", "Akşam Yemeği" gibi sınıflara otomatik ayırır.
* 📄 **PDF Çıktısı:** Kaydettiğiniz veya yeni oluşturduğunuz her tarifi PDF dosyası olarak cihazınıza indirin.
* 📱 **PWA (Telefona Ekle):** Tarayıcı menüsünden "Ana Ekrana Ekle" diyerek mobil uygulama gibi kullanın.

## 🚀 Kurulum & Çalıştırma (Lokal)

Uygulamayı kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Gereksinimleri Yükleyin:**
   `ash
   pip install -r requirements.txt
   `

2. **API Anahtarı:**
   Ana dizinde .env isimli bir dosya oluşturun ve içerisine Google Gemini API anahtarınızı ekleyin:
   `env
   GEMINI_API_KEY="api-anahtariniz-buraya"
   `

3. **Uygulamayı Başlatın:**
   `ash
   streamlit run app.py
   `

## 🛠️ Kullanılan Teknolojiler
* **Streamlit** (Arayüz ve Web Sunucusu)
* **Google Generative AI (Gemini)** (Tarif Üretimi)
* **SQLite** (Favorilerin veritabanı)
* **fpdf2** (PDF Oluşturma)
* **Web Speech API** (Sesli Okuma - TTS)
