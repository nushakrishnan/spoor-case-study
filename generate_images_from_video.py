import os
import cv2

from utils import delete_files_in_folder

home = os.path.expanduser('~')
video_file = './data/pigeon.mp4'
output_dir = f'{home}/Documents/assignments/images/'

os.makedirs(output_dir, exist_ok=True)
delete_files_in_folder(output_dir)

video = cv2.VideoCapture(video_file)
if not video.isOpened():
    raise Exception('Error opening video file')

frame_number = 0
while True:
    success, frame = video.read()
    if not success:
        break

    frame_number += 1
    output_file = os.path.join(output_dir, f'frame_{frame_number}.png')

    cv2.imwrite(output_file, frame)
    print(f'Frame {frame_number} saved to {output_file}')

video.release()
