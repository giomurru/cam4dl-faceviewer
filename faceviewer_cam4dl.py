import json
import matplotlib.pyplot as plt
import PIL.Image
import numpy as np
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="filename",
                    help="the input image file name", metavar="INPUT_IMAGE", required=True)
#parser.add_argument("-q", "--quiet",
#                    action="store_false", dest="verbose", default=True,
#                    help="don't print status messages to stdout")

args = parser.parse_args()

with open('{}.JSON'.format(os.path.splitext(args.filename)[0])) as user_file:
  file_contents = user_file.read()
  
print(file_contents)

parsed_json = json.loads(file_contents)

image = PIL.Image.open(args.filename)
np_image_initial = np.array(image)



# get image EXIF
image_exif = image.getexif()
# retrieve orientation byte
orientation = image_exif.get(0x0112)
print(orientation)

# get the corresponding transformation
method = {
    2: PIL.Image.FLIP_LEFT_RIGHT,
    3: PIL.Image.ROTATE_180,
    4: PIL.Image.FLIP_TOP_BOTTOM,
    5: PIL.Image.TRANSPOSE,
    6: PIL.Image.ROTATE_270,
    7: PIL.Image.TRANSVERSE,
    8: PIL.Image.ROTATE_90,
}.get(orientation)
if method is not None:
    # replace original orientation
    image_exif[0x0112] = 1
    # apply transformation
    image = image.transpose(method)

np_image_correct = np.array(image)

implot = plt.imshow(np_image_correct)


faces = parsed_json['faces']
landmarks = faces[0]['landmarks']
bbox = faces[0]['bbox']
bbox_origin = bbox[0]
bbox_size = bbox[1]
landmarks_x = map(lambda x: bbox_origin[0] * image.width + x[0] * image.width * bbox_size[0], landmarks)
landmarks_y = map(lambda x: (1.0 - bbox_size[1] - bbox_origin[1]) * image.height  + (1.0 - x[1]) * image.height * bbox_size[1], landmarks)
x = list(landmarks_x)
y = list(landmarks_y)
print(x)
print(y)
# put a red dot, size 40, at 2 locations:
plt.scatter(x=x, y=y, c='g', s=3)
  

plt.show()