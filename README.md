# Simple Slam
Visual Slam implementation for practice. Used orb features (Akaze can also be used) as sift feature extraction was slowing down the process.


## How to run
```
StartFrame=0 F=270 DownScale=4 ./main.py videos/<Video>.mp4
```
* F is focal lenght
* StartFrame seeks from the frame specified
* DownScale downsize the image i.e 2 means half of the image
## Built With
* [Python3](https://www.python.org/download/releases/3.0/)
* [PyGame](https://www.pygame.org/)
* [OpenCV](https://pypi.org/project/opencv-python/)
* [NumPy](https://numpy.org/)

## To-do
* Triangulation
* pangolin for 3-D display
* g2opy for optimization

## Acknowledgements
* [GeoHotz](https://github.com/geohot)
