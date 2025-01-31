from PIL import Image
import numpy as np
import imageio
from tqdm import tqdm  # Import tqdm for progress bar
from scipy.ndimage import convolve
import os

def convolute(img_source):

    img_source = 'analyzer/plots/colors/' + img_source

    # Load your PNG file
    img = Image.open(img_source)

    # Convert image to numpy array (RGB)
    img_array = np.array(img)

    # Define a simple kernel (e.g., identity or blur kernel)
    kernel = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]) / 9

    # Function to apply convolution using scipy
    def apply_convolution(img_array, kernel):
        # Apply convolution for each color channel separately
        convolved_img_array = np.zeros_like(img_array)
        
        for c in range(img_array.shape[2]):  # Iterate over color channels (RGB)
            convolved_img_array[:, :, c] = convolve(img_array[:, :, c], kernel)
        
        return convolved_img_array

    # Prepare for GIF generation
    frames = []

    # Number of frames for GIF generation

    column_sizes = [30 - i for i in range(30)]  # List of column sizes to iterate over
    num_frames = len(column_sizes)  # We have 30 steps, one for each column count

    # Start with the original image
    current_img_array = img_array

    # Determine the target size for resizing all frames (use the size of the original image)
    height, width, _ = img_array.shape
    target_size = (width, height)  # We will resize all images to match the original size

    # Convolve image step by step and save frames for the GIF, with progress bar
    for i in tqdm(range(num_frames), desc="Generating Frames", unit="frame"):
        # Determine the current column size
        column_size = column_sizes[i % len(column_sizes)]  # Loop through the column sizes
        
        # Resize the image to the current column size
        new_width = column_size
        resized_img = Image.fromarray(current_img_array)
        resized_img = resized_img.resize((new_width, height))  # Resize to new width
        resized_img_array = np.array(resized_img)

        # Apply convolution to the resized image
        convolved_img_array = apply_convolution(resized_img_array, kernel)

        # Resize back to the target size (original size) to ensure all frames are the same size
        resized_back_img = Image.fromarray(np.clip(convolved_img_array, 0, 255).astype(np.uint8))
        resized_back_img = resized_back_img.resize(target_size)  # Resize to original size
        frames.append(np.array(resized_back_img))  # Store frame as numpy array

    # Create and save the GIF
    file_path = '/'.join(img_source.split('/')[:-1])
    file_path = file_path + '/blur_convolution_gifs/' + img_source.split('/')[-1][:-3] + 'gif'

    imageio.mimsave(file_path, frames, duration=0.1)  # Adjust duration for frame speed

# convolute('or_joy.png')

folder_path = 'analyzer/plots/colors/'

# Get a list of all file names in the folder
file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

for pngs in file_names:
    convolute(pngs)
