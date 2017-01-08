import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from time import time

clf = RandomForestClassifier(n_estimators=10)

# use a full grid over all parameters
param_grid = {
	"max_depth": [3,4,5,6, None],
	"max_features": [3,4,5],
	"min_samples_split": [2,5,10],

	"min_samples_leaf": [1, 3, 10],
	"bootstrap": [True, False],
	"criterion": ["gini", "entropy"]
}

# run grid search
def best_model(X, y, clf=clf, param_grid=param_grid):
	grid_search = GridSearchCV(clf, param_grid=param_grid)
	start = time()
	model = grid_search.fit(X, y)
	print "GridSearchCV took %.2f seconds for %d candidate parameter settings." % (time() - start, len(grid_search.cv_results_['params']))
	return model
