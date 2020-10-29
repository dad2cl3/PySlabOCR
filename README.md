## PySlabOCR

Basic Python 3 script that manages scans of trading cards graded by [PSA](https://www.psacard.com).

### How It Works

The Python script assumes that the user has scanned (and cropped) images of the front and back of a slabbed trading card. The ordering of the files ***MUST*** be sequential with the front scan followed by the back scan for the same card with no files between. The files must also be named in such a way as to allow ordering by name. It is recommended to utilize a timestamp in the name of the scanned files to ensure sort order is accurate.

The script will load the configuration file and use the defined paths to read the directory where the raw scans are located and order them in ascending order by file name. It will then attempt to read the front scan to locate the PSA certification number utilizing the [pytesseract](https://github.com/madmaze/pytesseract) library. The library is a Python wrapper for [Google's Tesseract-OCR engine](https://github.com/tesseract-ocr/tesseract). The script will try to identify the certification number using Regular Expressions in the characters read by pytesseract. If the scan is unsuccessful, the script will pop up an image preview window containing the front scan and prompt the user to manually enter the certification number.

Once the certification number is captured, the script will create two additional images. The first is a simple side-by-side composite of the front and back scans left to right, respectively. The second is a square side-by-side composite of the front and backs scan left to right, respectively. The background of the square image is black where a border around one dimension of the composite scans is present.

### Examples
1. Standard - 3 1/8" x 5 5/16"

Front Scan
![Front Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/standard/25015763-1-Front.png)

Back Scan
![Back Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/standard/25015763-2-Back.png)

Composite
![Composite](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/standard/25015763-3-Composite.png)

Square composite
![Square](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/standard/25015763-4-Square.png)

2. Small Tallboy - 4 3/16" x 7 3/16"

Front Scan
![Front Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-small/44235825-1-Front.png)

Back Scan
![Back Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-small/44235825-2-Back.png)

Composite
![Composite](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-small/44235825-3-Composite.png)

Square composite
![Square](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-small/44235825-4-Square.png)

3. Large Tallboy - 4 9/16" x 9 1/2"

Front Scan
![Front Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-large/21152460-1-Front.png)

Back Scan
![Back Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-large/21152460-2-Back.png)

Composite
![Composite](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-large/21152460-3-Composite.png)

Square composite
![Square](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/tallboy-large/21152460-4-Square.png)

4. Medium - 6 5/8" x 10 1/8"

Front Scan
![Front Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/medium/45450481-1-Front.png)

Back Scan
![Back Scan](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/medium/45450481-2-Back.png)

Composite
![Composite](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/medium/45450481-3-Composite.png)

Square composite
![Square](https://github.com/dad2cl3/PySlabOCR/blob/master/samples/medium/45450481-4-Square.png)

5. Jumbo - 9 13/16" x 13 3/16" - Too large for scanner so no examples available
