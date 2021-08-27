# Color Palette
1. Returns a list of Matplotlib CSS colors for ease of access
2. Extracts a color palette from an image
3. Extracts a Matplotlib color palette from an image

## Setup
### Dependencies
1. Python3

See https://www.python.org/downloads/ to install the latest version of Python3.

2. requirements.txt

The `requirements.txt` file lists all the Python libraries needed, and they can be installed using:

```
pip install -r requirements.txt
```

## Useage
### Matplotlib Colors
You can create an alias in your rc file as follows:

```
alias colorpalette='python /path/to/dir/colorpalette.py'
```

Just running `colorpalette` on the command line will show a list of Matplotlib CSS colors and their names. You can search up colors that have a specific word in them by adding the following tag:

```
colorpalette -s blue
```

This will return Matplotlib CSS colors with the word "blue" in its name. 

### Image Color Palette
You can also obtain a color palette from an image of your choice. You just need to make sure that the image is in the same directory or specify the path to the image in the command, like below:

```
colorpalette -i image.jpg
```

This will return a window with your image and the color palette next to it, with the HEX value of the color as well.

### Matplotlib Image Color Palette
The concept is the same as above, but you can return just colors found in the Matplotlib CSS library. I'm using a basic weighted formula to determine the closest color, but I'm sure there are better methods out there. In `colorpalette.py`, you can find two other formulas I tried. Regardless of whether the colors are accurate to the image, it's fun to play around with! And you might get to see a nice color combination. The command you want to run is:

```
colorpalette -t image.jpg
```
