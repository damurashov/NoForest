#!/usr/bin/python3

"""
Usage: s_gen_mermaid.py  branch1  branch2  branch3  ...
"""

from mermaid import mrm_gen_graph
from git_wrapper import git_is_ancestor
import sys
from numpy import matmul
from itertools import product


# def _form_ancestry_pairs(*branches):
# 	ancestors = [git_establish_ancestry(*pair) for pair in combinations(branches, 2)]
# 	ancestors = [pair for pair in ancestors if pair is not None]
# 	return ancestors


def _reachability_matrix(branches : list) -> list:
	"""
	:param branches: list of branch names
	:return: square matrix denoting ancestry of branches
	"""
	mat = [[0] * len(branches) for _ in range(len(branches))]  # Stub, square matrix

	# Establish reachability using git
	for i, ibranch in enumerate(branches):
		for j, jbranch in enumerate(branches):
			if i != j:
				mat[i][j] = int(git_is_ancestor(ibranch, jbranch))

	return mat


def _tree(reachability_matrix):
	"""
	:return: Transforms reachability_matrix to a spanning tree
	"""
	sz = len(reachability_matrix)

	def clean_redundant_adjacencies(reach_iter):
		for i in range(sz):
			for j in range(sz):
				if reachability_matrix[i][j] and reach_iter[i][j]:
					reachability_matrix[i][j] = 0

	n_iters = len(reachability_matrix)
	rm_iter = reachability_matrix

	for i in range(2, n_iters + 1):
		rm_iter = matmul(reachability_matrix, rm_iter)
		clean_redundant_adjacencies(rm_iter)

	return reachability_matrix


if __name__ == "__main__":
	assert len(sys.argv) > 2
	GRAPH_CONFIGURATION = "TD"  # Top-down

	branches = list(set(sys.argv[1:]))  # Ensure uniqueness
	sz = len(branches)
	matrix = _tree(_reachability_matrix(branches))
	pairs = [(branches[i], branches[j],) for i, j in product(range(sz), repeat=2) if matrix[i][j]]

	nodes = sys.argv[1:]
	print(mrm_gen_graph(GRAPH_CONFIGURATION, *pairs) + '\n\t' + '\n\t'.join(nodes))
