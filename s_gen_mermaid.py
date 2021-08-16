#!/usr/bin/python3

"""
Usage: s_gen_mermaid.py  branch1  branch2  branch3  ...
"""

from mermaid import mrm_gen_graph
from git_wrapper import tree
import sys
from numpy import matmul
from itertools import product


# def _form_ancestry_pairs(*branches):
# 	ancestors = [git_establish_ancestry(*pair) for pair in combinations(branches, 2)]
# 	ancestors = [pair for pair in ancestors if pair is not None]
# 	return ancestors


if __name__ == "__main__":
	assert len(sys.argv) > 2
	GRAPH_CONFIGURATION = "TD"  # Top-down

	branches = list(set(sys.argv[1:]))  # Ensure uniqueness
	sz = len(branches)
	matrix = tree(branches)
	pairs = [(branches[i], branches[j],) for i, j in product(range(sz), repeat=2) if matrix[i][j]]

	nodes = sys.argv[1:]
	print(mrm_gen_graph(GRAPH_CONFIGURATION, *pairs))
