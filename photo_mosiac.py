import os
from PIL import Image
import numpy as np

class Mosiac(object):
    """docstring for Mosiac."""

    def __init__(self, grid_size):
        self.target_img = None
        self.grid_size = grid_size # size of the grid
        self.tile_dim = () # dimension of each tile
        self.tile_folder = [] # each tile image is stored here
        self.split_imgs = [] # image after splitting is stored here
        self.tile_avg = [] # avg value of all tile Images
        self.split_avg = [] # avg value of all splitted images
        self.index_list = [] # index of tile image closest to the splitted image

    def getavg_RGB(self, image):
        """Function to get avg rgb values of a image"""
        img = np.array(image)
        w, h, d = img.shape
        return tuple(np.average(img.reshape(w*h, d), axis=0))

    def get_dist(self, d1, d2):
        """Function to get dist between two rgb values"""
        dist = ((d1[0] - d2[0]) ** 2 +
                (d1[1] - d2[1]) ** 2 +
                (d1[2] - d2[2]) ** 2)
        return dist

    def load_images(self, location, dir):
        """Function to load the target and tile images"""
        # loading the target images
        self.target_img = Image.open(location)

        # calculating the dimensions for each tile
        width, height = self.target_img.size[0], self.target_img.size[1]
        m, n = self.grid_size
        w, h = int(width / n), int(height / m)
        self.tile_dim = (w, h)

        # loading the tile images
        files = os.listdir(dir)
        for file in files:
            file_path = os.path.abspath(os.path.join(dir, file))
            with open(file_path, 'rb') as fi:
                img = Image.open(fi)
                img.load()
                img.thumbnail(self.tile_dim)
                self.tile_folder.append(img)

    def split_target(self):
        """Function to split image into grid"""
         m, n = self.grid_size
         w, h = self.tile_dim
         for j in range(m):
           for i in range(n):
             self.split_imgs.append(self.target_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))

    def RGB_list(self):
        """Function to get avg rgb values of tiles"""
        # to get avg rgb value of tile images
        for img in self.tile_folder:
            self.tile_avg.append(self.getavg_RGB(img))

        # to get avg rbg values of splitted target tiles
        for img in self.split_imgs:
            self.split_avg.append(self.getavg_RGB(img))

    def index_for_tile(self):
        """Function to find the closest image for a tile"""
        for img in self.split_avg:
            lst = []
            for tile in self.tile_avg:
                lst.append(self.get_dist(tile, img))
            self.index_list.append(lst.index(min(lst)))

    def create_grid(self, name):
        """Function to create the mosiac image"""
        w, h = self.tile_dim

        # New blank image
        img_grid = Image.new('RGB', (self.grid_size[0] * w, self.grid_size[1] * h))

        # pasting the closest image on the tile
        for i in range(len(self.index_list)):
            row = int(i/self.grid_size[1])
            col = i - self.grid_size[1] * row
            img_grid.paste(self.tile_folder[self.index_list[i]], (col*w, row*h))

        img_grid.save(f'{ name }.jpg')

def main():
    grid_size = (128,128)
    target_img = 'try2.jpg'
    img_directory = 'images'
    output_file = 'try2_mosiac'

    sol = Mosiac(grid_size)
    sol.load_images(target_img, img_directory)
    print('Images Loaded')
    sol.split_target()
    print('Finding closest Image')
    sol.RGB_list()
    sol.index_for_tile()
    print('Creating mosiac')
    sol.create_grid(output_file)
    print('Mosiac Created')

if __name__ == '__main__':
  main()
