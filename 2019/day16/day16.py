import numpy as np

def parse(s):
    return np.array(list(s)).astype(int)

base_pattern = np.r_[0, 1, 0, -1]

def fft(signal):
    N = len(signal)
    output = np.empty_like(signal)
    for i in range(N):
        pattern = np.repeat(base_pattern, 1+i)
        repeats_needed = int(np.ceil((N + 1) / len(pattern)))
        repeats_needed += 1  # TODO just for good measure in lieu of testing...
        tiled_pattern = np.tile(pattern, repeats_needed)
        actual_pattern = tiled_pattern[1:][:N]
        output[i] = np.abs((actual_pattern * signal).sum()) % 10
    return output

def fft_mat(N, start=0):
    output = np.empty((N-start, N-start), dtype=int)
    for i in range(start, N):
        pattern = np.repeat(base_pattern, 1+i)
        repeats_needed = int(np.ceil((N + 1) / len(pattern)))
        repeats_needed += 1  # TODO just for good measure in lieu of testing...
        tiled_pattern = np.tile(pattern, repeats_needed)
        output[i-start, :] = tiled_pattern[1:][start:N]
    return output

def fft_100(signal):
    N = len(signal)
    A = fft_mat(N)
    for _ in range(100):
        signal = np.abs(A @ signal) % 10
    return signal

input_str = '59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848'

def print_digits(arr):
    print(''.join(map(str, arr.tolist())))

def part1():
    signal = parse(input_str)
    result = fft_100(signal)[:8]
    print_digits(result)

def fft_end(signal):
    # the end of the matrix is just an upper-triangular of ones
    # so the last element doesn't actually change
    # we can just work backwards
    # all digits are positive
    output = signal
    count = 0
    for i in range(len(output)-1, -1, -1):
        count += output[i]
        output[i] = count % 10
    return output

from tqdm import trange
def fft_end_100(signal):
    for _ in trange(100):
        signal = fft_end(signal)
    return signal

def part2():
    signal_str = input_str * 10000
    offset = int(signal_str[:7])
    signal = parse(signal_str)
    L = len(signal) - offset
    signal_end = fft_end_100(signal[- 2 * L - 2:])
    result = signal_end[-L:-L+8]
    print_digits(result)
