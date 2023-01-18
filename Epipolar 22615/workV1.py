import cv2
import numpy as np

#step 1: calibrate the camera with cv2.calibrateCamera()
# Load the checkerboard images in the file
c1Right = cv2.imread("chessboards/c1Right.png")
c2Right = cv2.imread("chessboards/c2Right.png")
c3Right = cv2.imread("chessboards/c3Right.png")
c4Right = cv2.imread("chessboards/c4Right.png")
c1Left = cv2.imread("chessboards/c1Left.png")
c2Left = cv2.imread("chessboards/c2Left.png")
c3Left = cv2.imread("chessboards/c3Left.png")
c4Left = cv2.imread("chessboards/c4Left.png")

# Define the chessboard size
chessboard_size = (7*7,3)

# Find the chessboard corners
ret, cornersRight1 = cv2.findChessboardCorners(c1Right, chessboard_size)
ret, cornersRight2 = cv2.findChessboardCorners(c2Right, chessboard_size)
ret, cornersRight3 = cv2.findChessboardCorners(c3Right, chessboard_size)
ret, cornersRight4 = cv2.findChessboardCorners(c4Right, chessboard_size)
ret, cornersLeft1 = cv2.findChessboardCorners(c1Left, chessboard_size)
ret, cornersLeft2 = cv2.findChessboardCorners(c2Left, chessboard_size)
ret, cornersLeft3 = cv2.findChessboardCorners(c3Left, chessboard_size)
ret, cornersLeft4 = cv2.findChessboardCorners(c4Left, chessboard_size)

# Define the chessboard points in 3D
objp = np.zeros((chessboard_size[0]*chessboard_size[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboard_size[0],0:chessboard_size[1]].T.reshape(-1,2)

#Create arrays to store the object points and image points
objpoints = []
imgpointsRight = []
imgpointsLeft = []

#Append the object points and image points from the first image
objpoints.append(objp)
imgpointsRight.append(cornersRight1)
imgpointsLeft.append(cornersLeft1)

#Append the object points and image points from the second image
objpoints.append(objp)
imgpointsRight.append(cornersRight2)
imgpointsLeft.append(cornersLeft2)

#Append the object points and image points from the third image
objpoints.append(objp)
imgpointsRight.append(cornersRight3)
imgpointsLeft.append(cornersLeft3)

#Append the object points and image points from the fourth image
objpoints.append(objp)
imgpointsRight.append(cornersRight4)
imgpointsLeft.append(cornersLeft4)

#Calibrate the cameras
ret, mtxRight, distRight, rvecsRight, tvecsRight = cv2.calibrateCamera(objpoints, imgpointsRight, c1Right.shape[1::-1], None, None)
ret, mtxLeft, distLeft, rvecsLeft, tvecsLeft = cv2.calibrateCamera(objpoints, imgpointsLeft, c1Left.shape[1::-1], None, None)

#Undistort the scanned images
for i in range(25):
 scanLeft[i] = cv2.undistort(scanLeft[i], mtxLeft, distLeft, None, mtxLeft)
 scanRight[i] = cv2.undistort(scanRight[i], mtxRight, distRight, None, mtxRight)


#step 2: find the fundamental matrix with cv2.findFundamentalMat() of 2 images
# Define the object points and image points, the points are stored in an array
objpoints = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objpoints[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)
imgpointsRight = [cornersRight1, cornersRight2, cornersRight3, cornersRight4]
imgpointsLeft = [cornersLeft1, cornersLeft2, cornersLeft3, cornersLeft4]

# Compute the fundamental matrix
F, mask = cv2.findFundamentalMat(imgpointsLeft, imgpointsRight, cv2.FM_8POINT)

#step 3: find the essential matrix with cv2.findEssentialMat() of 2 cameras
E, mask = cv2.findEssentialMat(imgpointsLeft, imgpointsRight, K1, method=cv2.RANSAC, prob=0.999, threshold=1.0)

#step 4: Recover the relative camera pose
# Recover the relative camera pose
_, R, t, mask = cv2.recoverPose(E, imgpointsLeft, imgpointsRight, K1)

# step 5 Triangulate the 3D points from the 2d monkey
# step 5.1 : Load the scanned images
scanned_left_images = []
scanned_right_images = []

for i in range(25):
 scanned_left_images.append(cv2.imread("scanLeft/{}.png".format(str(i).zfill(4))))
 scanned_right_images.append(cv2.imread("scanRight/scan{}.png".format(str(i).zfill(4))))

#step 5.2 : undistort the scanned images, because images may deform 
undistorted_left_images = []
undistorted_right_images = []
for i in range(25):
 undistorted_left_images.append(cv2.undistort(scanned_left_images[i],camera_matrix_left, distortion_coefficients_left))
 undistorted_right_images.append(cv2.undistort(scanned_right_images[i],camera_matrix_right, distortion_coefficients_right))

#step 5.3: find the 2D points in the undistorted images
points_2d_left = []
points_2d_right = []
for i in range(25):
 ret,points_2d_l = cv2.findChessboardCorners(undistorted_left_images[i], chessboard_size)
 ret,points_2d_r = cv2.findChessboardCorners(undistorted_right_images[i], chessboard_size)
 points_2d_left.append(points_2d_l)
 points_2d_right.append(points_2d_r)

#step 5.4: triangulate the 3D points
points_3d = []
for i in range(25):
 point_4d = cv2.triangulatePoints(P_left, P_right, points_2d_left[i], points_2d_right[i])
 point_3d = point_4d / np.repeat(point_4d[-1, :], 4, axis=0)
 points_3d.append(point_3d)

#Step6: convert the 3D points to a point cloud format and visualize using Open3D
point_cloud = PointCloud()
point_cloud.points = Vector3dVector(points_3d)
draw_geometries([point_cloud])

