
number_points = 18
dco = DetectContours()
dci = DetectCircles()
fh = FindHomography()
points = []
cam_shape = []

points = read_dots("images/" + sys.argv[1])



print points
forwarp = cv2.imread('images/doge18.jpg')
height, width, depth = forwarp.shape
userpt_locations = get_dots("images/user/3e18user.jpg")
#userpt_orig_locations = original_locations(userpt_locations, (3,6), orig18, points)

#warp_image(map(lambda x:x[0], points), forwarp, (3,6), userpt_locations, points)

#warp_image(userpt_locations, forwarp, (3,6), map(lambda x:x[0] , points), userpt_locations)

warp_image(orig18, forwarp, (3,6), userpt_locations, map(lambda x:x[0], points))
