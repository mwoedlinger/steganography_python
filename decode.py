import cv2
import numpy as np
import argparse

def bin_to_dec(bl: list) -> list:
    """List of bit list to list of integers 
       e.g.: [[0,0,0,1,0,1,0], [0,0,0,1,0,1,1]] -> [10, 11]

    Args:
        bl (list): List of bit lists

    Returns:
        list: [description]
    """
    num_bits = len(bl[0])
    powers_of_two = 2**np.linspace(num_bits-1, 0, num_bits).reshape((1, num_bits))
    powers_of_two = np.repeat(powers_of_two, len(bl), axis=0)

    return (powers_of_two*bl).sum(axis=1)

def decode_img(img: np.array, bit_idx: int=0) -> list:
    
    # Extract relevant bits from image
    bit_window = np.ones(img.shape, dtype=np.uint8)<<bit_idx
    img_bitstream = (img & bit_window).flatten()>>bit_idx
    
    # Extract message length and message bitstream
    message_len = bin_to_dec([img_bitstream[:24]])[0]

    # Check if something went wrong (for example because the encoded image got compressed lossy)
    assert (message_len % 8 == 0), 'message length not divisible by 8.'

    # Process bit list
    message_bitstream = img_bitstream[24:(24 + int(message_len))]
    message_bytes = np.split(message_bitstream, len(message_bitstream)/8)    
    message_ints = bin_to_dec(message_bytes).astype(np.uint8)
    
    return message_ints


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract files from an encoded image.')
    parser.add_argument('filename', metavar='N', type=str, nargs=1,
                        help='filename of the encoded image')
    parser.add_argument('--bit_idx', '--b', default=0, type=int, help='index of bit where information will be store. (default: 0)')
    parser.add_argument('--out', '--o', default='message', type=str, help='filename of output image. (default: message)')
    args = parser.parse_args()

    img_file = args.filename[0]
    bit_idx = args.bit_idx
    out_file = args.out

    img = cv2.imread(img_file)
    decoded = decode_img(img, bit_idx)

    with open(out_file, 'wb') as f:
        message = f.write(decoded)