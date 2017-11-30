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
model = mltree_check.check(y < 0, x1 > 0, x2 > 0, x3 > 0, x4 > 0)
if model:
    f = lambda x: float(x.numerator_as_long()) / float(x.denominator_as_long())
    x_pred = [f(model[x1]), f(model[x2]), f(model[x3]), f(model[x4])]
    print 'found counter example'
    print 'x = ', x_pred
    print 'y = ', clf.predict([x_pred])
else:
    print 'claim holds!'
