import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt

import findpeaks

x = np.linspace(0, 1, 1000)
y = np.sin(x*10)**2

peaks_idx, peaks_val = findpeaks.findpeaks(y)
print(peaks_idx)
print(peaks_val)

plt.plot(x, y)
plt.scatter(x[peaks_idx], peaks_val, color='red')
plt.show()

