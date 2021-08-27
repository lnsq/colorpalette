import argparse
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import numpy as np

from sklearn.cluster import KMeans
import cv2 as cv
import math

def rgb2hex(r,g,b):
    """
    input: RGB value of color
    output: hex value of RGB color
    """
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

## K-means method to extract palette of colors from an image
def palette(clusters):
    width=300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_): 
        palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
    return palette

def imagePalette(img, marker=0):
    # can change number of clusters
    clt = KMeans(n_clusters=5)
    clt_1 = clt.fit(img.reshape(-1, 3))
    unique = np.unique(palette(clt_1)[0], axis=0)
    if marker == 0:
        return unique
    else:
        return palette(clt_1)

## can play around with these weights to get a more accurate similarity between the colors
def colorDistance_euclidian(rgb1, rgb2):
    return math.sqrt(pow((rgb2[0]-rgb1[0]),2) + pow((rgb2[1]-rgb1[1]),2) + pow((rgb2[2]-rgb1[2]),2))

def colorDistance_weighted(rgb1, rgb2):
    return 2*rgb1[0]*rgb2[0] + 4*rgb1[1]*rgb2[1] + 3*rgb1[2]*rgb2[2]

def colorDistance_weighted_1(rgb1, rgb2):
    return math.sqrt(pow(((rgb2[0]-rgb1[0])*0.299),2) + pow(((rgb2[1]-rgb1[1])*0.587),2) + pow(((rgb2[2]-rgb1[2])*0.114),2))

def closestColor(color, rgbList, colorList):
    distances = [colorDistance_weighted(color, secondColor) for secondColor in rgbList]
    index = distances.index(min(distances))
    return colorList[index], index

def show_img_compar(img_1, text, mpl = None):
    f, ax = plt.subplots(1, 2, figsize=(10,10))
    ax[0].imshow(img_1)
    if text:
        for i, hex_val in enumerate(text):
            ax[1].text(0.1, 0.85 - 0.17*i, text[i], fontsize=20, color = "black", bbox=dict(facecolor=hex_val, edgecolor='none',boxstyle='square,pad=1.5'))
    elif mpl:
        for i, hex_val in enumerate(mpl):
            ax[1].text(0.1, 0.85 - 0.17*i, mpl[i], fontsize=20, color = "black", bbox=dict(facecolor=hex_val, edgecolor='none',boxstyle='square,pad=1.5'))
    
    ax[0].axis('off')
    ax[1].axis('off')
    f.tight_layout()
    plt.show()

def printColors(colors, sort_colors = True, title = "", searchColor = None, similarColor = None):
    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)
    
    if searchColor:
        names = [name for name in names if searchColor in name]

    nearestColors = []
    if similarColor is not None:
        ## drop grays and blacks
        drop = ['black', 'gray', 'grey', 'white', 'silver', 'gainsboro', 'snow', 'linen']
        for unwanted in drop:
            colors = {k:v for k,v in colors.items() if unwanted not in k}
            names = [name for name in names if unwanted not in name]

        ## get list of rgb values of colors
        rgb = [mcolors.to_rgb(color) for color in colors]
        for color in similarColor:
            closest, index = closestColor(color, rgb, names)
            nearestColors.append(closest)
            names.pop(index)
            rgb.pop(index)
        names = nearestColors
        return names

    n = len(names)

    ncols = 4
    nrows = n // ncols + int( n % ncols > 0 )

    cell_width = 212
    cell_height = 22
    swatch_width = 30
    margin = 12
    topmargin = 40

    width = cell_width * 3 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-topmargin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(title, fontsize=24, loc="left", pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7')
        )

    return fig


def main(args):
    if args.search:
        printColors(mcolors.CSS4_COLORS, True, "CSS Colors", args.search)
    elif args.imagetompl and args.image:
        print("Please select only one option between -i and -t.")
        return
    elif args.imagetompl:
        img = cv.imread(args.imagetompl)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        names = printColors(mcolors.CSS4_COLORS, True, "CSS Colors", args.search, imagePalette(img))
        show_img_compar(img, None, names)
    elif args.image:
        img = cv.imread(args.image)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        rgb_values = imagePalette(img)
        hex_values = []
        for rgb in rgb_values:
            hex_values.append(rgb2hex(rgb[0], rgb[1], rgb[2]))
        show_img_compar(img, hex_values)
    else:
        printColors(mcolors.CSS4_COLORS, True, "CSS Colors")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help="search for a particular color group")
    parser.add_argument("-i", "--image", type=str, help="search for a particular color group that matches the colors in a specified image")
    parser.add_argument("-t", "--imagetompl", type=str, help="search for a particular color group from the list of CSS matplotlib colors that matches the colors in a specified image")

    args = parser.parse_args()

    main(args)