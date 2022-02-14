# steganography_python
Simple python project to hide any file in an image.

From wikipedia: "Steganography is the practice of concealing a message within another message or a physical object. In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video." ([Link](https://en.wikipedia.org/wiki/Steganography))

This project allows to conceal an arbitrary file in an image by modifying one bit for every pixel. The resulting image contains is typically indistinguishable from the original image with the naked eye. For a given image the maximal message_file size is 8*3*width*height* - 24 ("-24" because we use 3 bytes, i.e. 24 bits, to save the length of the encoded file). This implementation only work with lossless compression (e.g. png), lossy compression might change the pixel values which leads to a corrupted message.

## Requirements

The project requires an active python environmen with numpy and opencv-python:

```
python3 -m venv env
source env/bin/activate
pip install opencv-python numpy
```

## Quickstart

Encode the complete text of shakespeare's Hamlet in a portrait of Shakespeare:

```
python encode.py assets/images/shakespeare.png assets/messages/shakespeare.txt --out shakespeare_with_hamlet.png
```

Extract the hidden text message from the encoded image:

```
python decode.py shakespeare_with_hamlet.png --out hamlet.txt
```

## Encoding

To encode a file "message_file" in an image "image_file":

```
python encode.py image_file message_file
```

optional arguments:

    --bit_idx       specify the index where the information is hidden. 
                    bit_idx=0 hides the message in the least imporant bit, 
                    bit_idx=1 hides the message in the second least important bit, etc. 
                    (default: 0)
    --out           Name of output image file 
                    (default: encoded.png)

## Decoding

To decode an image file "image_file":

```
python decode.py image_file
```

optional arguments:

    --bit_idx       specify the index where the information is encoded (see encode.py). 
                    (default: 0)
    --out           Name of output file 
                    (default: message)

(Modifying the image between encoding and decoding, for example by compressing the image with a lossy compression algorithm like jpg, will results in a corruption of the saved image. For small or localized corruption like adding some pixel values the decode method will still be able to extract a message, albait with some bits corrupted. That is, except if the first 24 bits are corrupted where the message length is saved. One could probably improve this by adding extra bits and error correcting code.)
