# Forensics 100 - Clams don't dance

> Writeup by feignix (Paras Chetal)

In this challenge we are provided with an image file. The file has messed up boot sectors which I detected ahd rebuilt using the `testdisk` tool. The contents of the repaired image file consisted of a `dance.mp4` video and a `clam.pptx` presentation. 

On using `unzip` on the clam.pptx file and analyzing the extracted contents, I found a MaxiCode [image](image0.gif) in it, which I scanned using a barcode reader [app](https://play.google.com/store/apps/details?id=com.funcode.decoder.bs). That gave me the flag.
