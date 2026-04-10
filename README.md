# 🧭 İBB Akıllı Trafik Modeli ve Dinamik Rota Optimizasyonu

Bu proje, İstanbul Büyükşehir Belediyesi (İBB) Açık Veri Portalı'ndan elde edilen 1.6 Milyon satırlık trafik yoğunluk verisi kullanılarak geliştirilmiş, makine öğrenmesi (Random Forest) tabanlı proaktif bir rota optimizasyon motorudur. 

Geleneksel, reaktif navigasyon sistemlerinin aksine; bu motor zamanın döngüsel doğasını (Cyclical Time) ve stadyum bölgelerindeki maç saati yoğunlukları (Haversine Formülü ile) gibi bölgesel anomalileri önceden hesaplayarak OSRM algoritmasına dinamik ağırlıklar atar.

## 🚀 Kullanılan Teknolojiler
* **Makine Öğrenmesi:** Scikit-Learn (Hiperparametreleri optimize edilmiş Random Forest)
* **Veri İşleme:** Pandas, Numpy
* **Haritalama & Yönlendirme:** Folium, OSRM API, Polyline
* **Kullanıcı Arayüzü (UI):** Streamlit (Glassmorphism Tasarım)

---

## 🛠️ Ekip İçin Kurulum ve Çalıştırma Rehberi

GitHub dosya sınırı (100MB) nedeniyle projenin eğitilmiş model ağırlıkları (~800 MB) bu repoda tutulmamaktadır. Sistemin takım arkadaşlarınızın bilgisayarında (localhost) sorunsuz çalışması için aşağıdaki adımları sırasıyla uygulayın:

### Adım 1: Projeyi Bilgisayarınıza Çekin
Terminali açın ve projeyi klonlayın:
`git clone https://github.com/enes-dogruk/istanbul-traffic-optimization.git`
`cd istanbul-traffic-optimization`

### Adım 2: Sanal Ortam (Virtual Environment) Kurun
Kütüphane çakışmalarını önlemek için projeye izole bir ortam kurun ve aktif edin:
* **Windows:** `python -m venv venv` ve ardından `venv\Scripts\activate`
* **Mac/Linux:** `python3 -m venv venv` ve ardından `source venv/bin/activate`

### Adım 3: Bağımlılıkları Yükleyin
Projenin ihtiyaç duyduğu tüm kütüphaneleri tek seferde kurun:
`pip install -r requirements.txt`

### Adım 4: Yapay Zeka Modellerini İndirin (KRİTİK ADIM)
Aşağıdaki linklerden projenin beyni olan iki dosyayı indirin ve projenin **ana klasörünün içine** (`app.py` ile aynı dizine) atın:
1. `istanbul_traffic_rf_model.pkl` -> https://drive.google.com/file/d/1wgFkBU-YIWk8P0I8asGnl0EJT5VCuKFy/view?usp=sharing
2. `traffic_scaler.pkl` -> https://drive.google.com/file/d/1M6anPSN7oJYRblBtTREAKiI7FDacYG3x/view?usp=sharing

### Adım 5: Sistemi Başlatın
Her şey hazır. Arayüzü başlatmak için terminale şunu yazın:
`streamlit run app.py`

Tarayıcınızda otomatik olarak `localhost:8501` açılacak ve sistem çalışacaktır.

Proje Linki : https://github.com/enes-dogruk/istanbul-traffic-optimization
