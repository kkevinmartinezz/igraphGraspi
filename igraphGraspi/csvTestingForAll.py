import csv
import sys
from fileinput import filename

import igraph_testing as ig

def main():
    filename_10 = sys.argv[1]
    # filename_50 = sys.argv[2]
    # filename_100 = sys.argv[3]
    # filename_500 = sys.argv[4]
    # filename_1000 = sys.argv[5]
    g = ig.generateGraph(filename_10)
    with open('Current_Test.csv', 'w', newline='') as file:
        field = ["n", " n2", " Graph creation", " Connected Components", " Shortest Path", " total",
                 " Memory Usage"]
        writer = csv.writer(file)
        f = "{:<5} {:<8} {:<24} {:<24} {:<24} {:<24} {:<24}".format(*field)
        writer.writerow([f])
        n = ig.read_file_size_n("testFile-10-2D.txt")
        dimensions = 2
        data = ig.run_all_three_functions(filename_10, g)
        n_2 = n * n
        total_time = data[0] + data[1] + data[3]
        row = f"{n:<5} {n_2:<8} {data[0]:<24} {data[1]:<24} {data[2]:<24} {total_time:<24} {data[3]:<24}"
        writer.writerow([row])

if __name__ == '__main__':
    main()