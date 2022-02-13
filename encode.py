import cv2
import numpy as np
import argparse


def integer_to_bit_list(integer: int, num_bytes: int=1) -> list:
    """Convert an integer to a list of bits

    Args:
        integer (int): input integer
        num_bytes (int, optional): byte number of the integer. 1 corresponds to a C char value. Defaults to 1.

    Returns:
        list: list of bit values
    """
    return [integer >> i & 1 for i in range(num_bytes*8-1, -1, -1)]

def encode_img(img: np.array, message: bytes, bit_idx: int=0) -> np.array:
    """Hide message in img

    Args:
        img (np.array): Image as numpy array
        message (bytes): message as byte string
        bit_idx (int, optional): Which bit to hide the message. If set to zero the least important bit is used. 
                                 Defaults to 0.

    Returns:
        np.array: image with hidden message as numpy array
    """
    width, height, channels = img.shape
    assert width*height*channels >= 8*len(message) + 24, "Message is too long."
    
    # The first 24 bits encode the length of the message
    bitstream = np.concatenate([integer_to_bit_list(b) for b in message]).astype(np.uint8)
    message_len = len(bitstream)

    # Create list of bits containing message len + the message itself
    bitstream_metainfo = integer_to_bit_list(message_len, num_bytes=3)
    img_array_1d = img.reshape(height*width*channels)
    bit_array_1d = np.array([int(b) for b in bitstream_metainfo] + 
                            [int(b) for b in bitstream])
    
    # pad the bit array with the smallest bits with random bits such that the length matches the length of the flattened image
    bit_array_1d_padded = np.concatenate([bit_array_1d, 
                                          np.random.randint(0, 2, len(img_array_1d)-len(bit_array_1d))])
    bit_array_2d_padded = bit_array_1d_padded.reshape(img.shape)
    
    # Zero out the image bits that will be used to store the message
    bit_window = (np.ones(img.shape)*255 - (1<<bit_idx)).astype(np.uint8)

    return (img & bit_window) | (bit_array_2d_padded.astype('uint8')<<bit_idx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hide a file in an image.')
    parser.add_argument('filenames', metavar='N', type=str, nargs=2,
                        help='filenames of (1) the image (2) the file that will be hidden.')
    parser.add_argument('--bit_idx', '--b', default=0, type=int, help='index of bit where information will be store. (default: 0)')
    parser.add_argument('--out', '--t', default='encoded.png', type=str, help='filename of output image. (default: encoded.png)')
    args = parser.parse_args()

    img_file = args.filenames[0]
    message_file = args.filenames[1]
    bit_idx = args.bit_idx

    img = cv2.imread(img_file)

    with open(message_file, 'rb') as f:
        message = f.read()

    img_encoded = encode_img(img, message, bit_idx)
    cv2.imwrite(args.out, img_encoded)

