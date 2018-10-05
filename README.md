# Cyclic Codes

Implementation of self-correcting cycling codes with python. First attempt with Hamming codes.

I discovered Coding Theory during a semester abroad in Novosibirsk State University. There, I coded my first attempt of self correcting code. This first attempt worked, but had some issues : it was not handling all possible generator polynomials for one Hamming Code with given parameter m, it was not handling parameters m > 4, all was only design to work on a finite field of cardinal 2, and so on...

As a result, I wanted to code it again, making it more general : this is the core goal of the repo.
Moreover, I conceive this repo as a little "laboratory" on cyclic codes.
## How to use the repo ?

The first step is to compute the pairs of generators/check polynomials for the wanted set of (m, q) pairs, where m is the parameter of the Hamming Code ```(2^m-1,2^m-m-1,3)``` over the finite field ```Fq``` .
To do this, just run **hcodebuilder.py**. You can modify the predefined set of (m, q) pairs by editing **hcodebuilder.py** .

Then, try to code and decode messages !
 + Encoding/decoding words in ```Fq```, with the small Human-Machine interface. Run **smallihm.py**, and let the script guide you ! you may either encode/decode single words, or proceed by batches.
 + Encoding/decoding texts. The end of **Coder.py** alows you to write a text, then code and decode it !

Remember that each time you'll have to choose which polynomial pair you'll use for the coding procedure
