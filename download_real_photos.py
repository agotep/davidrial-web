import requests
import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
save_dir = '/home/ubuntu/davidrial/assets/real'
os.makedirs(save_dir, exist_ok=True)

# URLs de imágenes reales extraídas del perfil de imginn (excluyendo foto de perfil y videos)
# Estas son las imágenes de los posts visibles en el perfil
img_urls = [
    # Post 3 meses - mujer pelo gris/rubio (anuncio captación - skip)
    # Post 7 meses - corte masculino moderno con degradado - BUENA
    "https://s6.imginn.com/652767945_18550190398071622_1863752595731869180_n.webp",
    # Post boda - recogido - BUENA  
    "https://s6.imginn.com/635252722_18002204261894203_8511745844214392595_n.webp",
]

# Posts a analizar para extraer más fotos de carruseles
post_urls = [
    "https://imginn.com/p/DV_kXBYCu-h/",   # post sin descripción
    "https://imginn.com/p/DU0PMnpDD-F/",   # post sin descripción
    "https://imginn.com/p/DUYQdhWipaS/",   # post sin descripción
    "https://imginn.com/p/DRR_mKiDO_G/",   # post sin descripción
    "https://imginn.com/p/DPhVW4DDauH/",   # post sin descripción
    "https://imginn.com/p/DM2YBOmsvg4/",   # post sin descripción
    "https://imginn.com/p/DMKuIEHNfwE/",   # post sin descripción
    "https://imginn.com/p/DMAhEUUMSwI/",   # post sin descripción
    "https://imginn.com/p/DMAMFZrs0_O/",   # post sin descripción
    "https://imginn.com/p/DKeCaxGslsZ/",   # post sin descripción
]

from bs4 import BeautifulSoup

all_img_urls = list(img_urls)

for post_url in post_urls:
    print(f"\nAnalizando: {post_url}")
    try:
        r = requests.get(post_url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Buscar imágenes en el post
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src and ('imginn.com' in src or 'cdninstagram' in src or 'scontent' in src):
                if 'profile' not in src.lower() and 'lazy' not in src.lower():
                    if src not in all_img_urls:
                        all_img_urls.append(src)
                        print(f"  + {src[:100]}...")
        
        # Buscar en data-src
        for el in soup.find_all(attrs={'data-src': True}):
            src = el['data-src']
            if src and src not in all_img_urls:
                all_img_urls.append(src)
                print(f"  + (data-src) {src[:100]}...")
        
        time.sleep(0.8)
    except Exception as e:
        print(f"  Error: {e}")

print(f"\nTotal URLs encontradas: {len(all_img_urls)}")

# Descargar todas las imágenes
downloaded = []
for i, url in enumerate(all_img_urls):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200 and len(r.content) > 10000:
            ext = 'webp' if 'webp' in url.lower() else 'jpg'
            fname = f'real_{i+1:02d}.{ext}'
            fpath = os.path.join(save_dir, fname)
            with open(fpath, 'wb') as f:
                f.write(r.content)
            downloaded.append(fpath)
            print(f"OK: {fname} ({len(r.content)//1024}KB)")
        else:
            print(f"Skip: status={r.status_code}, size={len(r.content)}")
    except Exception as e:
        print(f"Error: {e}")

print(f"\nDescargadas: {len(downloaded)}")
for d in downloaded:
    print(f"  {d}")
