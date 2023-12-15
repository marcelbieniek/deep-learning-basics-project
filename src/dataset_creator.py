"""
Dataset creator app entry point
"""

from dataset_manager import DatasetManager


def main():
    """ Main function """
    data_path = "../data/"

    dataset_manager = DatasetManager(data_path)
    dataset_manager.create_dataset()


if __name__ == "__main__":
    main()
