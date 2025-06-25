import os
import shutil

# Thư mục nguồn chứa các thư mục con ảnh
SRC_DIR = r"D:/WorkSpace/_thangle15894/_AIproject/_person/_Vgg16-CBIR/code/demo_ceramic/images_ceramic"
# Thư mục đích chứa toàn bộ ảnh đã merge
DEST_DIR = r"D:/WorkSpace/_thangle15894/_AIproject/_person/_Vgg16-CBIR/code/demo_ceramic/images_ceramic"

os.makedirs(DEST_DIR, exist_ok=True)
idx = 0
seen = set()

for root, dirs, files in os.walk(SRC_DIR):
    for file in sorted(files):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            new_name = f"{idx}.jpg"
            # Đảm bảo không trùng tên
            while new_name in seen or os.path.exists(os.path.join(DEST_DIR, new_name)):
                idx += 1
                new_name = f"{idx}.jpg"
            shutil.copy2(os.path.join(root, file), os.path.join(DEST_DIR, new_name))
            seen.add(new_name)
            idx += 1

print(f"Đã chuyển và đánh số lại toàn bộ ảnh vào {DEST_DIR}") 