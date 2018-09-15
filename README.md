# Cyclic Codes

Implementation of self-correcting cycling codes with python. First attempt with Hamming codes.

I discovered Coding Theory during a semester abroad in Novosibirsk State University. There, I coded my first attempt of self correcting code. This first attempt worked, but had some issues : it was not handling all possible generator polynomials for one Hamming Code with given parameter m, it was not handling parameters m > 4, all was only design to work on a finite field of cardinal 2, and so on...

As a result, I wanted to code it again, making it more general : this is the core goal of the repo.
