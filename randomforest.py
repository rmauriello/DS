# 
# Titanic survivor prediction contest
#
# ) random forest
#          Results: 0.858956076795, 0.78469  747 of 4540
# ) SVM
# ) Regression (Ridge, Lasso, IRLS, logistic)
# ) Naive Bayes
# ) k nearest neighbors

import pandas as pd
import numpy as np
import scipy as sp
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

# 
# Evaluation function: log-loss
#          The logarithm of the likelihood function for a Bernoulli random distribution.
#      Values range from 0 - 
#
def llfun(act, pred):
    epsilon = 1e-15
    pred = sp.maximum(epsilon, pred)
    pred = sp.minimum(1-epsilon, pred)
    ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
    ll = ll * -1.0/len(act)
    return ll

def main():
    # Create the training & test sets
    dataset = pd.read_csv('Data/train.csv')          # load dataframe 
    test = pd.read_csv('Data/test.csv').drop(['name', 'ticket', 'cabin','embarked'], axis=1)

    target = dataset.survived.values                 # y_train
    train  = dataset.drop(['survived','name', 'ticket', 'cabin','embarked'], axis=1)      # X_train, i.e. removed labels
    
    test[test.sex == 'male'] = np.float(1)
    test[test.sex == 'female'] = np.float(2)
    
    train[train.sex == 'male'] = np.float(1)
    train[train.sex == 'female'] = np.float(2)
    
 
    # Create and train the random forest
    # n_jobs of -1 will use the number of cores present on your system.   
    rfc = RandomForestClassifier(n_estimators=100,verbose=1)
  
    # Simple K-Fold cross validation with 10 folds.
    # 1) Creates 10 folds, each with 10% of training data
    # 2) Aggregate results (e.g. logloss) into a list
    cv = cross_validation.KFold(len(train), n_folds=10, indices=False)
    results = []
    for traincv, testcv in cv:
        #  Fit then predict using random forest 
        probas = rfc.fit(train[traincv], target[traincv]).predict_proba(train[testcv])
        #probas = rfc.fit(train, target).predict_proba(train)

        results.append( llfun(target[testcv], [x[1] for x in probas]) )

    #print out the mean of the cross-validated results and submit
    print "Results: " + str( np.array(results).mean() )

    if np.array(results).mean() > 0.5:
#        predicted_probs = [x[1] for x in rfc.predict(test)]
        predicted_probs = pd.Series(rfc.predict(test))
        predicted_probs.to_csv('Data/submission.csv', index=False, float_format="%f")




if __name__ == "__main__":
    main()