# External Packages
import argparse
import cairo
import math
import random
from PIL import Image
# These are some colors which I liked.
list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
                  (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188),
                  (197, 239, 247), (190, 144, 212),
                  (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]


# Function for adding Noise
def float_gen(a, b): return random.uniform(a, b)


# Function for drawing a filled circle.
def draw_circle(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2 * math.pi)
    cr.fill()


# Function for drawing a filled square.
def draw_square(cr, x, y, side, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(x - (side / 2), y - (side / 2), side, side)
    cr.fill()


# Function for drawing a filled diamond.
def draw_diamond(cr, x, y, side, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.move_to(x, y - (side / 2))
    cr.rel_line_to(-side / 2, side / 2)
    cr.rel_line_to(side / 2, side / 2)
    cr.rel_line_to(side / 2, -side / 2)
    cr.close_path()
    cr.set_source_rgb(r, g, b)
    cr.fill_preserve()
    cr.set_source_rgb(r, g, b)
    cr.stroke()


# Function for drawing border for the label.
def draw_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height - size, width, size)
    cr.rectangle(width - size, 0, size, height)
    cr.fill()


# Dark background which gives it a gentle look.
def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()


# Function which randomly chooses color out of the list of colors.
def choose_color(last_color):
    rand_color = random.choice(list_of_colors)
    while rand_color == last_color:
        rand_color = random.choice(list_of_colors)
    return rand_color


# For drawing dashes for second column.
def draw_dash(cr, x1, y1, x2, y2, r, g, b, pattern):
    cr.set_source_rgb(r, g, b)
    cr.set_line_width(2.0)
    cr.set_dash(pattern)
    cr.move_to(x1, y1)
    cr.line_to(x2, y2)
    cr.stroke()


def main():
    # Arguments for custom designs.
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width", default=3000, type=int)
    parser.add_argument("--height", help="Specify Height", default=1000, type=int)
    parser.add_argument("-d", "--diamond", help="Logo Design", action="store_true")
    parser.add_argument("-s", "--square", help="Logo Design", action="store_true")
    parser.add_argument("-c", "--circle", help="Logo Design", action="store_true")
    parser.add_argument("-bs", "--bordersize", help="Border Width", default=20, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()

    width, height = args.width, args.height
    border_size = args.bordersize

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    # Background
    draw_background(cr, .2, .2, .2, width, height)

    # Choosing color // Last color is being used so that no two colors repeat.
    last_color = random.choice(list_of_colors)
    color = choose_color(last_color)
    last_color = color

    # Drawing Border
    r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
    draw_border(cr, border_size, r, g, b, width, height)

    # Choosing color
    color = choose_color(last_color)
    last_color = color

    # Make two columns with ratio of 2:8.
    r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
    cr.set_source_rgb(r, g, b)
    cr.move_to(592, 20)
    cr.line_to(592, 980)
    cr.stroke()

    # First column.
    color = choose_color(last_color)
    last_color = color
    r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0

    if args.diamond:
        draw_diamond(cr, x=286, y=480, side=400, r=r, g=g, b=b)

    elif args.square:
        draw_square(cr, x=286, y=480, side=400, r=r, g=g, b=b)

    elif args.circle:
        draw_circle(cr, x=286, y=480, radius=200, r=r, g=g, b=b)

    # Second Column contains only dashes as of now.
    draw_dash(cr, x1=593, y1=(height - 20) / 2, x2=width-20, y2=(height - 20) / 2, r=255, g=204, b=255, pattern=[76.0, 110])

    # Convert the surface to image.
    ims.write_to_png('Label-Flat.png')

    # Save the flat image(without noise)
    pil_image = Image.open('Label-Flat.png')
    pixels = pil_image.load()

    # Adding noise so as to give it a texture look.     // Texture Image.
    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]

            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r * noise), int(g * noise), int(b * noise))
    pil_image.save('Label-Texture.png')


# Calling the main function.    // Also , we could also use just main() for calling.
if __name__ == "__main__":
    main()
