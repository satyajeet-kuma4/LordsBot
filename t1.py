import cv2

# Load full screenshot and cropped image
full_img = cv2.imread("utils/full.png")
cropped_img = cv2.imread("utils/cropped.png")

# Match cropped image in full image
result = cv2.matchTemplate(full_img, cropped_img, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Get top-left corner and dimensions
top_left = max_loc
w, h = cropped_img.shape[1], cropped_img.shape[0]

# Print region
print(f"Region found at: x={top_left[0]}, y={top_left[1]}, width={w}, height={h}")

# Draw rectangle on original image
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(full_img, top_left, bottom_right, (0, 255, 0), 2)

# Resize for display (scaling down to 50%)
scale_percent = 50  # You can tweak this (e.g., 30, 70)
width = int(full_img.shape[1] * scale_percent / 100)
height = int(full_img.shape[0] * scale_percent / 100)
resized = cv2.resize(full_img, (width, height))

# Show resized image
cv2.imshow("Matched Region (Resized)", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
