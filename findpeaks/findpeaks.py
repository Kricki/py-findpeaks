# see also: https://github.com/MonsieurV/py-findpeaks/blob/master/tests/libs/detect_peaks.py

from . import detect_peaks

__author__ = 'Kricki (https://github.com/Kricki)'
__version__ = "1.0.0"


def compute_peak_prominence(signal, peak_index):
    """ Computes the prominences for the peaks at positions peak_index in the 1d-signal.
    The peaks have to be detected with another routine before, see e.g. https://github.com/MonsieurV/py-findpeaks

    See https://mathworks.com/help/signal/ref/findpeaks.html for explanation of "Prominence".

    :param signal: An array containing the signal
    :param peak_index: Index positions of the peaks
    :return: Array with the prominences for each peak. Length of this array is the same as len(peak_index).
    """
    prominence = []
    left = 0
    right = 0
    for index in peak_index:
        peak_amp = signal[index]

        # extend horizontal line from the peak to the left
        for k in reversed(range(index)):
            left = k
            if signal[k] > peak_amp:  # we crossed the signal (there is higher value than the peak)
                break

        # extend horizontal line from the peak to the right
        for k in range(index+1, len(signal)):
            right = k
            if signal[k] > peak_amp:  # we crossed the signal (there is higher value than the peak)
                break

        # Find the minimum of the signal in each of the two intervals found above:
        # [left,index] and [index,right]. This point is either a valley or one of the signal endpoints.
        minimum_left = min(signal[left:index])
        minimum_right = min(signal[index:right])

        # The higher of the two interval minima specifies the reference level.
        # The height of the peak above this level is its prominence.
        prominence.append(abs(signal[index] - max([minimum_left, minimum_right])))
    return prominence


def findpeaks(signal, mph=None, mpd=1, threshold=0, mpp=None, edge='rising',
                 kpsh=False, valley=False):
    """ Detect peaks in data based on their amplitude and other features.

    :param signal: 1D array_like data.
    :param mph: {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    :param mpd: positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in units of array indexes)
    :param threshold: positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold` in relation to their immediate neighbors.
    :param mpp: {None, positive number}, optional (default = None)
        Minimum peak prominence (see e.g. https://mathworks.com/help/signal/ref/findpeaks.html)
    :param edge: {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    :param kpsh: bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    :param valley: bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    :return: An array with indexes of found peaks, and an array with signal values on the peak locations.
    """

    # Using the "valley=True" option in detect_peaks does not work in combination with the prominence computation.
    # Instead, we simply invert the signal.
    signal_temp = signal
    if valley:
        signal_temp = -signal

    # use detect_peaks to detect peaks in the input signal x
    peak_index = detect_peaks.detect_peaks(signal_temp, mph, mpd, threshold, edge, kpsh)

    if mpp is not None:
        # compute the prominences for the peaks, and discard peaks that have prominence below mpp
        prominence = compute_peak_prominence(signal_temp, peak_index)
        peak_index = [peak_index[k] for k in range(len(peak_index)) if prominence[k] >= mpp]

    peak_signal = [signal[k] for k in peak_index]

    return peak_index, peak_signal
