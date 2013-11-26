from qrs_detector import QrsDetector
import matplotlib.pyplot as plt
import sys

record_file = "files/s20011"
if 1 in sys.argv:
    record_file = sys.argv[1]

qrs_detector = QrsDetector(record_file)

qrs_detector.read_file()
qrs_detector.high_pass_filter()
qrs_detector.low_pass_filter()
qrs_detector.qrs_detect()
qrs_detector.set_qrs_indexes()
qrs_detector.write_results()

# plot values
plt.figure(1)
plt.subplot(221)
plt.plot(qrs_detector.input_signal)
plt.xlabel('input signal')

plt.subplot(222)
plt.plot(qrs_detector.high_pass)
plt.xlabel('high pass')

plt.subplot(223)
plt.plot(qrs_detector.low_pass)
plt.xlabel('low pass')

plt.subplot(224)
plt.plot(qrs_detector.qrs)
plt.xlabel('qrs')

plt.show()