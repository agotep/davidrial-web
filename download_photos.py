import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://imginn.com/',
}

# URLs de las mejores fotos de trabajos de peluquería (excluyendo productos, bodas de terceros, etc.)
# Selección manual de las más profesionales y representativas del trabajo del salón
photos = {
    # Foto 2: imagen limpia sin texto (trabajo de cabello)
    'insta_01.webp': 'https://s6.imginn.com/657323360_18552634237071622_3205096238199948799_n.webp?t51.82787-15/657323360_18552634237071622_3205096238199948799_n.webp?stp=dst-webp_p828x828&_nc_cat=102&ig_cache_key=Mzg2MDg1MjMwNjA3ODY4MzYyOA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=dm-Ua9-HxX8Q7kNvwGH7fFi&_nc_oc=AdrzXx7rcN-A5q_22vacsHWoihWJ6nllLMa3ILExINEXVmQCLb4HIOCku1g8AZWZ0StP7Jf_zEgMFBvviI9SHrfR&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af9sBR0LL4rC_spEFcY7Sc0dseSMSmrUrWdk9Tx_LHT3dg&oe=6A306DC2',
    # Foto 5: trabajo de cabello
    'insta_02.webp': 'https://s6.imginn.com/626288072_18539869171071622_3068385338368787139_n.webp?t51.82787-15/626288072_18539869171071622_3068385338368787139_n.webp?stp=dst-webp_s1290x1290&_nc_cat=104&ig_cache_key=MzgyNTM2MjU5OTMwMzI5MDM5Nw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=rJJT6pzDLVcQ7kNvwHMkHxV&_nc_oc=Adqt6M_gLbhHwmfqBNULFXnPYxjOjpKAH5bXPAEBpxT-vGHC8VzSqYmhNJVp5Wl_Qzq2pMRPnLlbV1qdKqmhEPp&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_Yt_Bj7rDiDNkxoFJXBfpfxNzr9pqNWHNhNJiJKMfxg&oe=6A2FE63B',
    # Foto 6: trabajo de cabello
    'insta_03.webp': 'https://s6.imginn.com/583690248_18525854917071622_3498967546641339056_n.webp?t51.82787-15/583690248_18525854917071622_3498967546641339056_n.webp?stp=dst-webp_s1290x1290&_nc_cat=105&ig_cache_key=Mzc3MDQ3MjI5MDYyNTM3OTM1Mg%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=yqJzuPVIjxAQ7kNvwGqKQ6i&_nc_oc=AdqCBMbNFmcHDFaHCvFJPgQlQhDDXrJLXgXy0b7qqnuVhXGhU5dJoiCBPpBNNqQJFVW3yzMQVOHhvpIzjFJoJVJ&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_4Gd0wWXrxHFGdHEDGLaYmJLlgXiC6tZJRBR6DqJMnw&oe=6A2FE5C3',
    # Foto 7: trabajo de cabello
    'insta_04.webp': 'https://s6.imginn.com/561628295_18515986915071622_3868659346712750683_n.webp?t51.82787-15/561628295_18515986915071622_3868659346712750683_n.webp?stp=dst-webp_s1290x1290&_nc_cat=105&ig_cache_key=MzczODM2NjUyMjQ3NTcwNjQ2Mg%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=oCJHxAFEUuEQ7kNvwEQ6Ld4&_nc_oc=AdqkMFdGl1GYXnBDKcnMHFSqRCXGgkqWiRnLR0mZdBDKV5FGFmqXSBqKHVjFRhUXJHt5KHJJiXGBPkRMjHnxWXz&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_Yt_Bj7rDiDNkxoFJXBfpfxNzr9pqNWHNhNJiJKMfxg&oe=6A2FE63B',
    # Foto 8: trabajo de cabello
    'insta_05.webp': 'https://s6.imginn.com/527156752_18503961769071622_5483928027993853033_n.webp?t51.82787-15/527156752_18503961769071622_5483928027993853033_n.webp?stp=dst-webp_s1290x1290&_nc_cat=106&ig_cache_key=MzY5MDYyNjY0MzQ5ODIwMzUxMQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=OFQBOCkqJMUQ7kNvwHKJbHR&_nc_oc=AdqzFJHjLkxXTz7kGxFHXWvXHlVCKqFHJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqk&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_Yt_Bj7rDiDNkxoFJXBfpfxNzr9pqNWHNhNJiJKMfxg&oe=6A2FE63B',
    # Foto 10: trabajo de cabello
    'insta_06.webp': 'https://s6.imginn.com/518183979_18500323861071622_2420554488240114730_n.webp?t51.82787-15/518183979_18500323861071622_2420554488240114730_n.webp?stp=dst-webp_s1290x1290&_nc_cat=108&ig_cache_key=MzY3NTQxMTcyMjM5NzI4NjA4MA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=OFQBOCkqJMUQ7kNvwHKJbHR&_nc_oc=AdqzFJHjLkxXTz7kGxFHXWvXHlVCKqFHJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqk&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_Yt_Bj7rDiDNkxoFJXBfpfxNzr9pqNWHNhNJiJKMfxg&oe=6A2FE63B',
    # Foto 12: trabajo de cabello
    'insta_07.webp': 'https://s6.imginn.com/503756088_18493651924071622_2032719952160455202_n.webp?t51.75761-15/503756088_18493651924071622_2032719952160455202_n.webp?stp=dst-webp_s1290x1290&_nc_cat=105&ig_cache_key=MzY0NzI2NzI3NjYwMTYyMzA3Ng%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkZFRUQueHBpZHMuMTEyNS5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=OFQBOCkqJMUQ7kNvwHKJbHR&_nc_oc=AdqzFJHjLkxXTz7kGxFHXWvXHlVCKqFHJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqkFJHkJGGkKBJbHlvXJHqk&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-lga3-3.cdninstagram.com&_nc_gid=ownlg_Rc4X3BTGAobEJw3A&_nc_ss=7a22e&oh=00_Af_Yt_Bj7rDiDNkxoFJXBfpfxNzr9pqNWHNhNJiJKMfxg&oe=6A2FE63B',
}

os.makedirs('/home/ubuntu/davidrial/assets', exist_ok=True)

for filename, url in photos.items():
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            path = f'/home/ubuntu/davidrial/assets/{filename}'
            with open(path, 'wb') as f:
                f.write(r.content)
            size = len(r.content)
            print(f'✓ {filename} — {size//1024}KB')
        else:
            print(f'✗ {filename} — HTTP {r.status_code}')
    except Exception as e:
        print(f'✗ {filename} — Error: {e}')

print('Descarga completada')
