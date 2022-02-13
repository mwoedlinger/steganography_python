import cv2
import numpy as np
import argparse

def bin_to_dec(bl: list, total_bits: int=8):
    # e.g.: [[0,0,0,1,0,1,0], [0,0,0,1,0,1,1]] -> [10, 11]
    powers_of_two = 2**np.linspace(total_bits-1, 0, total_bits).reshape((1, total_bits))
    powers_of_two = np.repeat(powers_of_two, len(bl), axis=0)
    return (powers_of_two*bl).sum(axis=1)

def decode_img(img, bit_idx=0):
    
    width, height, channels = img.shape
    
    bit_window = np.ones(img.shape, dtype=np.uint8)<<bit_idx
    img_bitstream = (img & bit_window).flatten()>>bit_idx
    
    message_len = bin_to_dec([img_bitstream[:24]], total_bits=24)[0]
    message_bitstream = img_bitstream[24:(24 + int(message_len))]
    
    assert (len(message_bitstream) % 8 == 0), 'message bitstream not divisible by 8.'
    message_bytes = np.split(message_bitstream, len(message_bitstream)/8)
    
    message_ints = bin_to_dec(message_bytes).astype(np.uint8)
    
    return message_ints

# def bits_to_ints(bl: list, total_bits: int=8):
#     # e.g.: [[0,0,0,1,0,1,0], [0,0,0,1,0,1,1]] -> [10, 11]
#     powers_of_two = 2**np.linspace(total_bits-1, 0, total_bits).reshape((1, total_bits))
#     powers_of_two = np.repeat(powers_of_two, len(bl), axis=0)
#     return (powers_of_two*bl).sum(axis=1)

# def decode_img(img, bit_idx=0):
    
#     width, height, channels = img.shape
    
#     bit_window = np.ones(img.shape, dtype=np.uint8)<<bit_idx
#     img_bitstream = (img & bit_window).flatten()>>bit_idx
    
#     message_len = bits_to_ints([img_bitstream[:24]], total_bits=24)[0]
#     print(int(message_len))
#     message_bitstream = img_bitstream[24:(24 + int(message_len))]
    
#     assert (len(message_bitstream) % 8 == 0), 'message bitstream not divisible by 8.'
#     message_chars = np.split(message_bitstream, len(message_bitstream)/8)
    
#     message_ints = bits_to_ints(message_chars).astype(np.uint8)
#     message_character_list = [chr(m) for m in message_ints]
    
#     return ''.join(message_character_list)



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