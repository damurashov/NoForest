#!/usr/bin/python3

from generic import *
import fnmatch


def git_commit_files(commit_hash: str):
	# git diff-tree --no-commit-id --name-only -r HEAD
	COMMAND = f'git diff-tree --no-commit-id --name-only -r {commit_hash}'
	return smart_split(command_output(COMMAND)[0])


def git_commit_hashes(commit_from, commit_to):
	cmd = f"git log --pretty=format:%h {commit_from}..{commit_to}"
	return smart_split(command_output(cmd)[0])


def git_is_ancestor(h1, h2) -> bool:
	command = f'git merge-base --is-ancestor {h1} {h2}'
	_, ret = command_output(command)
	return ret == 0


def git_establish_ancestry(hash1, hash2) -> str and str or None:
	"""
	:return: (ancestor, descendant), if there exists an ancestry. None otherwise
	"""
	if git_is_ancestor(hash1, hash2):
		return hash1, hash2
	elif git_is_ancestor(hash2, hash1):
		return hash2, hash1
	else:
		return None


def git_commits_by_file_pattern(commit_from, commit_to, pattern, match: bool, strict: bool):
	"""
	:param commit_from: begin
	:param commit_to: end
	:param pattern: file pattern
	:param match: files that match   vs   files that don't
	:param strict: include files that match   vs   only files that match
	:return:
	"""

	def git_condition_commits(hashes, bin_op, bin_op_base_operand: bool):
		"""
		The core function. Returns commit hashes satisfying given condition
		:param hashes:  {def123321, 314ad21, ...}
		:param bin_op:  def bin_op(base, operand): bool
		:param bin_op_base_operand:  bin_op_base_operand = bin_op(bin_op_base_operand, operand)
		:return:
		"""
		commits = []

		for hash in hashes:
			flag = bin_op_base_operand
			for file in git_commit_files(hash):
				flag = bin_op(flag, fnmatch.fnmatch(file, pattern))
			if flag:
				commits.append(hash)
		return commits

	def negation_trait(x):
		if match:
			return x
		else:
			return not x

	def binary_operation(base, operand):
		if strict:
			return base and negation_trait(operand)
		else:
			return base or negation_trait(operand)

	binary_operation_base = True if strict else False

	return git_condition_commits(git_commit_hashes(commit_from, commit_to), binary_operation, binary_operation_base)


def _git_get_files_change_type(commit_from, commit_to, change_type):
	"""

	:param commit_from:
	:param commit_to:
	:param change_type: see 'GIT_CHANGE_TYPE_..."
	:return:
	"""
	file_list, _ = command_output(f'git difftool {commit_from} {commit_to} --name-status')
	file_list = file_list.strip()
	file_list = file_list.split('\n')
	file_list = [f.strip() for f in file_list]

	file_list = [re.split('\s+', f) for f in file_list]

	file_list = list(filter(lambda f: f[0] == change_type, file_list))
	file_list = [f[1] for f in file_list]

	return file_list


def git_get_files_modified(commit_from, commit_to):
	return _git_get_files_change_type(commit_from, commit_to, 'M')


def git_get_files_added(commit_from, commit_to):
	return _git_get_files_change_type(commit_from, commit_to, 'A')
