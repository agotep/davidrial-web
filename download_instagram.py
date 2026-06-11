import requests
from bs4 import BeautifulSoup
import os
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Referer': 'https://imginn.com/',
}

print("Descargando página de imginn...")
r = requests.get('https://imginn.com/davidrialpeluquerias/', headers=headers, timeout=20)
print(f"Status: {r.status_code}, Tamaño: {len(r.text)} chars")

soup = BeautifulSoup(r.text, 'html.parser')

# Guardar HTML para análisis
with open('/home/ubuntu/davidrial/imginn_page.html', 'w') as f:
    f.write(r.text)
print("HTML guardado en imginn_page.html")

# Buscar todos los elementos de post
posts = soup.find_all('div', class_='item')
print(f"Posts encontrados con class=item: {len(posts)}")

# Buscar imágenes directamente
all_imgs = soup.find_all('img')
print(f"Total imágenes en página: {len(all_imgs)}")
for i, img in enumerate(all_imgs):
    src = img.get('src', '')
    alt = img.get('alt', '')[:100]
    if src:
        print(f"  IMG {i}: {alt[:60]} | {src[:150]}")
