from PIL import Image
import matplotlib.pyplot as plt

def eye_positions(img):
    # One-at-a-time clicks are more robust. Block for each.
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    
    # Step 1: left eye
    plt.title("Click eye on the left")
    x1, y1 = plt.ginp_t(1, timeout=-1)[0]
    plt.plot(x1, y1, 'gx')
    plt.draw()
    
    # Step 2: right eye
    plt.title("Click eye on the right")
    x2, y2 = plt.ginp_t(1, timeout=-1)[0]
    plt.plot(x2, y2, 'gx')
    plt.draw()
    plt.close()
    
    return (x1, y1), (x2, y2)  # return left, right tuple


import numpy as np

def extract_face(img):
    # Convert to grayscale
    gray_img = img.convert('L')
    
    # Get eye positions
    c1, c2 = eye_positions(gray_img)
    
    # Calculate angle
    angle = np.degrees(np.arctan2(______, ______))
    print("Angle =", angle)
    # Rotate image
    I2_img = gray_img.rot_te(angle, expand=False)
    I2 = np.array(I2_img)

    # Center coordinates
    h, w = I2.shape
    R = np.array([[______(np.radians(______)), ______(np.radians(______))],
                  [______(np.radians(______)), ______(np.radians(______))]])
    
    new_c1 = (R @ (np.array(c1).______-np.array([[w/2], [h/2]]))) + np.array([[w/2], [h/2]])
    new_c2 = (R @ (np.array(c2).______-np.array([[w/2], [h/2]]))) + np.array([[w/2], [h/2]])

    plt.imshow(img, cmap='gray')
    # Show eyes
    plt.figure()
    ax = plt.gca()
    ax.imshow(I2, cmap='gray')
    ax.plot(new_c1[0], new_c1[1], 'go')
    ax.plot(new_c2[0], new_c2[1], 'go')
    plt.title("Rotated image with eye positions (left, then right)")
    plt.show(block=False)
    plt.figure()
    # size of face
    scale = np.sqrt(np.sum((new_c1 - new_c2) __ 2))

    # Crop and resize
    x, y = new_c1.flatten()
    crop_box = (int(______), int(______), int(______), int(______))
    cropped = I2_img.crop(crop_box)
    cropped = cropped.resize((______, ______))

    # Show crop
    plt.imshow(cropped, cmap='gray')
    plt.axis('off')
    plt.show(block=False)

    return cropped


if __name__ == "__main__":
    img = Image.open('lena.png')
    # left, right = eye_positions(img)
    # print("Left eye: (%.1f, %.1f)" % left)
    # print("Right eye: (%.1f, %.1f)" % right)
    face = extract_face(img.rotate(45, expand=False))
    plt.figure()
    plt.imshow(face, cmap='gray')
    plt.title("Extracted Face")
    plt.show()