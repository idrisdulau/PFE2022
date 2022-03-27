#------------------------------------------------------------------
# Code written by Idris DULAU, Rodin DUHAYON and Guillaume DUBRASQUET-DUVAL.
# Adapted from https://github.com/Chiaraplizz/ST-TR.
# For the use of Dr. Marie Beurton-Aimar and Phd. student Kévin Réby.
#------------------------------------------------------------------

import numpy as np
from . import tools

# Joint index:
# {0,  "Waist"}
# {1,  "Spine"},
# {2,  "Chest"},
# {3,  "Neck"},
# {4,  "Head"},
# {5,  "Head tip"},
# {6,  "LeftCollar"},
# {7,  "Leftupperarm"},
# {8,  "Leftforearm"},
# {9,  "Lefthand"},
# {10,  "RightCollar"},
# {11,  "Rightupperarm"},
# {12,  "Rightforearm"},
# {13,  "Righthand"},
# {14,  "Leftupperleg"},
# {15,  "Leftlowerleg"},
# {16,  "Leftfoot"},
# {17,  "Leftlegtoes"},
# {18,  "Rightupperleg"},
# {19,  "Rightlowerleg"},
# {20,  "Rightfoot"},
# {21,  "Rightlegtoes"},

# Edge format: (origin, neighbor)
num_node = 22
self_link = [(i, i) for i in range(num_node)]
inward = [(5, 4), (4, 3), (3, 6), (6, 7), (7, 8), (8, 9), (3, 10), (10, 11),
          (11, 12), (12, 13), (3, 2), (2, 1), (1, 0), (0, 14), (14, 15), (15, 16),
          (16, 17), (0, 18), (18, 19), (19, 20), (20, 21)]
outward = [(j, i) for (i, j) in inward]
neighbor = inward + outward


class Graph():

    def __init__(self, labeling_mode='uniform'):
        self.A = self.get_adjacency_matrix(labeling_mode)
        self.num_node = num_node
        self.self_link = self_link
        self.inward = inward
        self.outward = outward
        self.neighbor = neighbor

    def get_adjacency_matrix(self, labeling_mode=None):
        if labeling_mode is None:
            return self.A
        if labeling_mode == 'uniform':
            A = tools.get_uniform_graph(num_node, self_link, neighbor)
        elif labeling_mode == 'distance*':
            A = tools.get_uniform_distance_graph(num_node, self_link, neighbor)
        elif labeling_mode == 'distance':
            A = tools.get_distance_graph(num_node, self_link, neighbor)
        elif labeling_mode == 'spatial':
            A = tools.get_spatial_graph(num_node, self_link, inward, outward)
        elif labeling_mode == 'DAD':
            A = tools.get_DAD_graph(num_node, self_link, neighbor)
        elif labeling_mode == 'DLD':
            A = tools.get_DLD_graph(num_node, self_link, neighbor)
        else:
            raise ValueError()
        return A


def main():
    mode = ['uniform', 'distance*', 'distance', 'spatial', 'DAD', 'DLD']
    np.set_printoptions(threshold=np.nan)
    for m in mode:
        print('=' * 10 + m + '=' * 10)
        print(Graph(m).get_adjacency_matrix())


if __name__ == '__main__':
    main()