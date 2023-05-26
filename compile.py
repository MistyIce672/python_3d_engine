import cv2
import os

# Directory containing the images
image_directory = 'output'

# Output video filename
output_video = 'output_video.mp4'

# Frame rate (number of frames per second)
frame_rate = 30

# Get the list of image filenames in the directory
image_files = sorted([os.path.join(image_directory, file) for file in os.listdir(image_directory)])

# Read the first image to get the dimensions
first_image = cv2.imread(image_files[0])
height, width, channels = first_image.shape

# Create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 video
video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

# Iterate over the image files and write each frame to the video
def oder(images):
    for count in range(0,len(images)):
        for count in range(0,len(images)):
            if count+1 < len(images):
                if int(images[count].split(".")[0].split("\\")[-1]) > int(images[count+1].split(".")[0].split("\\")[-1]):
                    images[count],images[count+1] = images[count+1],images[count]
    return(images)

images = oder(image_files)
print(images)
for image_file in image_files:
    print(image_file)
    image = cv2.imread(image_file)
    video_writer.write(image)

# Release the video writer
video_writer.release()