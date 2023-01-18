# Epipolar-geometry-reconstitution

#In the zip of the statement, you will find two sequences of images taken by two cameras during the scanning of an object by a laser plane, these images are stored separately in 2 files named "sanLeft" and "scanRight", there are 25 scanned images in each file. In the "sanLeft" file, we have scan images named from "0000" to "0025", and in the "scanRight" file, we have scan images named from "scan0000" to "scan0025”. And the files are in the same path with our main python project.
You will also find shots of a checkerboard in different positions that will help you calibrate your cameras; they are stored in the file named "chessboards". In this "chessboards" file, there are 4 photos taken from the right side of the chessboard, they are named as "c1Right", "c2Right", "c3Right" and "c4Right". There are also 4 photos taken from the left side of the chessboard, they are named as "c1Light", "c2Light", "c3Light" and "c4Light". All the images are in png format.
The goal is to reconstruct the scanned object in 3D with python and OpenCV.

