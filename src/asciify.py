from PIL import Image
import sys


def resize_for_terminal(image, new_width):
    '''
    takes a Pillow image and returns a resized pillow image of new_width
    :param image: input Pillow image
    :return: Pillow image of NEW_WIDTH
    '''
    width, height = image.size
    division_factor = width / new_width
    # divide the current width to make it new_width
    # do the same for height, except cut it in half,
    # because terminals have greater width than height per character prinetd
    return image.resize((int(width / division_factor),
                         int(height / (division_factor * 2))))


def convert_to_grayscale(image):
    '''
    takes Pillow image and returns a grayscale version
    :param image: Pillow image
    :return: grayscaled Pillow image
    '''
    #L is for 8 bit greyscale according to: http://effbot.org/imagingbook/decoder.htm
    return image.convert('L')


def convert_to_ascii(image):
    '''
        takes Pillow image and returns ascii version
        :param image: Pillow image
        :return: ascii string
    '''

    width, height = image.size
    pixel_counter = 0 #current pixel number we are processing

    # index in string maps to a brightness range,
    # lower index characters in pixel_map correspond to darker pixels
    pixel_map = '@#%xo;:,.'

    # each interval maps to an index in pixel_map
    interval_length = 255 / len(pixel_map)

    #output_string is the result we keep on concatenating to
    output_string = ''

    #iterate through each pixel in the image
    for pixel in image.getdata():
        #if we are at the end of a line, print a newline
        if pixel_counter % width == 0:
            output_string += '\n'

        #get the index into the pixel_map
        result = round(pixel / interval_length)

        #special case if pixel value was 255 which gets mapped to 9
        if result >= len(pixel_map):
            result = len(pixel_map) -1

        #concatenate to result and increment counter
        output_string += pixel_map[result]
        pixel_counter += 1

    return output_string


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.stderr.write("Usage: python asciify.py <path-to-image> [terminal-width]")
        sys.exit(1)

    terminal_width = 80
    if len(sys.argv) == 3:
        try:
            terminal_width = int(sys.argv[2])
        except ValueError:
            sys.stderr.write('Incorrect terminal width passed, defaulting to 80')


    #open the image specified on the command line
    image = Image.open(sys.argv[1])
    #first convert the image to greyscale
    image = convert_to_grayscale(image)
    #then resize it so that it'll fit on a terminal
    image = resize_for_terminal(image, terminal_width)
    #print the string after conversion
    print(convert_to_ascii(image))
