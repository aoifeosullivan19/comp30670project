import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

#print(matplotlib.get_backend())

plt.plot(range(10))

plt.savefig('test.png')
