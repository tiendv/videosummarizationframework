from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import f1_score, precision_score, recall_score
predicted = [0,0,1,1,0,0,0,1,1,1,0,1]
y_test = [1,0,1,1,0,1,0,0,1,1,1,0]

precision, recall, fscore, support = score(y_test, predicted)

print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print(f1_score(y_test,predicted))
print(precision_score(y_test,predicted))
print(recall_score(y_test,predicted))
