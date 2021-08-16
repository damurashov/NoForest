# https://mermaid-js.github.io/mermaid/#/flowchart?id=flowcharts-basic-syntax

from functools import reduce


def _code_connection(src, dest):
	return ' '.join(['\t', str(src), '-->', str(dest)])


def _code_header(configuration):
	if configuration not in ['TB', 'TD', 'BT', 'RL', 'LR']:
		configuration = 'TD'
	return ' '.join(['graph', configuration])


def mrm_gen_graph(configuration, *pairs):
	"""
	:param configuration: TB, TD, BT, RL, LR
	:param pairs: (A, B), (A, C), (B, C), ...
	:return: mermaid code
	"""
	header = _code_header(configuration)
	graph = [_code_connection(*pair) for pair in pairs]
	return '\n'.join([header] + graph) + '\n\t' + '\n\t'.join(list(set(reduce(lambda a, b: a + b, pairs, ()))))


if __name__ == "__main__":
	print(mrm_gen_graph("TD", (1, 2), (3, 4), (2, 4)))