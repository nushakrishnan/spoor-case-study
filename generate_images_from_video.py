import os
import cv2
import argparse
from utils import delete_files_in_folder


def main(video_file, image_dir):
    os.makedirs(image_dir, exist_ok=True)
    delete_files_in_folder(image_dir)

    video = cv2.VideoCapture(video_file)
    if not video.isOpened():
        raise Exception('Error opening video file')

    frame_number = 0
    while True:
        success, frame = video.read()
        if not success:
            break

        frame_number += 1
        output_file = os.path.join(image_dir, f'frame_{frame_number}.jpg')

        cv2.imwrite(output_file, frame)
        print(f'Frame {frame_number} saved to {output_file}')

    video.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract frames from a video.')

    parser.add_argument('video_file',
                        type=str,
                        help='Path to the input video file.')
    parser.add_argument('image_dir',
                        type=str,
                        help='Directory to save the extracted frames.')

    args = parser.parse_args()
    main(args.video_file, args.image_dir)
