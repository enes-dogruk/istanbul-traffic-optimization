import pandas as pd
import numpy as np

# 1. Haversine Mesafe Fonksiyonu (Motorumuz)
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Dünya'nın yarıçapı (km)
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# 2. Statik Fikstür Veritabanı
fixtures_data = [
    # --- GALATASARAY (RAMS Park) ---
    {
        'match_date': '2025-01-04',
        'stadium': 'RAMS',
        'lat': 41.1034,
        'lon': 28.9944,
        'effect_start': '2025-01-04 16:00:00', # Göztepe maçı (19:00)
        'effect_end': '2025-01-04 22:00:00'
    },
    {
        'match_date': '2025-01-08',
        'stadium': 'RAMS',
        'lat': 41.1034,
        'lon': 28.9944,
        'effect_start': '2025-01-08 17:30:00', # Başakşehir Kupa maçı (20:30)
        'effect_end': '2025-01-08 23:30:00'
    },
    {
        'match_date': '2025-01-21',
        'stadium': 'RAMS',
        'lat': 41.1034,
        'lon': 28.9944,
        'effect_start': '2025-01-21 15:30:00', # Dinamo Kiev maçı (18:30)
        'effect_end': '2025-01-21 21:30:00'
    },
    {
        'match_date': '2025-01-25',
        'stadium': 'RAMS',
        'lat': 41.1034,
        'lon': 28.9944,
        'effect_start': '2025-01-25 16:00:00', # Konyaspor maçı (19:00)
        'effect_end': '2025-01-25 22:00:00'
    },
    
    # --- FENERBAHÇE (Şükrü Saracoğlu) ---
    {
        'match_date': '2025-01-05',
        'stadium': 'SARACOGLU',
        'lat': 40.9876,
        'lon': 29.0369,
        'effect_start': '2025-01-05 16:00:00', # Hatayspor maçı (19:00)
        'effect_end': '2025-01-05 22:00:00'
    },
    {
        'match_date': '2025-01-23',
        'stadium': 'SARACOGLU',
        'lat': 40.9876,
        'lon': 29.0369,
        'effect_start': '2025-01-23 17:45:00', # Lyon maçı (20:45)
        'effect_end': '2025-01-23 23:45:00'
    },
    {
        'match_date': '2025-01-26',
        'stadium': 'SARACOGLU',
        'lat': 40.9876,
        'lon': 29.0369,
        'effect_start': '2025-01-26 16:00:00', # Göztepe maçı (19:00)
        'effect_end': '2025-01-26 22:00:00'
    },
    
    # --- BEŞİKTAŞ (Tüpraş Stadyumu) ---
    {
        'match_date': '2025-01-11',
        'stadium': 'TUPRAS',
        'lat': 41.0395,
        'lon': 28.9940,
        'effect_start': '2025-01-11 16:00:00', # Bodrum FK maçı (19:00)
        'effect_end': '2025-01-11 22:00:00'
    },
    {
        'match_date': '2025-01-18',
        'stadium': 'TUPRAS',
        'lat': 41.0395,
        'lon': 28.9940,
        'effect_start': '2025-01-18 16:00:00', # Samsunspor maçı (19:00)
        'effect_end': '2025-01-18 22:00:00'
    },
    {
        'match_date': '2025-01-22',
        'stadium': 'TUPRAS',
        'lat': 41.0395,
        'lon': 28.9940,
        'effect_start': '2025-01-22 15:30:00', # Athletic Bilbao maçı (18:30)
        'effect_end': '2025-01-22 21:30:00'
    }
]

df_fixtures = pd.DataFrame(fixtures_data)
df_fixtures['match_date'] = pd.to_datetime(df_fixtures['match_date']).dt.date
df_fixtures['effect_start'] = pd.to_datetime(df_fixtures['effect_start'])
df_fixtures['effect_end'] = pd.to_datetime(df_fixtures['effect_end'])