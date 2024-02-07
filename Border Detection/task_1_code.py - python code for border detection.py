import cv2
import rembg

# Function to draw object outline
def draw_outline(image, contour, thickness):
    cv2.drawContours(image, [contour], 0, (0, 255, 0), thickness)

# Function to remove background using rembg
def remove_background(image):
    result = rembg.remove(image)
    return result

# Input image path
input_image_path = 'TEST IMAGES/4.jpg'

# Read the input image
image = cv2.imread(input_image_path)

# Get original image dimensions
height, width = image.shape[:2]

# Set the window size with the same aspect ratio as the original image
window_width = 800
window_height = int(height * (window_width / width))
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", window_width, window_height)

# Specify the thickness of the rectangle
rectangle_thickness = 3

while True:
    # Display the image
    cv2.imshow("Image", image)

    # Ask user to draw a rectangle over an object
    roi = cv2.selectROI("Image", image)

    # Crop the selected Region Of Interest (ROI)
    x, y, w, h = roi
    roi_image = image[y:y + h, x:x + w]

    # Remove background from ROI using rembg
    roi_image_no_bg = remove_background(roi_image)

    # Find contours in the ROI
    contours, _ = cv2.findContours(cv2.cvtColor(roi_image_no_bg, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Draw outline over the object with specified thickness
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        draw_outline(image[y:y + h, x:x + w], max_contour, rectangle_thickness)

    # Overlay object outline in the original input image
    cv2.imshow("Image", image)

    # Wait for user input
    key = cv2.waitKey(0)

    # Press 'q' to quit
    if key == ord('q'):
        break
    # Press 'c' to clear outline
    elif key == ord('c'):
        image = cv2.imread(input_image_path)

cv2.destroyAllWindows()
