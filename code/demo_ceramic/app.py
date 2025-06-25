import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os
import math
from vgg19 import search_img

st.title("Ceramic Tile Image Search")

# Đường dẫn gốc chứa ảnh
IMAGE_ROOT = r"D:/WorkSpace/_thangle15894/_AIproject/_person/_Vgg16-CBIR/code/demo_ceramic/images_ceramic"

# Sidebar: upload image and select number of results
st.sidebar.header("Query Settings")
query_img = st.sidebar.file_uploader("Upload a query image", type=["jpg", "jpeg", "png"])
num_results = st.sidebar.slider("Number of results", min_value=1, max_value=30, value=12)

if query_img is not None:
    # Save uploaded image to a temp file
    temp_query_path = "temp_query.jpg"
    with open(temp_query_path, "wb") as f:
        f.write(query_img.read())
    st.image(temp_query_path, caption="Query Image", use_container_width=True)

    # Search for similar images
    with st.spinner("Searching for similar images..."):
        results = search_img(temp_query_path, num_results)

    st.success(f"Top {num_results} similar images:")
    grid_size = int(math.ceil(math.sqrt(len(results))))
    cols = st.columns(grid_size)
    for idx, (img_path, dist) in enumerate(results):
        col = cols[idx % grid_size]
        with col:
            # Nếu img_path là đường dẫn tương đối, nối với IMAGE_ROOT
            if not os.path.isabs(img_path):
                img_path_full = os.path.join(IMAGE_ROOT, os.path.basename(img_path))
            else:
                img_path_full = img_path
            st.image(img_path_full, caption=f"{os.path.basename(img_path)}\nDist: {dist:.4f}", use_container_width=True)
else:
    st.info("Please upload a query image to start searching.") 