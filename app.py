import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium
import requests
import polyline
import datetime
import os

# --- 1. YARDIMCI FONKSİYONLAR ---
def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def check_match_zone(lat, lon, selected_date, hour):
    match_schedule = {
        datetime.date(2025, 1, 10): (41.1034, 28.9944), 
        datetime.date(2025, 1, 17): (40.9876, 29.0369), 
        datetime.date(2025, 1, 19): (41.0395, 28.9940), 
        datetime.date(2025, 1, 21): (41.1034, 28.9944), 
        datetime.date(2025, 1, 25): (40.9876, 29.0369)  
    }
    if selected_date in match_schedule and (16 <= hour <= 23):
        s_lat, s_lon = match_schedule[selected_date]
        if calculate_haversine(lat, lon, s_lat, s_lon) <= 3.0: 
            return 1
    return 0

# --- 2. ASSETS (SESSİZ ÇÖKMEYİ ENGELLEYEN YAPI) ---
@st.cache_resource
def load_assets():
    if not os.path.exists('istanbul_traffic_rf_model.pkl') or not os.path.exists('traffic_scaler.pkl'):
        return None, None
    try:
        model = joblib.load('istanbul_traffic_rf_model.pkl')
        scaler = joblib.load('traffic_scaler.pkl')
        return model, scaler
    except Exception as e: 
        return None, None

model, scaler = load_assets()

# --- 3. UI AYARLARI VE CSS ---
st.set_page_config(page_title="İBB Akıllı Trafik Modeli", layout="wide", page_icon="🧭")

st.markdown("""
    <style>
    .block-container { padding: 1rem 2rem !important; max-width: 100% !important; }
    header, footer, [data-testid="collapsedControl"] { visibility: hidden !important; display: none !important; }
    .stApp { background-color: #0b1120; } 

    [data-testid="column"]:nth-of-type(1) {
        background-color: rgba(43, 65, 94, 0.85);
        backdrop-filter: blur(16px);
        padding: 25px 30px !important;
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2), 0 0 40px rgba(255, 0, 255, 0.1) !important;
        height: calc(100vh - 2rem);
        overflow-y: auto;
    }

    [data-testid="column"]:nth-of-type(1) > div > div > div { gap: 0.8rem !important; } 

    label, .stMarkdown p { 
        color: #FFFFFF !important; font-weight: 800 !important; font-size: 1.15rem !important; 
        margin-bottom: 5px !important; letter-spacing: 0.5px;
    }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: rgba(23, 51, 91, 0.8) !important; 
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 10px !important; height: 3.8rem !important; 
        display: flex !important; align-items: center !important; 
    }
    
    .stDateInput div[data-baseweb="input"] { background-color: transparent !important; }
    div[data-baseweb="select"] *, .stDateInput input {
        color: #FFFFFF !important; font-size: 1.15rem !important; font-weight: bold !important; 
    }
    
    .stDateInput input { text-align: center !important; width: 100% !important; }
    div[data-baseweb="select"] > div > div > div {
        display: flex !important; justify-content: flex-start !important;
        padding-left: 10px !important; width: 100% !important;
    }

    /* --- BUTON SINIRLARI SIFIRLANDI, YAZI DUVARLARA DAYANDI --- */
    .stButton { margin-top: 25px !important; margin-bottom: 15px !important; }
    .stButton>button {
        width: 100% !important; 
        border-radius: 15px !important; 
        height: 80px !important; 
        background-color: #1C2F60 !important;
        color: white !important; 
        font-weight: 950 !important; 
        font-size: 2.85rem !important; /* MAKSİMUM BOYUT */
        padding: 0 !important; /* SAĞ-SOL BOŞLUKLARI YOK ET */
        margin: 0 !important;
        border: 3px solid #00FFFF !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.2) !important; 
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important; /* ALT SATIRA GEÇMEYİ YASAKLA */
        letter-spacing: -0.5px !important; /* Harfleri hafif sıkıştır ki sığsın */
        overflow: hidden !important;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button p {
        width: 100% !important;
        margin: 0 !important; 
        padding: 0 !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 255, 255, 1.0), 0 0 60px rgba(0, 255, 255, 0.6) !important;
        transform: scale(1.02);
        background-color: #1e3a8a !important;
    }

    /* --- SONUÇ KARTLARI VE ALTIN SARISI VURGU --- */
    .route-card {
        padding: 15px !important; border-radius: 15px; color: white; 
        border: 1px solid rgba(0, 255, 255, 0.2); box-shadow: 0 8px 20px rgba(0,0,0,0.6); 
        display: flex; flex-direction: column;
    }
    .best-route { 
        border: 2px solid #FFD700 !important; 
        border-left: 8px solid #FFD700 !important; 
        background-color: #1C2F60;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.4); 
    } 
    .alt-route { background-color: #2B3949; border-left: 8px solid #FF00FF !important; }  
    .route-title { font-size: 1.1rem !important; font-weight: 900; margin-bottom: 8px; }
    .route-time { font-size: 2.0rem !important; font-weight: bold; color: #00FFFF; }
    .best-route .route-time { color: #FFD700 !important; text-shadow: 0 0 10px rgba(255, 215, 0, 0.6) !important; }
    .route-details { font-size: 1.0rem !important; color: #cbd5e1; }

    [data-testid="column"]:nth-of-type(2) { padding-left: 20px; }
    iframe {
        border-radius: 20px !important;
        border: 1px solid rgba(0, 255, 255, 0.15) !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.95);
    }
    hr { margin: 15px 0 !important; border-color: rgba(0, 255, 255, 0.3) !important; }
    [data-testid="column"] [data-testid="column"] { padding-right: 8px !important; padding-left: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'analiz_yapildi' not in st.session_state:
    st.session_state.update({'analiz_yapildi': False, 'map_obj': None, 'route_stats': []})

istanbul_hubs = {
    "Taksim (Meydan)": (41.0360, 28.9850), "Beşiktaş (Meydan)": (41.0422, 29.0077),
    "Beşiktaş Stadyumu (Tüpraş)": (41.0395, 28.9940), "Mecidiyeköy (Meydan)": (41.0660, 28.9920),
    "Levent (Büyükdere Cd.)": (41.0810, 29.0140), "Maslak (Büyükdere Cd.)": (41.1070, 29.0230),
    "Karaköy (İskele)": (41.0220, 28.9760), "Eminönü (İskele)": (41.0150, 28.9730),
    "Bakırköy (İncirli)": (40.9800, 28.8710), "Avcılar (Metrobüs)": (40.9790, 28.7210),
    "Beylikdüzü (Meydan)": (41.0010, 28.6410), "Sarıyer (Merkez)": (41.1680, 29.0550),
    "Rams Park (Seyrantepe)": (41.1034, 28.9944), "Kadıköy (Rıhtım)": (40.9900, 29.0200),
    "Fenerbahçe Stadyumu (Kadıköy)": (40.9876, 29.0369)
}

col_panel, col_map = st.columns([1, 2.2])

with col_panel:
    st.markdown("<h1 style='text-align: center; margin-bottom: 25px; color: white; font-size: 2.6rem;'>📊 Tahmin Paneli</h1>", unsafe_allow_html=True)
    
    if not model or not scaler:
        st.error("🚨 DİKKAT: 'istanbul_traffic_rf_model.pkl' veya 'traffic_scaler.pkl' dosyası klasörde bulunamadı. Lütfen dosyaları app.py ile aynı klasöre koyun.")
    
    col_date, col_time = st.columns(2)
    with col_date:
        # TARİH SEÇİMİ SADECE OCAK 2025'E KİLİTLENDİ
        selected_date = st.date_input("📅 Tarih (Ocak 2025)", 
                                      value=datetime.date(2025, 1, 10),
                                      min_value=datetime.date(2025, 1, 1),
                                      max_value=datetime.date(2025, 1, 31))
    with col_time:
        hour_opts = [f"{h:02d}:00" for h in range(24)]
        selected_hour_str = st.selectbox("⏰ Saat", hour_opts, index=18)
        hour = int(selected_hour_str.split(":")[0])
    
    st.markdown("<br>", unsafe_allow_html=True)
    start_point = st.selectbox("📍 Başlangıç", list(istanbul_hubs.keys()), index=0)
    end_point = st.selectbox("🏁 Varış", list(istanbul_hubs.keys()), index=12)
        
    start_lat, start_lon = istanbul_hubs[start_point]
    end_lat, end_lon = istanbul_hubs[end_point]

    predict_btn = st.button("🚀 Rota Optimizasyonunu Başlat", use_container_width=True)

    if st.session_state.analiz_yapildi and st.session_state.route_stats:
        st.markdown("<hr>", unsafe_allow_html=True)
        best_s = max(r['avg_speed'] for r in st.session_state.route_stats)
        sorted_results = sorted(st.session_state.route_stats, key=lambda x: x['avg_speed'], reverse=True)[:2]
        
        card_cols = st.columns(2)
        for idx, res in enumerate(sorted_results):
            est_min = int((res['dist'] / res['avg_speed']) * 60) if res['avg_speed'] > 0 else 0
            is_best = res['avg_speed'] == best_s
            card_class = "best-route" if is_best else "alt-route"
            title = "🏆 EN HIZLI" if is_best else "⚪ ALTERNATİF"
            
            with card_cols[idx]:
                st.markdown(f"""
                    <div class="route-card {card_class}">
                        <div class="route-title">{title}</div>
                        <div class="route-time">⏱️ ~{est_min} DK</div>
                        <div class="route-details">🚀 {res['avg_speed']:.1f} km/h <br> 📏 {res['dist']:.1f} km</div>
                    </div>
                """, unsafe_allow_html=True)

with col_map:
    if predict_btn and model and scaler:
        with st.spinner('Analiz yapılıyor...'):
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=polyline&alternatives=3"
            try:
                r = requests.get(osrm_url).json()
                if r.get('code') == 'Ok':
                    map_tiles = 'CartoDB dark_matter' if (hour >= 18 or hour <= 7) else 'CartoDB positron'
                    m = folium.Map(location=[(start_lat+end_lat)/2, (start_lon+end_lon)/2], zoom_start=12, tiles=map_tiles)
                    
                    route_results = []
                    day_of_week = selected_date.weekday()
                    is_weekend = 1 if day_of_week >= 5 else 0
                    is_holiday = 1 if selected_date.day == 1 else 0
                    is_semester = 1 if (20 <= selected_date.day <= 31) else 0
                    h_sin, h_cos = np.sin(2*np.pi*hour/24), np.cos(2*np.pi*hour/24)

                    for r_idx, route in enumerate(r['routes']):
                        coords = polyline.decode(route['geometry'])
                        num_samples = 15
                        sample_indices = np.linspace(0, len(coords)-1, num_samples, dtype=int)
                        preds = []
                        for s_idx in sample_indices:
                            pt_l, pt_lo = coords[s_idx]
                            is_m = check_match_zone(pt_l, pt_lo, selected_date, hour)
                            df_in = pd.DataFrame([[pt_l, pt_lo, 150, hour, h_sin, h_cos, day_of_week, is_weekend, is_holiday, is_semester, is_m]], 
                                                 columns=['LATITUDE', 'LONGITUDE', 'NUMBER_OF_VEHICLES', 'hour', 'hour_sin', 'hour_cos', 'day_of_week', 'is_weekend', 'is_holiday', 'is_semester', 'is_match_zone'])
                            raw_speed = model.predict(scaler.transform(df_in))[0]
                            if is_m == 1: raw_speed = raw_speed * 0.55
                            preds.append(raw_speed)
                        route_results.append({'index': r_idx, 'coords': coords, 'avg_speed': np.mean(preds), 'dist': route['distance']/1000})

                    best_route = max(route_results, key=lambda x: x['avg_speed'])
                    for res in route_results:
                        is_best = (res['index'] == best_route['index'])
                        coords = res['coords']
                        if not is_best:
                            folium.PolyLine(coords, color="#9ca3af", weight=4, opacity=0.4, dash_array='10, 10').add_to(m)
                        else:
                            num_segments = min(20, len(coords)-1)
                            pts_per_seg = len(coords) // num_segments
                            for i in range(num_segments):
                                s_idx = i * pts_per_seg
                                e_idx = (i + 1) * pts_per_seg if i < num_segments - 1 else len(coords)
                                seg_coords = coords[s_idx:min(e_idx+1, len(coords))]
                                if len(seg_coords) < 2: continue
                                mid_pt = coords[(s_idx + e_idx) // 2]
                                is_m = check_match_zone(mid_pt[0], mid_pt[1], selected_date, hour)
                                df_seg = pd.DataFrame([[mid_pt[0], mid_pt[1], 150, hour, h_sin, h_cos, day_of_week, is_weekend, is_holiday, is_semester, is_m]], 
                                                     columns=['LATITUDE', 'LONGITUDE', 'NUMBER_OF_VEHICLES', 'hour', 'hour_sin', 'hour_cos', 'day_of_week', 'is_weekend', 'is_holiday', 'is_semester', 'is_match_zone'])
                                raw_speed = model.predict(scaler.transform(df_seg))[0]
                                if is_m == 1: seg_speed = raw_speed * 0.55
                                else: seg_speed = raw_speed
                                s_color = '#FF0000' if seg_speed < 24 else ('#FFD700' if seg_speed < 40 else '#00FF00')
                                folium.PolyLine(seg_coords, color="black", weight=10, opacity=0.6).add_to(m)
                                folium.PolyLine(seg_coords, color=s_color, weight=6, opacity=1.0).add_to(m)

                    folium.Marker([start_lat, start_lon], icon=folium.Icon(color='blue', icon='play')).add_to(m)
                    folium.Marker([end_lat, end_lon], icon=folium.Icon(color='red', icon='flag')).add_to(m)
                    st.session_state.update({'map_obj': m, 'route_stats': route_results, 'analiz_yapildi': True})
                    st.rerun() 
            except Exception as e: st.error(f"OSRM/Harita Hatası: {e}")

    if st.session_state.analiz_yapildi and st.session_state.map_obj:
        st_folium(st.session_state.map_obj, width="100%", height=850, key="ist_final_map", returned_objects=[])
    else:
        st_folium(folium.Map(location=[41.0082, 28.9784], zoom_start=11, tiles='CartoDB dark_matter'), width="100%", height=850)