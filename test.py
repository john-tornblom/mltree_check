# encoding: utf-8
# Copyright (C) 2017 John Törnblom

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

import mltree_check


# Training
iris = load_iris()
clf = DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

# Theorem proving
symbols = mltree_check.translate(clf, ['x1', 'x2', 'x3', 'x4'])
globals().update(symbols)

# A sample shall be classified into exactly one class
model = mltree_check.check(y1 != 0 and y2 == 0 and y3 == 0,
                           y1 == 0 and y2 != 0 and y3 == 0,
                           y1 == 0 and y2 == 0 and y3 != 0)

def f(x):
    if x:
        num = float(x.numerator_as_long())
        den = float(x.denominator_as_long())
        return num / den
    else:
        return 0.0
    
if model:
    x_pred = [f(model[x1]), f(model[x2]), f(model[x3]), f(model[x4])]
    print 'found counter example'
    print 'x = ', x_pred
    print 'y = ', list(clf.predict([x_pred]))
else:
    print 'claim holds!'
