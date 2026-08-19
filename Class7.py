import cv2
#Load the image
image =cv2.imread('Example.png')
#Resize the window to a specific size without resizing the image
cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL)#Create a resizeable window
cv2.resizeWindow('Loaded Image', 800, 500)#Set the window size to 800x500 (width x height)
#Display the image in the resizeable window
cv2.imshow('Loaded Image', image)
cv2.waitKey(0)#Wait for a key press
cv2.destroyAllWindows()#Close the window
#Print the image Properties
print(f"Image Dimension:{image.shape}")#Height, Width, Channels