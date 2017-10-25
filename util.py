# -*- encoding: utf-8 -*-
from earley import *

def loadGrammar(filename):
    rules = {}
    for line in open(filename):
        pos = line.find('#')
        if pos > 0: line = line[:pos]
        line = line.strip()
        if len(line) == 0: continue
        two = line.split("->")
        if len(two) != 2 or len(two[0]) == 0 or len(two[1]) == 0:
            continue
        if two[0][0] != '<' or two[0][-1] != '>': continue
        if two[0] not in rules:
            rules[two[0]] = Rule(two[0])
        for prods in two[1].split("|"):
            p = Production()
            for tok in prods.split(" "):
                if tok == "": continue
                if tok[0] == '<' and tok[-1] == '>':
                    if tok not in rules:
                        rules[tok] = Rule(tok)
                    p.terms.append(rules[tok])
                else:
                    p.terms.append(tok)
            rules[two[0]].add(p)
    return rules

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: %s <cfgfile>" % sys.argv[0])
        sys.exit(1)
    rules = loadGrammar(sys.argv[1])

    #for tree in build_trees(parse(rules['<S>'], "john saw the boy with telescope")):
    for tree in build_trees(parse(rules['<S>'], "john saw boy")):
        print "--------------------------"
        tree.print_()
