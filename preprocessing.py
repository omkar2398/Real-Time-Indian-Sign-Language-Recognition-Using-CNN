# STEP 2 (PART2): IMAGE PREPROCESSING
# TURNING IMAGE WITH A LOT OF FEATURES INTO A SIMPLE ONE TO FEED IT TO THE NN SO THAT IT WILL REQUIRE LESS COMPUTATIONAL POWER.

import numpy as np
import cv2
import os

from image_processing import func

if not os.path.exists("myProcessData"):
    os.makedirs("myProcessData")
if not os.path.exists("myProcessData/train"):
    os.makedirs("myProcessData/train")
if not os.path.exists("myProcessData/test"):
    os.makedirs("myProcessData/test")
path = "myData/train"
output = "myProcessData"
a = ["label"]

for i in range(128 * 128):
    a.append("pixel" + str(i))
# outputLine = a.tolist()

label = 0
var = 0
c1 = 0
c2 = 0

for (dirpath, dirnames, filenames) in os.walk(path):
    for dirname in dirnames:
        print(dirname)
        for (direcpath, direcnames, files) in os.walk(path + "/" + dirname):
            if not os.path.exists(output + "/train/" + dirname):
                os.makedirs(output + "/train/" + dirname)
            if not os.path.exists(output + "/test/" + dirname):
                os.makedirs(output + "/test/" + dirname)
            num = 0.70 * len(files)
            i = 0
            for file in files:
                var += 1
                actual_path = path + "/" + dirname + "/" + file
                output_path = output + "/" + "train/" + dirname + "/" + file
                output_path_test = output + "/" + "test/" + dirname + "/" + file
                img = cv2.imread(actual_path, 0)
                bw_image = func(actual_path)
                if i < num:
                    c1 += 1
                    cv2.imwrite(output_path, bw_image)
                else:
                    c2 += 1
                    cv2.imwrite(output_path_test, bw_image)

                i = i + 1

        label = label + 1

print(var)
print(c1)
print(c2)
