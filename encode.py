import cv2
import numpy as np
import argparse


def integer_to_bit_list(integer, num_bytes=1):
    return [integer >> i & 1 for i in range(num_bytes*8-1, -1, -1)]

def encode_img(img, message, bit_idx=0):
    width, height, channels = img.shape
    assert width*height*channels >= 8*len(message) + 24    
    
    # The first 24 bits encode the length of the message (2^24 is larger than the number of pixels in a 4k image)
    bitstream = np.concatenate([integer_to_bit_list(b) for b in message]).astype(np.uint8)
    message_len = len(bitstream)
    bitstream_metainfo = integer_to_bit_list(message_len, num_bytes=3)

    img_array_1d = img.reshape(height*width*channels)
    bit_array_1d = np.array([int(b) for b in bitstream_metainfo] + 
                            [int(b) for b in bitstream])
    
    # pad the bit array with the smallest bits from the remaining pixels in the image such that the length matches the length of the flattened image
    bit_array_1d_padded = np.concatenate([bit_array_1d, 
                                          np.random.randint(0, 2, len(img_array_1d)-len(bit_array_1d))])
    bit_array_2d_padded = bit_array_1d_padded.reshape(img.shape)
    
    bit_window = (np.ones(img.shape)*255 - (1<<bit_idx)).astype(np.uint8)
    
    return (img & bit_window) | (bit_array_2d_padded.astype('uint8')<<bit_idx)

# def pad_zeros(l, pad_to_length=8):
#     return '0'*(pad_to_length - len(l)) + l

# def char_to_bit_str(c):
#     return pad_zeros(bin(ord(c)).split('b')[1])

# def char_list_to_bitstream(cl):
#     cl_bins = [char_to_bit_str(c) for c in cl]
#     return ''.join(cl_bins)

# def encode_img(img, message, bit_idx=0):
#     message_char_list = [m for m in message]
#     width, height, channels = img.shape
#     assert width*height*channels >= 8*len(message_char_list) + 24
    
#     bitstream = char_list_to_bitstream(message_char_list)
    
#     # The first 24 bits encode the length of the message (2^24 is larger than the number of pixels in a 4k image)
#     message_len = len(bitstream)
#     bitstream_metainfo = pad_zeros(bin(message_len).split('b')[1], pad_to_length=24)

#     img_array_1d = img.reshape(height*width*channels)
#     bit_array_1d = np.array([int(b) for b in bitstream_metainfo] + 
#                             [int(b) for b in bitstream])
    
#     # pad the bit array with the smallest bits from the remaining pixels in the image such that the length matches the length of the flattened image
#     bit_array_1d_padded = np.concatenate([bit_array_1d, 
#                                           np.random.randint(0, 2, len(img_array_1d)-len(bit_array_1d))]) 
#     bit_array_2d_padded = bit_array_1d_padded.reshape(img.shape)
    
#     bit_window = (np.ones(img.shape)*255 - (1<<bit_idx)).astype(np.uint8)
    
#     return (img & bit_window) | (bit_array_2d_padded.astype('uint8')<<bit_idx)

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

