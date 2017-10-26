# -*_ encoding: utf-8 -*-
from util import *
from earley import *

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: %s <cfgfile>" % sys.arvv[0])
        sys.exit(1)
    rules = loadGrammar(sys.argv[1])
    st = parse(rules['<s>'], "3 4 . 1 9")
    trees = build_trees(st)
    for tree in trees:
        print("="*80)
        tree.print_()
