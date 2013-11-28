'''
@author: drazen
'''

import random
import pywfdb


class QrsDetector:
    def __init__(self, record_file):
        self.input_signal = []
        self.high_pass = []
        self.low_pass = []
        self.qrs = []
        self.qrs_indexes = []
        self.n_samples = 0
        self.m = 5
        self.record_file = record_file

    def read_file(self):
        record = pywfdb.Record(self.record_file)

        if len(record.signal_names) > 0:
            signal_type = record.signal_names[0]

            self.input_signal = record.read(signal_type, 0)
            self.n_samples = len(self.input_signal)

    def high_pass_filter(self):
        self.high_pass = [None]*self.n_samples
        constant = float(1/self.m)

        for i in range(0, self.n_samples):
            y1 = 0
            y2 = 0

            y2_index = i-((self.m+1)/2)

            if y2_index < 0:
                y2_index += self.n_samples

            y2 = self.input_signal[y2_index]

            y1_total = 0
            for j in range(i, i-self.m, -1):
                x_index = i - (i-j)

                if x_index < 0:
                    x_index += self.n_samples

                y1_total += self.input_signal[x_index]

            y1 = constant * y1_total

            self.high_pass[i] = y2 - y1

    # on n index write square of 30 numbers inside frame
    def low_pass_filter(self):
        self.low_pass = [None]*self.n_samples

        for i in range(0, self.n_samples):
            total = 0

            if i+30 < self.n_samples:
                for j in range(i, i+30):
                    current = self.high_pass[j]**2
                    total += current
            elif i+30 >= self.n_samples:
                over = i+30 - self.n_samples

                for j in range(i, self.n_samples):
                    current = self.high_pass[j]**2
                    total += current

                for j in range(0, over):
                    current = self.high_pass[j]**2
                    total += current

            self.low_pass[i] = total

    def qrs_detect(self):
        self.qrs = [None]*self.n_samples
        threshold = 0
        frame = 250

        for i in range(0, 200):
            if self.low_pass[i] > threshold:
                threshold = self.low_pass[i]

        for i in range(0, self.n_samples, frame):
            added = False
            max = 0
            index = i + frame

            if index > self.n_samples:
                index = self.n_samples

            for j in range(i, index):
                if self.low_pass[j] > max:
                    max = self.low_pass[j]

            for j in range(i, index):
                if (self.low_pass[j] > threshold) and not added:
                    self.qrs[j] = 1
                    self.qrs_indexes.append(j)
                    added = True
                else:
                    self.qrs[j] = 0

            gama = 0.15 if random.random() > 0.5 else 0.20
            alpha = 0.01 + (random.random() * (0.1 - 0.01))

            threshold = alpha * gama * max + (1 - alpha) * threshold

    def write_results(self):
        f = open(self.record_file + '.det', 'w')

        for i in range(0, len(self.qrs_indexes)):
            f.write('0:00:00.00 %s N 0 0 0\n' % self.qrs_indexes[i])

        f.close()
