import numpy as np
import pandas as pd
import cv2
import os
import matplotlib.pyplot as plt
import datetime
from pathlib import Path
from typing import Optional, List

class Dataset:
    def __init__(self, sequence_number):
        self.seq_dir: Path = "data/sequences/" + str(sequence_number)
        self.pos_dir: Path = "data/poses/" + str(sequence_number) + ".txt"
        self.calib_dir: Path = "data/calib/" + str(sequence_number) + ".txt"

        self.pos_df: Optional[pd.DataFrame] = pd.read_csv(self.pos_dir, delimiter = " ", header = None)
        self.calib_df: Optional[pd.DataFrame] = pd.read_csv(self.calib_dir, delimiter = " ", header = None, index_col = 0)
        self.left_images: List[Path] = os.listdir(self.seq_dir + "/" + "image_0/")
        self.right_images: List[Path] = os.listdir(self.seq_dir + "/" + "image_1/")

        self.P0: Optional[np.ndarray]  = None
        self.P1: Optional[np.ndarray] = None
        self.P2: Optional[np.ndarray] = None
        self.P3: Optional[np.ndarray] = None
        self.TR: Optional[np.ndarray] = None

        self.gt: np.ndarray = np.zeros((len(self.pos_df), 3, 4))

    def total_num_images_on_seq(self):
        print("Number of Images on Sequence: ", len(self.left_images))

    def get_poses_from_df(self):
        self.P0 = np.array(self.calib_df.loc["P0"]).reshape(3, 4)
        self.P1 = np.array(self.calib_df.loc["P1"]).reshape(3, 4)
        self.P2 = np.array(self.calib_df.loc["P2"]).reshape(3, 4)
        self.P3 = np.array(self.calib_df.loc["P3"]).reshape(3, 4)

    def get_translation_matrices(self):
        self.TR = np.array(self.calib_df.loc["Tr"]).reshape(3, 4)

    def gt_poses(self):
        for i in range(len(self.pos_df)):
            self.gt[i] = np.array(self.pos_df.iloc[i]).reshape(3, 4)

    def reset_frames(self):
        self.left_images = (cv2.imread(self.seq_dir + "/" + "image_0/" + left_img_name, 0) for left_img_name in self.left_images)
        self.right_images = (cv2.imread(self.seq_dir + "/" + "image_1/" + right_img_name, 0) for right_img_name in self.right_images)


if __name__ == "__main__":
    pass