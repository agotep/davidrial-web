import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://imginn.com/'
}

# URLs de miniaturas extraídas del HTML de los reels
thumbnails = {
    # Reel "Descubre David Rial en 10 segundos" - miniatura con cara del dueño
    'david_owner': 'https://s6.imginn.com/503829725_9855941301160661_1851036794394226527_n.jpg?t51.71878-15/503829725_9855941301160661_1851036794394226527_n.jpg?stp=dst-jpg_e35_p720x720_sh2.08_tt6&_nc_cat=101&ig_cache_key=MzYzNjI5MDYzMzU4MzgxMTM2Mg%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=YxXCfNlJKBsQ7kNvwH0JNVZ&_nc_oc=AdqWJpQtGYwQJHlqxWxT8YbdNJGJNWlCnJJjhGFBJJKkuDzHXiCHFWBjkMBECJRFJPE&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_gid=DpOakEAGy8Vp1adZl_GdOw&_nc_ss=7a22e&oh=00_Af8ORdSQcuHjJvTDhZsRMzTqjkPjuQcMFWjJqkWXMuqCdQ&oe=6A30B5B3',
    # Reel "Magia en accion" - peinado de boda
    'boda_recogido': 'https://s6.imginn.com/503351316_1049474996608978_8643902792268160281_n.jpg?t51.71878-15/503351316_1049474996608978_8643902792268160281_n.jpg?stp=dst-jpg_e15_p320x320_tt6&_nc_cat=107&ig_cache_key=MzYzNjI2MzI0NTg5NzY4OTEwMQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjMyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=4Ozi7x68XyYQ7kNvwEfeg0k&_nc_oc=AdrjHSJDyUVkFjCFrJgkOvFUGmjGbLBXm1bPPGdX5oBr2nBmXjFiSCcFSl7lFSCuCl4&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_gid=ROjEATUpgaWbWwM6YiTGiQ&_nc_ss=7a22e&oh=00_Af-XYjz8iTfAZHhVCBhAP4GZGowNW_wCbOiQbicSW7YpxQ&oe=6A2C8085',
    # Reel "Cambios de look Antes y Después"
    'antes_despues': 'https://s6.imginn.com/477091712_611273081656602_6153161545000504965_n.jpg?t51.71878-15/477091712_611273081656602_6153161545000504965_n.jpg?stp=dst-jpg_e15_p320x320_tt6&_nc_cat=103&ig_cache_key=MzU3MDU3MDg1NzA5OTk2NzA0Mw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjMyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=nhHeD0sZWyMQ7kNvwEPkiNv&_nc_oc=AdpnkG0lmg7Io1VGNysnQYpSoUKONsDUp2nSlvGfZ03iFEJHOU0spxm8iS6hMzF0DlvYC0kdQTHdc9yJPdFvm8_x&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-atl3-2.cdninstagram.com&_nc_gid=DpOakEAGy8Vp1adZl_GdOw&_nc_ss=7a22e&oh=00_Af9wvdxECs88fyPc_qQYBWA58UThmMrnv5nOWRI08Htv5A&oe=6A3063FE',
    # Reel "Pixie con rizos"
    'pixie_rizos': 'https://s6.imginn.com/471889933_18464999926071622_1435733223015210305_n.jpg?t51.75761-15/471889933_18464999926071622_1435733223015210305_n.jpg?stp=dst-jpg_e15_p480x480_tt6&_nc_cat=102&ig_cache_key=MzU3NzE0NDE3MjExMzY2NzA0OTE3ODU5MTM3OTg4MzY1OTUy.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjQ4MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=2LTnbs-1hXQQ7kNvwEp5qmL&_nc_oc=AdoRJVKj8-VVe9xgrYsQ3RIsLSn9ZRsuG7EFlnXwwkGriQObOmD1ihfNfSh7zJflKvnQ_QecwlY0CHGUZbA1UCSu&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-atl3-2.cdninstagram.com&_nc_gid=DpOakEAGy8Vp1adZl_GdOw&_nc_ss=7a22e&oh=00_Af_giw0lBtueuB-zccG8LpJ8AxciiCKj3MUQyB7PgZSRXQ&oe=6A30447E',
    # Reel "Melena" - chica de espaldas con melena larga castaña
    'melena_larga': 'https://s6.imginn.com/470913396_18465001873071622_5070304064271975497_n.jpg?t51.75761-15/470913396_18465001873071622_5070304064271975497_n.jpg?stp=dst-jpg_e15_p240x240_tt6&_nc_cat=101&ig_cache_key=MzU3NzE0NDE3MjExMzY2NzA0OTE3ODU5MTM3OTg4MzY1OTUy.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjI0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=2LTnbs-1hXQQ7kNvwEp5qmL&_nc_oc=AdoRJVKj8-VVe9xgrYsQ3RIsLSn9ZRsuG7EFlnXwwkGriQObOmD1ihfNfSh7zJflKvnQ_QecwlY0CHGUZbA1UCSu&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-atl3-2.cdninstagram.com&_nc_gid=DpOakEAGy8Vp1adZl_GdOw&_nc_ss=7a22e&oh=00_Af_giw0lBtueuB-zccG8LpJ8AxciiCKj3MUQyB7PgZSRXQ&oe=6A30447E',
}

os.makedirs('/home/ubuntu/davidrial/assets/real', exist_ok=True)

for name, url in thumbnails.items():
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 5000:
            path = f'/home/ubuntu/davidrial/assets/real/{name}.jpg'
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"✅ {name}: {len(r.content)} bytes -> {path}")
        else:
            print(f"❌ {name}: status {r.status_code}, size {len(r.content)}")
    except Exception as e:
        print(f"❌ {name}: {e}")
