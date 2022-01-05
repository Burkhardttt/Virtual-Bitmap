import math
import random
import sys

import matplotlib.pyplot as plt
import numpy
from matplotlib.backends.backend_pdf import PdfPages


class VirtualBitmap:

    def __init__(self):
        self.num_of_flows = 8507
        self.num_of_bit_of_phy = 500000
        self.num_of_bit_of_vir = 500
        self.data = []
        self.true_size = []
        self.estimated_size = []
        self.random_500_nums = []
        self.a_random_num = random.randint(0, sys.maxsize)

        self.physical_bit_map = [0 for _ in range(self.num_of_bit_of_phy)]
        self.flow_ids = [0 for _ in range(self.num_of_flows)]

    def read_file(self):
        file = open("project4input.txt", 'r')
        for line in file:
            line = line.split()
            self.data.append(line)
        self.data = self.data[1:]
        file.close()

    def pre_processing(self):
        for i in range(self.num_of_flows):
            self.flow_ids[i] = hash(self.data[i][0])
            self.true_size.append(int(self.data[i][1]))

    def generate_random_nums(self):
        self.random_500_nums = random.sample(range(0, sys.maxsize), self.num_of_bit_of_vir)

    def recording(self):
        for i in range(self.num_of_flows):
            elements = random.sample(range(0, sys.maxsize), self.true_size[i])
            for element in elements:
                self.physical_bit_map[abs((self.random_500_nums[(element ^ self.a_random_num)
                % self.num_of_bit_of_vir] ^ self.flow_ids[i]) % self.num_of_bit_of_phy)] = 1

    def query(self):
        Vb = (self.num_of_bit_of_phy - sum(self.physical_bit_map)) / self.num_of_bit_of_phy
        log_Vb = math.log(Vb)

        for flow_id in self.flow_ids:
            num_of_zeros = 0
            for element in self.random_500_nums:
                if self.physical_bit_map[abs((element ^ flow_id) % self.num_of_bit_of_phy)] == 0:
                    num_of_zeros += 1
            Vf = num_of_zeros / self.num_of_bit_of_vir
            log_Vf = math.log(Vf)
            estimated = self.num_of_bit_of_vir * (log_Vb - log_Vf)
            if estimated < 0:
                self.estimated_size.append(0)
            else:
                self.estimated_size.append(estimated)

    def make_plot(self, true_size, estimated_size):
        x = true_size
        y = estimated_size
        plt.scatter(x, y, marker="+")
        parameter = numpy.polyfit(x, y, 1)
        f = numpy.poly1d(parameter)
        plt.plot(x, f(x), "r-")
        pp.savefig()
        plt.show()


if __name__ == '__main__':
    vb = VirtualBitmap()
    vb.read_file()
    vb.pre_processing()
    vb.generate_random_nums()
    vb.recording()
    vb.query()
    # making a plot
    pp = PdfPages('result.pdf')
    vb.make_plot(vb.true_size, vb.estimated_size)
    pp.close()

    doc = open("output4.txt", 'w')
    for i in range(len(vb.true_size)):
        print(str(vb.true_size[i]) + "  " + str(vb.estimated_size[i]))
        print(str(vb.true_size[i]) + "  " + str(vb.estimated_size[i]), file=doc)








