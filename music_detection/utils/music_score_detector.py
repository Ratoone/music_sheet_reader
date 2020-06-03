import cv2
import numpy as np 

#Link to the tutorial that helped me :
#https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/


def scale_image(img : np.ndarray) -> np.ndarray:
    """Scale down an image for display with cv2.imshow()
       :img : image to be scaled
       :return : scaled down image
    """
    max_height = 800
    max_width = 1600
    height = img.shape[0]
    width = img.shape[1]
    if height > max_height:
        ratio = max_height/height
        height = max_height
        width = int(width*ratio)
    if width > max_width:
        ratio = max_width/width
        width = max_width
        height = int(height*ratio)

    img_resized = cv2.resize(img, (width, height))
    return img_resized

    

def find_music_score(image:np.ndarray) -> np.ndarray:
    """Locate and the music score in image, udistorts it, crops it out
       :image: RGB image containing the music score
       :return : rectified gray-level image of the music score 
    """
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    RESIZE_RATIO = 0.5
    height = int(im_gray.shape[0]*RESIZE_RATIO)
    width = int(im_gray.shape[1]*RESIZE_RATIO)
    #Downgrading the resolution speeds up the calculation, and
    #makes potential parasitic countours 
    im_resized = cv2.resize(im_gray, (width, height))

    #Downscaled image blurring and edge extraction
    im_blurr = cv2.GaussianBlur(im_resized, (3,3),0)
    edges = cv2.Canny(im_blurr, 75,200)

    #Closed contours localization
    contours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    #It is assumed that the music score is among the 5 longest
    #contours found. That is a realistic assumption considering that
    #the music score is supposed to be the main subject of the photograph
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

    # loop over the contours
    for contour in contours:
        # approximate the contour
        perimeter = cv2.arcLength(contour, True)
        
        #Approximate contour with a curve defined by the points stored in approx_contour
        approx_contour = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        # if the approximated contour has four points, then we
        # can assume that we have found the musci score
        if len(approx_contour) == 4:
            sheet_contour = approx_contour
            break

    pts = np.resize(sheet_contour, (4,2))

    #rect is to contain the corner points in the following order :
    #top-left, bottom-left, bottom-right, top-right 
    rect = np.zeros((4,2), np.float32)

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)] #top-left corner
    rect[2] = pts[np.argmax(s)] #bottom-right corner

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)] #bottom-left corner
    rect[3] = pts[np.argmax(diff)] #top-right corner

    rect = rect/RESIZE_RATIO #Corner coordinates are expressed in the unscaled image

    #Calculates the witdth and height of the rectified music score
    #They are considered to be the largest width and height values of the undistorded
    #image
    width = int(max(np.linalg.norm(rect[0]-rect[3]), np.linalg.norm(rect[1]-rect[2])))
    height = int(max(np.linalg.norm(rect[0]-rect[1]), np.linalg.norm(rect[2]-rect[3])))

    #Coordinates of the corners in the rectified picture
    new_shape = np.array([[0,0], [height-1,0], [height-1, width-1], [0,width-1]], np.float32)

    tform = cv2.getPerspectiveTransform(rect, new_shape)
    warped = cv2.warpPerspective(im_gray, tform, (height, width))

    return warped