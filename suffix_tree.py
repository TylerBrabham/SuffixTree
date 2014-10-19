class Node(object):
	"""
	Class for nodes in the tree. Some care needs to be had when creating children
	and setting parent nodes.
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
		return str(self.root.labels) + str(self.root.children[0].labels)

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

def main():
	print SuffixTree("aab")

if __name__ == "__main__":
	main()