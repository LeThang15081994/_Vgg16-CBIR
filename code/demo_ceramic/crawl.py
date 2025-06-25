import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Danh sách các loại gạch và từ khóa tìm kiếm
categories = {
    "Wall_Glazed_Tile": "glazed wall tile",
    "Cement_Tile": "cement tile",
    "Mosaic_Tile": "mosaic tile",
    "Natural_Stone_Tile": "natural stone tile",
    "3D_Decorative_Wall_Tile": "3D decorative wall tile",
    "Rug_Stone_Pattern_Tile": "stone pattern rug tile",
    "Terrazzo_Tile": "terrazzo tile",
    "Wood_Tile": "wood tile",
    "Glass_Decorative_Tile": "glass decorative tile",
    "Paving_Tile": "paving tile"
}

def get_image_links(keyword, max_images=30):
    links = []
    page = 1
    while len(links) < max_images:
        url = f"https://www.flickr.com/search/?text={keyword.replace(' ', '%20')}&page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all("img")
        for img in imgs:
            src = img.get("src")
            # Ưu tiên lấy ảnh có hậu tố _b.jpg (big), _c.jpg (large), _z.jpg (medium 640), _n.jpg (small 320), _m.jpg (small)
            # Nếu src là thumbnail (_m, _n), chuyển sang _b hoặc _c nếu có thể
            if src and "staticflickr.com" in src and src not in links:
                # Tìm và thay hậu tố kích thước
                for size in ["_b.jpg", "_c.jpg", "_z.jpg", "_n.jpg", "_m.jpg"]:
                    if src.endswith(size):
                        # Ưu tiên _b, _c, _z
                        for highres in ["_b.jpg", "_c.jpg", "_z.jpg"]:
                            highres_src = src[:-6] + highres
                            if highres_src not in links:
                                links.append(highres_src)
                                break
                        else:
                            links.append(src)
                        break
                else:
                    links.append(src)
            if len(links) >= max_images:
                break
        page += 1
        time.sleep(1)  # tránh bị chặn
        if not imgs:
            break
    return links

def download_images(links, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    for idx, link in enumerate(tqdm(links)):
        try:
            if link.startswith("//"):
                link = "https:" + link
            img_data = requests.get(link, timeout=10).content
            with open(os.path.join(save_dir, f"{idx}.jpg"), "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Error downloading {link}: {e}")

if __name__ == "__main__":
    for folder, keyword in categories.items():
        print(f"Crawling: {keyword}")
        links = get_image_links(keyword, max_images=1000)
        download_images(links, os.path.join("images_ceramic", folder))