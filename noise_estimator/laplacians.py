# Different Laplacian kernels. Bigger kernels produce bigger values, but
# doesn't improve results in my opinion. L3 is recommended.
# Kernels from ImageMagic doc: http://www.imagemagick.org/Usage/convolve/#log
L3 = [[ 1, -2,  1],
      [-2,  4, -2],
      [ 1, -2,  1]]
L5 = [[-4, -1, 0, -1, -4],
      [-1,  2, 3,  2, -1],
      [ 0,  3, 4,  3,  0],
      [-1, 2,  3,  2, -1],
      [-4, -1, 0, -1, -4]]
L7 = [[-10, -5, -2, -1, -2, -5, -10],
      [ -5,  0,  3,  4,  3,  0,  -5],
      [ -2,  3,  6,  7,  6,  3,  -2],
      [ -1,  4,  7,  8,  7,  4,  -1],
      [ -2,  3,  6,  7,  6,  3,  -2],
      [ -5,  0,  3,  4,  3,  0,  -5],
      [-10, -5, -2, -1, -2, -5, -10]]
