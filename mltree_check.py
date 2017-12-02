# encoding: utf-8
# Copyright (C) 2017 John Törnblom

import z3


class Walker(object):
    symtab = None
    feature_names = None
    
    def __init__(self, feature_names=None):
        self.symtab = dict()
        self.feature_names = feature_names
        if feature_names is not None:
            for name in feature_names:
                self.symtab[name] = z3.Real(name)
            
    def accept(self, tree, parent_id, node_id):
        left_id = tree.children_left[node_id]
        right_id = tree.children_right[node_id]
        
        if left_id < 0 or right_id < 0:
            return self.terminal(tree, node_id)

        sym = self.symbol(tree, node_id)
        cond = sym <= tree.threshold[node_id]
        iftrue = self.accept(tree, node_id, left_id)
        iffalse = self.accept(tree, node_id, right_id)
        return [z3.If(cond, t, f) for t, f in zip(iftrue, iffalse)]
        
    def terminal(self, tree, node_id):
        if tree.n_outputs != 1:
            raise Exception('Unsupported value type in terminal')

        return tree.value[node_id][0, :]
    
    def symbol(self, tree, node_id):
        idx = tree.feature[node_id]
        if idx < 0:
            idx += tree.n_features

        if self.feature_names is None:
            name = 'x%d' % (idx + 1)
        else:
            name = self.feature_names[idx]

        if not name in self.symtab:
            self.symtab[name] = z3.Real(name)
            
        return self.symtab[name]


def translate(tree, feature_names=None, target_names=None):
    w = Walker(feature_names)
    symbols = dict()
    res = w.accept(tree.tree_, 0, 0)
    for idx, y in enumerate(res):
        if  target_names is None:
            name = 'y%d' % (idx+1)
        else:
            name = target_names[idx]
            
        symbols[name] = y
        
    symbols.update(w.symtab)
    return symbols


def check(*args):
    s = z3.Solver()
    s.add(*args)
    res = s.check()
    if res.r > 0:
        return s.model()
