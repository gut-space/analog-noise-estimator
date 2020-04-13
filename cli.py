import cv2

from noise_estimator.rating import gaussian_rating as rating
from noise_estimator.estimation import np_fftconvolve, estimate_in_boxes, estimate_noise
from noise_estimator import laplacians
from noise_estimator import metrics

def draw_noise(I, stats, box, metric="sigma"):
    '''
    Draw noise on image. Show division into boxes. Green circuit of box means
    low noise, red circuit means high noise. Requires original image @I,
    noise statistics @stats and @box size used to calculation.
    Sigma noise may be used directly @metric=sigma or may be rated using 
    normal distribution based rank when @metric=gauss (or something else).

    Display OpenCV window.
    '''
    for stat in sorted(stats, key=lambda s: s['noise']):
        start = (stat['col'], stat['row'])
        end = tuple([min(d + box, s) for d, s in zip(start, reversed(I.shape[:2]))])
        center = tuple([int(d + box / 2) for d in start])
        noise = stat['noise']

        if metric == "sigma":
            val = noise
            max_ = 40
            text = "%.0f" % (val,)
        else:
            rate = rating(noise)
            val = rate
            max_ = 1
            text = "%.1f" % (rate,)
        color = (0, 255 * (max_ - val) / max_, 255 * (val / max_))

        cv2.rectangle(I, start, end, color, 2)
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.25
        font_thickness = 1
        cv2.putText(I, text, center, font_face, font_scale, (0, 128, 255), font_thickness)

    window_title = "Noise"
    cv2.imshow(window_title, I)
    while cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) > 0:
        key = cv2.waitKey(50)
        if key == 27: # ESC
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to image file")
    parser.add_argument("-l", "--laplacian", choices=['3', '5', '7'], default='3', help="Laplacian")
    parser.add_argument("-c", "--conv", help="Convulsion function", choices=['numpy', 'scipy'], default='numpy')
    parser.add_argument("-m", "--metric", help="Metric to plot", choices=["sigma", "gauss"], default="sigma")
    parser.add_argument("-n", "--noise", help="Noise plot", default=False, action="store_true")
    parser.add_argument("-r", "--rating", help="Plot rating", default=False, action="store_true")
    parser.add_argument("-b", "--box", default=25, type=int, help="Box size")
    args = parser.parse_args()

    Ls = {
        '3': laplacians.L3,
        '5': laplacians.L5,
        '7': laplacians.L7
    }
    L = Ls[args.laplacian]
    
    if args.conv == 'numpy':
        conv2d = np_fftconvolve
    else:
        from scipy.signal import convolve2d
        conv2d = convolve2d
    
    path = args.path

    # Global recognition
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    sigma = estimate_noise(img, L, conv2d)

    # Local recognition
    box = args.box
    noise_stats = estimate_in_boxes(img, L, conv2d, box)
    noises = [s['noise'] for s in noise_stats]

    # Some metrics
    # Sigma - Gauss distribution parameter for describe 'size' ('area') of the noise)
    # Global value of sigma for whole image:
    print("Global sigma:", sigma)
    # Average of sigma in separate boxes
    print("Average local sigma:", metrics.average_sigma(noises))
    # Average of sigma in separate boxes, but sigma is cliped to 30.
    print("Average local sigma clip:", metrics.average_sigma_clip(noises, 30))
    # Rating calculated on global sigma
    print("Global rating:", rating(sigma))
    # Rating with constant threshold. 0 for sigma < 10, 0.5 for sigma < 20 otherwise 1.
    print("Constant metric:", metrics.constant_ranges_rating(noises))
    # Rating with linear value for sigma between 10 and 20.
    print("Linear metric:", metrics.linear_middle_range_rating(noises))
    # Rating based on normal distribution for sigma between 10 and 20.
    print("Gauss metric:", metrics.gauss_middle_range_rating(noises))
    
    # Plot noises
    if args.noise:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        draw_noise(img, noise_stats, box, args.metric)

    # Plot rating
    if args.rating:
        from matplotlib import pyplot as plt
        arr = range(0, 25)
        val = [rating(v) for v in arr]
        plt.plot(arr, val, 'r')
        plt.xticks(arr)
        plt.xlabel("Sigma")
        plt.ylabel("Rate")
        plt.title("Noise rating for gaussian sigma")
        plt.show()
