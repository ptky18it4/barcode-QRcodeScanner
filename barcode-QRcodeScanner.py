from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) :
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', str(obj.data),'\n')

  return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points;

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Resize image
  scale_percent = 60  # percent of original size
  width = int(im.shape[1] * scale_percent / 100)
  height = int(im.shape[0] * scale_percent / 100)
  dim = (width, height)
  resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

  # Display results
  cv2.imshow("Results", resized)
  cv2.waitKey(0)


# Main
if __name__ == '__main__':

  # Read image
  im = cv2.imread('qrcode_fb.png')

  decodedObjects = decode(im)
  display(im, decodedObjects)

  # define a video capture object
  vid = cv2.VideoCapture(0)

  while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # After the loop release the cap object
  vid.release()
  # Destroy all the windows
  cv2.destroyAllWindows()

