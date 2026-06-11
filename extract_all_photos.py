import requests
from bs4 import BeautifulSoup
import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
save_dir = '/home/ubuntu/davidrial/assets/real'
os.makedirs(save_dir, exist_ok=True)

# Primero obtener todos los posts del perfil
print("Obteniendo posts del perfil...")
r = requests.get('https://imginn.com/davidrialpeluquerias/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# Extraer URLs de imágenes del perfil y links a posts individuales
post_links = []
img_urls = []

# Buscar todas las imágenes de posts
for item in soup.find_all('div', class_='item'):
    # Link al post
    a = item.find('a', href=True)
    if a and '/p/' in a['href']:
        post_links.append('https://imginn.com' + a['href'] if a['href'].startswith('/') else a['href'])
    # Imagen del post
    img = item.find('img')
    if img and img.get('src'):
        img_urls.append(img['src'])

print(f"Posts encontrados: {len(post_links)}")
print(f"Imágenes en perfil: {len(img_urls)}")

# Si no encontramos con class item, buscar de otra forma
if not post_links:
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/p/' in href:
            full = 'https://imginn.com' + href if href.startswith('/') else href
            if full not in post_links:
                post_links.append(full)
    print(f"Posts encontrados (método 2): {len(post_links)}")

# Posts de carrusel conocidos (con múltiples fotos) - los que tienen icono de carrusel
# Basado en lo que vimos en el perfil
carousel_posts = [
    'https://imginn.com/p/DWUgLd6EVHs/',  # 3 meses - foto mujer pelo gris/rubio
    'https://imginn.com/p/DF3LhXfs8Cc/',  # cambios antes/después
    'https://imginn.com/p/DGkkawJMaPp/',  # descubre David Rial
]

# Descargar imágenes directas del perfil que sean fotos (no videos)
# Usar las URLs de imginn que ya vimos
profile_img_urls = [
    # Foto mujer pelo gris/rubio (3 meses) - muy profesional
    'https://s6.imginn.com/657323360_18552634237071622_3205096238199948799_n.webp',
    # Corte masculino moderno (7 meses)  
    # Boda (4 meses)
]

# Entrar en cada post del carrusel para obtener todas las fotos
all_photo_urls = []

for post_url in carousel_posts[:5]:
    print(f"\nAnalizando post: {post_url}")
    try:
        r2 = requests.get(post_url, headers=headers, timeout=10)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        
        # Buscar todas las imágenes del post
        imgs = soup2.find_all('img')
        for img in imgs:
            src = img.get('src', '')
            if 'imginn.com' in src or 'cdninstagram.com' in src or 'scontent' in src:
                if src not in all_photo_urls and 'profile' not in src.lower():
                    all_photo_urls.append(src)
                    print(f"  Imagen: {src[:80]}...")
        
        # También buscar en los swiper slides
        slides = soup2.find_all('div', class_='swiper-slide')
        for slide in slides:
            img = slide.find('img')
            if img and img.get('src'):
                src = img['src']
                if src not in all_photo_urls:
                    all_photo_urls.append(src)
                    print(f"  Slide: {src[:80]}...")
        
        time.sleep(1)
    except Exception as e:
        print(f"  Error: {e}")

print(f"\nTotal fotos encontradas en carruseles: {len(all_photo_urls)}")

# Descargar las fotos
downloaded = []
for i, url in enumerate(all_photo_urls[:10]):
    try:
        r3 = requests.get(url, headers=headers, timeout=15)
        if r3.status_code == 200 and len(r3.content) > 5000:
            ext = 'webp' if 'webp' in url else 'jpg'
            fname = f'carousel_{i+1:02d}.{ext}'
            fpath = os.path.join(save_dir, fname)
            with open(fpath, 'wb') as f:
                f.write(r3.content)
            downloaded.append(fpath)
            print(f"Descargada: {fname} ({len(r3.content)//1024}KB)")
    except Exception as e:
        print(f"Error descargando {url[:60]}: {e}")

print(f"\nTotal descargadas: {len(downloaded)}")
for d in downloaded:
    print(f"  {d}")
