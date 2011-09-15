import netroc
import yard, pylab

def plotComparison(trainfile,testfile,scorelist,labelList=None,method="roc"):
	nr = netroc.NetReader(trainfile,testfile)
	if labelList!=None:
		labels = labelList
	else:
		labels = []
	for scorefile in scorelist:
		scores = nr.makeScores(scorefile)
		d = yard.BinaryClassifierData(zip(scores,nr.getLabels()))
		if (method.upper()=='ROC'):
			result = yard.PrecisionRecallCurve(d)
		pylab.plot(map(lambda x:x[0],result.points),map(lambda x:x[1],result.points))
		if labelList==None:
			labels.append(scorefile)
	pylab.legend(labels)


