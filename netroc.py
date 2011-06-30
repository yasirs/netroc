import yard
import random

def __iterable__(some_object):
	try:
		some_object_iterator = iter(some_object)
		return True
	except TypeError, te:
		return False

def writeTest(alledges,ftrain,ftest,frac=0.1,delimiter='\t'):
	"""
	writeTest(alledges,ftrain,ftest,frac=0.1,delimiter='\t')
	where,
		alledges: filename or iterable fo all edges to be divided into training and test edges
		ftrain : filename to write training edges
		ftest : filename to write postive test set edges
		frac : fraction of edges to include in test
		delimiter : delimiter used in input file, the output files always use tabs
	"""
	nodes = set()
	nlines = 0
	if type(alledges) is str:
		eiter = iter(open(alledges,'r'))
	elif __iterable__(alledges):
		eiter = iter(eiter)
	else:
		raise TypeError("edges need to be given as a filename or iterable")
	for e in eiter:
		nlines = nlines +1
	shufinds = range(nlines)
	random.shuffle(shufinds)
	if type(alledges) is str:
		eiter = iter((line.rstrip().split(delimiter) for line in open(alledges,'r')))
	elif __iterable__(alledges):
		eiter = iter(eiter)
	testinds = set(shufinds[:ntest])

	i = 0
	for e in eiter:
		if i not in testinds:
			nodes.update(e[:2])
		i = i+1

	if type(alledges) is str:
		eiter = iter((line.rstrip().split(delimiter) for line in open(alledges,'r')))
	elif __iterable__(alledges):
		eiter = iter(eiter)

	with open(ftrain,'w') as train:
		with open(ftest,'w') as test:
			i = 0
			for e in eiter:
				if i in testinds:
					if all((x in nodes for x in e[:2])):
						test.write('\t'.join(e))
				else:
					assert(all((x in nodes for x in e[:2])))
					train.write('\t'.join(e))
			i = i+1


class NetReader(object):
	"""
	class NetReader to read test and training edges and write scores for use in performance comparison
	>>> tredges = [[1,2], [3,4], [1,3], [2,4], [5,6], [7,8], [5,7], [6,8], [5,8], [8,1]]
	>>> testedges = [[1,4], [2,3], [6,7]]
	>>> net = NetReader(tredges, testedges)
	>>> partial_scores = [[6,7,0.4],[7,2,0.3],[1,4,0.5]]
	>>> labels = net.getLabels()
	>>> scores = net.makeScores(partial_scores)
	>>> scores
	[0, 0.5, 0.29999999999999999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.40000000000000002, 0, 0, 0, 0]
	>>> labels
	[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

	"""
	def __init__(self,trainingedges,testedges,delimiter='\t'):
		nodes = set()
		if type(trainingedges) is str:
			fi = open(trainingedges,'r')
			for line in fi:
				words = line.rstrip().split(delimiter)
				nodes.add(words[0]); verts.add(words[1])
			fi.close()
			self._nodes = sorted(nodes)
			self._node2i = dict(zip(self._nodes,range(len(self._nodes))))
			self._numNodes = len(self._nodes)
			self._trainedges = []
			fi = open(trainingedges,'r')
			for line in fi:
				words = line.rstrip().split(delimiter)
				self._trainedges.append(self.nPair2Ind(words[:2]))
		elif __iterable__(trainingedges):
			for e in trainingedges:
				nodes.add(e[0]); nodes.add(e[1])		
			self._nodes = sorted(nodes)
			self._node2i = dict(zip(self._nodes,range(len(self._nodes))))
			self._numNodes = len(nodes)
			self._trainedges = map(self.nPair2Ind,trainingedges)
		else:
			raise TypeError("trainingedges needs to be filename or iterable")

		if type(testedges) is str:
			self._tetedges = []
			fi = open(testedges,'r')
			for line in fi:
				words = line.rstrip().split(delimiter)
				self._testedges.append(self.nPair2Ind(words[:2]))
			self._testedges = set(self._testedges)
		elif __iterable__(testedges):
			self._testedges = set(map(self.nPair2Ind,testedges))
		else:
			raise TypeError("testedges needs to be filename or iterable")
		self._allLabels = [0] * ((self._numNodes*(self._numNodes-1))/2)
		for t in self._testedges:
			self._allLabels[t]=1
		self._allLabels = [self._allLabels[i] for i in xrange(len(self._allLabels)) if i not in self._trainedges]

	def makeScores(self,scores,delimiter='\t'):
		scoreVec = [0 for i in xrange((self._numNodes*(self._numNodes-1))/2)]
		if type(scores) is str:
			fi = open(scores,'r')
			for line in fi:
				w = line.rstrip().split(delimiter)
				scoreVec[self.nPair2Ind(w[:2])] = float(w[2])
		elif __iterable__(scores):
			for w in scores:
				scoreVec[self.nPair2Ind(w[:2])] = float(w[2])
		else:
			raise TypeError("scores need to be filename or iterable")
		scoreVec = [scoreVec[i] for i in xrange(len(scoreVec)) if i not in self._trainedges]
		return scoreVec
	def getLabels(self):
		return self._allLabels
					
	def nPair2Ind(self,x):
		return ((self._node2i[x[1]]-1)*self._node2i[x[1]])/2 + self._node2i[x[0]]

