import os
import argparse


def main(video_file, model_path):
    video_dir = os.path.dirname(video_file)
    image_dir = os.path.join(video_dir, 'images')
    csv_file = os.path.join(video_dir, 'predictions.csv')
    db_file = csv_file.replace('.csv', '.db')
    plot_file = os.path.join(video_dir, 'bird_count.jpg')

    os.system(f"python generate_images_from_video.py {video_file} {image_dir}")
    os.system(
        f"python yolo_prediction.py {image_dir} {model_path} {video_file} {csv_file}"
    )
    os.system(f"python create_db.py {csv_file} {db_file}")
    os.system(f"python plot_graph.py {db_file} {plot_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run end-to-end workflow.')
    parser.add_argument('video_file',
                        type=str,
                        help='Path to the input video file.')
    parser.add_argument('model_path', type=str, help='Path to the YOLO model.')

    args = parser.parse_args()
    main(args.video_file, args.model_path)
