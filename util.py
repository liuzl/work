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
        lhs = two[0].strip()
        rhs = two[1].strip()
        if lhs[0] != '<' or lhs[-1] != '>': continue
        if lhs not in rules:
            rules[lhs] = Rule(lhs)
        for prods in two[1].split("|"):
            p = Production()
            for tok in prods.split(" "):
                tok = tok.strip()
                if tok == "": continue
                if tok[0] == '<' and tok[-1] == '>':
                    if tok not in rules:
                        rules[tok] = Rule(tok)
                    p.terms.append(rules[tok])
                else:
                    p.terms.append(tok)
            rules[lhs].add(p)
    return rules

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: %s <cfgfile>" % sys.argv[0])
        sys.exit(1)
    rules = loadGrammar(sys.argv[1])

    for tree in build_trees(parse(rules['<S>'], "john saw the boy with telescope")):
        print "--------------------------"
        tree.print_()
