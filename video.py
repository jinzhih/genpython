import cv2
import numpy as np
import os

# Directory to save the video
output_dir = './content'

# Video properties
frame_width = 1920
frame_height = 1080
fps = 30

# Texts to display
texts = ["Text 1", "Text 2", "Text 3"]  # Add your texts here

# Font properties
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (255, 255, 255)  # White color

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(os.path.join(output_dir, 'output_video.mp4'), fourcc, fps, (frame_width, frame_height))

# Generate frames with text
for text in texts:
    # Create a black background
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Get text size and position
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = int((frame_width - text_size[0]) / 2)
    text_y = int((frame_height + text_size[1]) / 2)

    # Put text on the frame
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # Write frame to video
    for n in range(150):
      video.write(frame)
   

# Release VideoWriter object
video.release()