class Node(object):
	"""
	Class for nodes in the tree. Some care needs to be taken when creating
	children and setting parent nodes.
	"""

	def __init__(self, parent=None, parent_label=None):
		self.parent = parent
		self.children = []
		self.labels = []
		self.parent_label = parent_label

	def _add_child(self, child):
		self.children.append(child)

	def _add_label(self, label):
		self.labels.append(label)

	def add_edge(self, node, label):
		self._add_child(node)
		self._add_label(label)
		node.parent = self
		node.parent_label = label

	def delete_edge(self, node, label):
		self.children.remove(node)
		self.labels.remove(label)


class SuffixTree(object):
	original_string = None
	root = None

	def __init__(self, original_string):
		# Append money sign to the end so no suffix is a substring of any other 
		# suffix.
		self.root = Node()
		self.original_string = original_string + '$'
		self.naive_algorithm()

	def __str__(self):
		output_string = ""
		nodes = []
		nodes.append(self.root)

		while nodes:
			current_node = nodes.pop(0)

			if current_node.children:
				output_string += str(current_node.labels) + "\n"
				nodes.extend(current_node.children)

		return output_string

	def walk_tree(self, node, suffix):
		if suffix:
			matching_label = None
			child_index = 0
			for (i, label) in enumerate(node.labels):
				if label[0] == suffix[0]:
					matching_label = label
					child_index = i
					break

			if matching_label:
				split_index = None
				for i in range(1, min(len(matching_label), len(suffix))):
					if matching_label[i] != suffix[i]:
						split_index = i
						break

				if not split_index:
					# meaning we matched the whole edge label.
					return self.walk_tree(node.children[child_index], suffix[i+1:])
				else:
					return node, child_index, split_index, suffix[split_index:]
			else:
				#no match, so the best matching node is the original.
				return node, None, None, suffix
		else:
			# As is, this should not be called
			return node, None, None, suffix

	def add_suffix(self, suffix):
		# walk down from root as far as possible.
		node, child_index, split_index, label = self.walk_tree(self.root, suffix)
		if split_index:
			split_node = Node()
			leaf = Node()
			split_node.add_edge(leaf, label)

			child = node.children[child_index]
			split_label = node.labels[child_index]
			split_node.add_edge(child, split_label[split_index:])
			node.add_edge(split_node, split_label[:split_index])

			node.delete_edge(child, split_label)
		else:
			leaf = Node()
			node.add_edge(leaf, label)

	def naive_algorithm(self):
		"""
		Create the suffix tree using the O(n^2) naive algorithm. This is done mainly
		for comparing results with the more efficient algorithm, and to test the 
		design of my data structures.
		"""
		for i in range(len(self.original_string)):
			suffix = self.original_string[i:]
			self.add_suffix(suffix)


class UkkonenNode(Node):
	skip_node = None


class UkkonenTree(object):

	def __init__(self, original_string):
		# Append money sign to the end so no suffix is a substring of any other 
		# suffix.
		self.root = UkkonenNode()
		self.original_string = original_string + '$'
		self.ukkonen()

	def walk_tree(self, node, suffix):
		if suffix:
			matching_label = None
			child_index = 0
			for (i, label) in enumerate(node.labels):
				if label[0] == suffix[0]:
					matching_label = label
					child_index = i
					break

			if matching_label:
				if len(suffix) < len(matching_label):
					# eat up the suffix
					return node, child_index, len(suffix) - 1
				else:
					return self.walk_tree(node.children[child_index], suffix[len(matching_label):])
			else:
				# This shouldn't happen.
				print 'This is a mistake'
		else:
			return node, None, 0

	def apply_rule_one(self):
		# just add string to label
		pass

	def apply_rule_two(self):
		#	create new label, and a new leaf
		pass

	def apply_rule_three(self):
		# do nothing
		pass


	def ukkonen(self):
		"""
		Construct a suffix tree in linear time using Ukkonen's algorithm. This 
		constructs an implicit suffix once for each index in the original string. 
		Each implicit suffix tree depends on the previous suffix tree to speed up
		the construction. The algorithm is made linear by a few not-so-complicated 
		tricks (see Gusfield et al).
		"""

		for i in range(len(self.original_string)):
			# Construct the implicit suffix tree for the prefix S[1..i]
			for j in range(1, i+1): 
				# These indices are bound to be wrong
				# This will need changed in order to actually get the linear running 
				# time.
				prefix = self.original_string[j:i]

				# apply one of the three rules to create suffix S[j..i+1]
				node, child_index, last_index = self.walk_tree(self.root, prefix)

				if child_index:
					label = node.labels[child_index]

					if len(label) > len(prefix):
						if label[last_index+1] == self.original_string[i+1]:
							self.apply_rule_three()

				if not child_index:
					self.apply_rule_one()
				elif some_case:
					self.apply_rule_two()
				else:
					self.apply_rule_three()
					# break
		

def main():
	print SuffixTree("banana")

if __name__ == "__main__":
	main()