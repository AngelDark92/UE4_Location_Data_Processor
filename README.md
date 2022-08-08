# PythonProgram
An unpacker for position data exported by the Unreal Engine project for Spatial Development made for University of Magna Grecia, Italy. The program builds animation data and a heatmap of where people have walked as data for later review.

## Usage
The program can be used with any position data exported by unreal engine in the .csv format. The position data is usually in the format x=number y=number z=number. In this particular instance the positions are all collected after a 10ms interval so the app can create a realtime animation and a heatmap. The multiple elements are all separated by the comma delimiter as per .csv standards.
eg.:

| Data                     |
| ------------------------ |
| x=192.93 y=23.54 z=12.93 |
| x=23.34 y=563.33 z=12.45 |
| x=192.93 y=23.54 z=12.93 |

is:

> x=192.93 y=23.54 z=12.93, x=23.34 y=563.33 z=12.45, x=192.93 y=23.54 z=12.93

in the .csv file.

The line 51-54:
```python
xmin = -338.278
    xmax = 778.277
    ymin = -798.278
    ymax = 308.277
print s
```
Contains the max coordinates that the box is going to render, this will need to be updated for every project accordingly.

##acknowledgements
This program in particular is very heavy on RAM because it collects all the data at once and converts it to a gif file. A future version might contain an iterative process to creater various .png files to then put them together into a .gif animation file.
