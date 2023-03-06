from shapely.geometry import LineString
from shapely.affinity import rotate, translate
import numpy as np
import matplotlib.pyplot as plt
import math
import glob

# DATA IMPORT

path = "/Users/wilhelmtell/PycharmProjects/python/rund20/datensaetze/"

scanner_data_files = glob.glob(path + "*[1-3].npz*", recursive=True)

scanner1_temp = []
scanner2_temp = []
scanner3_temp = []

for file in scanner_data_files:
    if file.endswith("3.npz"):
        scanner3_temp.append(file)
    elif file.endswith("2.npz"):
        scanner2_temp.append(file)
    else:
        scanner1_temp.append(file)

scanner1_array = np.array(scanner1_temp)
scanner2_array = np.array(scanner2_temp)
scanner3_array = np.array(scanner3_temp)

i = 0

while i < len(scanner1_array):
    scanner1 = np.load(scanner1_array[i])
    scanner2 = np.load(scanner2_array[i])
    scanner3 = np.load(scanner3_array[i])
    i += 1

x1 = scanner1['x']
x2 = scanner2['x']
x3 = scanner3['x']
y1 = scanner1['z']
y2 = scanner2['z']
y3 = scanner3['z']

# Create a boolean mask that is True where x or y values are not 0

mask = np.logical_and(x1 != 0, y1 != 0)
mask2 = np.logical_and(x2 != 0, y2 != 0)
mask3 = np.logical_and(x3 != 0, y3 != 0)

# Apply the mask to x and y to remove the coordinates that contain 0

x1_filtered = x1[mask]
y1_filtered = y1[mask]

x2_filtered = x2[mask2]
y2_filtered = y2[mask2]

x3_filtered = x3[mask3]
y3_filtered = y3[mask3]

# neue maske, um das Rauschen zu entfernen

mask4 = x1_filtered <= 15
x1_oR = x1_filtered[mask4]
y1_oR = y1_filtered[mask4]

coords1 = np.column_stack([x1_oR, y1_oR])
coords2 = np.column_stack([x2_filtered, y2_filtered])
coords3 = np.column_stack([x3_filtered, y3_filtered])

# overall center

center = (0, 0)

# distance of the scanners to the absolute center
r = 260

# cylindrical coordinates of the positions of the scanners

scanner1_pos_cyl = (r, 7 * math.pi / 6)
scanner2_pos_cyl = (r, 11 * math.pi / 6)
scanner3_pos_cyl = (r, math.pi / 2)

# cartesian coordinates of the position of the scanners, the points are called 'center#'

scanner1_pos_x = scanner1_pos_cyl[0] * math.cos(scanner1_pos_cyl[1])
scanner1_pos_y = scanner1_pos_cyl[0] * math.sin(scanner1_pos_cyl[1])

center1 = (scanner1_pos_x, scanner1_pos_y)

scanner2_pos_x = scanner2_pos_cyl[0] * math.cos(scanner2_pos_cyl[1])
scanner2_pos_y = scanner2_pos_cyl[0] * math.sin(scanner2_pos_cyl[1])

center2 = (scanner2_pos_x, scanner2_pos_y)

scanner3_pos_x = scanner3_pos_cyl[0] * math.cos(scanner3_pos_cyl[1])
scanner3_pos_y = scanner3_pos_cyl[0] * math.sin(scanner3_pos_cyl[1])

center3 = (scanner3_pos_x, scanner3_pos_y)

# angle, each set of data has to be rotated

rotation_scanner1 = 300
rotation_scanner2 = 60
rotation_scanner3 = 180

# translating the LineStrings (line#trans) and then rotate it (line#rot)

line1 = LineString(coords1)
line1trans = translate(line1, xoff=scanner1_pos_x, yoff=scanner1_pos_y)
line1rot = rotate(line1trans, rotation_scanner1, origin=center1)
line2 = LineString(coords2)
line2trans = translate(line2, xoff=scanner2_pos_x, yoff=scanner2_pos_y)
line2rot = rotate(line2trans, rotation_scanner2, origin=center2)
line3 = LineString(coords3)
line3trans = translate(line3, xoff=scanner3_pos_x, yoff=scanner3_pos_y)
line3rot = rotate(line3trans, rotation_scanner3, origin=center3)

plt.plot(*line1rot.xy, color='b')
plt.plot(*line2rot.xy, color='r')
plt.plot(*line3rot.xy, color='k')

plt.show()
