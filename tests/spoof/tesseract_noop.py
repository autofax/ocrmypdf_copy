#!/usr/bin/env python3
import sys
import img2pdf
from PIL import Image


"""Tesseract no-op spoof

To quickly run tests where getting OCR output is not necessary.

In 'hocr' mode, create a .hocr file that specifies no text found.

In 'pdf' mode, convert the image to PDF using another program.

In orientation check mode, report the orientation is upright.
"""


VERSION_STRING = '''tesseract 3.04.00
 leptonica-1.72
  libjpeg 8d : libpng 1.6.19 : libtiff 4.0.6 : zlib 1.2.5
SPOOFED
'''

HOCR_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <title></title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name='ocr-system' content='tesseract 3.02.02' />
  <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word'/>
 </head>
 <body>
  <div class='ocr_page' id='page_1' title='image "x.tif"; bbox 0 0 {0} {1}; ppageno 0'>
   <div class='ocr_carea' id='block_1_1' title="bbox 0 1 {0} {1}">
    <p class='ocr_par' dir='ltr' id='par_1' title="bbox 0 1 {0} {1}">
     <span class='ocr_line' id='line_1' title="bbox 0 1 {0} {1}"><span class='ocrx_word' id='word_1' title="bbox 0 1 {0} {1}"> </span>
     </span>
    </p>
   </div>
  </div>
 </body>
</html>'''


def main():
    if sys.argv[1] == '--version':
        print(VERSION_STRING, file=sys.stderr)
        sys.exit(0)
    elif sys.argv[1] == '--list-langs':
        print('List of available languages (1):\neng', file=sys.stderr)
        sys.exit(0)
    elif sys.argv[-1] == 'hocr':
        inputf = sys.argv[-3]
        output = sys.argv[-2]
        with Image.open(inputf) as im, \
                open(output + '.hocr', 'w', encoding='utf-8') as f:
            w, h = im.size
            f.write(HOCR_TEMPLATE.format(str(w), str(h)))
    elif sys.argv[-1] == 'pdf':
        inputf = sys.argv[-3]
        output = sys.argv[-2]
        pdf_bytes = img2pdf.convert([inputf], dpi=300)
        with open(output + '.pdf', 'wb') as f:
            f.write(pdf_bytes)
    elif sys.argv[-1] == 'stdout':
        inputf = sys.argv[-2]
        print("""Orientation: 0
Orientation in degrees: 0
Orientation confidence: 100.00
Script: 1
Script confidence: 100.00""", file=sys.stderr)
    else:
        print("Spoof doesn't understand arguments", file=sys.stderr)
        print(sys.argv, file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
