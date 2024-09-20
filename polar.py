from Polar_codes_BEC import Polar_bec
import pandas as pd
import csv
import matplotlib.pyplot as plt
import math

class CSV:
    CSV_FILE = 'polarized_data.csv'
    COLUMNS = ['p', 'n', 'useless_channels', 'perfect_channels', 'mediocre_channels', 'perfect_channels_fr', 'useless_channels_fr']
    @classmethod
    def inintialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    @classmethod
    def add_entry(cls, p, n, extreme_channels, extreme_channels_fr):
        new_entry = {
            'p': p,
            'n': n,
            'perfect_channels': extreme_channels[0],
            'useless_channels': extreme_channels[1], 
            'mediocre_channels': extreme_channels[2], 
            'perfect_channels_fr' : extreme_channels_fr[0],
            'useless_channels_fr' : extreme_channels_fr[1],
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)


def plotter(erasure, n, p):
    x = list(range(len(erasure)))
    y = erasure
    plt.scatter(x, y, c = '#3d5a80')
    plt.xlabel("Equivalent Channel index (sorted)", c = '#4CAF50', fontsize=14)
    plt.ylabel("Equivalent BEC Erasure probability", c = '#4CAF50', fontsize=14)
    plt.title(f"Equivalent Channel with ({int(math.log2(n))} Stages), ε = {p}", c = '#ef233c',fontsize=16)
    plt.show()

def number_extreme_channels(polarization, p):
    perfect_channels = list(filter(lambda x : x <= p , polarization))
    useless_channels = list(filter(lambda x : x >= 1-p , polarization))
    mediocre_channels = list(filter(lambda x : p <= x <= 1-p , polarization))
    return (len(perfect_channels) , len(useless_channels), len(mediocre_channels))

def fraction(n, polarization):
    perfect_channels = list(filter(lambda x : x <= 0.01 , polarization))
    useless_channels = list(filter(lambda x : x >= 0.99 , polarization))
    print(f"this is the no of perfect_channels: {len(perfect_channels)}")
    result1 = float(len(perfect_channels)/n)
    result2 = float(len(useless_channels)/n)
    p_channels = round(result1, 2)
    u_channels = round(result2, 2)
    return (p_channels , u_channels)
    # n >> 1 

def sum_of_all_epsilon(polarization):
    result = sum(polarization)
    print(f"sum of all epsilons: {result}")


def upper_bound_block_error(n, p):
    result = n * p
    print(f"the upper bound for block error: {result}")
    #block error probability(emre telatar)

def sum_of_good_channels(polarization, p):
    filter_good_channels = list(filter(lambda x: x < p , polarization))
    result = sum(filter_good_channels)
    print(f"sum of epsilon_good_channels: {result}")
    
def main():
    CSV.inintialize_csv()
    Polar_bec.__init__(0)
    (p,n)=Polar_bec.input_p_n(0)
    polarization = Polar_bec.BEC(p,n)
    polarization.sort()
    sum_of_all_epsilon(polarization)
    sum_of_good_channels(polarization, p)
    upper_bound_block_error(n, p)
    extreme_channels = number_extreme_channels(polarization, p)
    # print('****extreme_channels', type(extreme_channels))
    extreme_channels_fr = fraction(n, polarization)
    CSV.add_entry(p, n, extreme_channels, extreme_channels_fr)
    Polar_bec.BEC_graph(p,n)
    plotter(polarization, n, p)

if __name__ == '__main__':
    main()
