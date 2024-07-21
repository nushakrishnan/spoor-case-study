import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


def main(db_file, plot_file):
    connection = sqlite3.connect(db_file)
    query = "SELECT * FROM detections WHERE Class = 'bird'"
    df = pd.read_sql_query(query, connection)
    connection.close()

    df['Timestamp'] = pd.to_datetime(df['Timestamp'].astype(str),
                                     format='%H:%M:%S')

    df['Second'] = df['Timestamp'].dt.floor('S')
    accumulated_frame_count = df.groupby(
        ['Second', 'Frame']).size().reset_index(name='accumulated_count')

    bird_counts = accumulated_frame_count.groupby(
        'Second')['accumulated_count'].mean().reset_index(name='average_count')
    bird_counts['average_count'] = bird_counts['average_count'].astype(int)
    bird_counts['duration_seconds'] = (
        bird_counts['Second'] -
        bird_counts['Second'].min()).dt.total_seconds()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=bird_counts, x='duration_seconds', y='average_count')
    plt.xlabel('Duration video (seconds)')
    plt.ylabel('Number of birds detected')
    plt.title('Bird Count Analysis')
    plt.grid(False)
    plt.gca().yaxis.get_major_locator().set_params(integer=True)
    plt.savefig(plot_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot bird count analysis.')

    parser.add_argument('db_file',
                        type=str,
                        help='Path to the input database.')
    parser.add_argument('plot_file',
                        type=str,
                        help='Path to the output image.')

    args = parser.parse_args()
    main(args.db_file, args.plot_file)
