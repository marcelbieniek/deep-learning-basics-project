"""
Dataset creator app entry point
"""

from dataset_manager import DatasetManager


def main():
    """ Main function """
    data_path = "../data/"
    segments_amount_per_track = 10
    segment_duration_in_s = 10

    dataset_manager = DatasetManager(data_path, segments_amount_per_track, segment_duration_in_s)
    dataset_manager.create_dataset()


if __name__ == "__main__":
    main()
