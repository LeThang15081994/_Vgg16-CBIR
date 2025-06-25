from vectorization import feature_extract
import pickle
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

def vectors_data(data_path):
    vectors = feature_extract()
    model = vectors.get_model_extract()
    vectors.store_vector(model, data_path)

def search_img(img_path, index):
    image = feature_extract()
    model = image.get_model_extract()
    img_search_vector = image.vector_normalized(model, img_path)

    with open("vectors.pkl", "rb") as f:
        vectors = pickle.load(f)
    with open("paths.pkl", "rb") as f:
        paths = pickle.load(f)

    distance = np.linalg.norm(vectors - img_search_vector, axis=1)

    ids = np.argsort(distance)[:index] # get 20 image have nearest image.
    nearest_image = [(paths[id], distance[id]) for id in ids]

    return nearest_image


if __name__ == "__main__":
    #vectors_data('dataset')
    nearest_image = search_img('testimg/wolf2.jpg', 20) # input query image and number of image will show
    
    # show the same image with query image
    axes = []
    grid_size = int(math.ceil(math.sqrt(len(nearest_image))))
    fig = plt.figure(figsize=(10,8))

    for id in range(len(nearest_image)):
        draw_image = nearest_image[id]
        axes.append(fig.add_subplot(grid_size, grid_size, id+1))

        axes[-1].set_title(draw_image[0] + '\n' + str(draw_image[1]))
        plt.imshow(Image.open(draw_image[0]))

    fig.tight_layout()
    plt.show()


