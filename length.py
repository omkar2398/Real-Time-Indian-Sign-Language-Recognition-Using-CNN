import os
import cv2

path = "myProcessData"
train_path = "myProcessdata/train"
test_path = "myProcessdata/test"

for (dirpath, dirnames, filenames) in os.walk(train_path):
    for dirname in dirnames:
        print(dirname)

        for (direcpath, direcnames, files) in os.walk(train_path + "/" + dirname):
            num = len(files)
            print("train : ", num)

        for (direcpath, direcnames, files) in os.walk(test_path + "/" + dirname):
            num = len(files)
            num += num
            print("test : ", num)
