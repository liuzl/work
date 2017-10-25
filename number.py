# -*_ encoding: utf-8 -*-
from util import *
from earley import *

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: %s <cfgfile>" % sys.arvv[0])
        sys.exit(1)
    rules = loadGrammar(sys.argv[1])
    st = parse(rules['<s>'], "1 9 . 3")
    print st
    trees = build_trees(st)
    print len(trees)
    for tree in trees:
        print("="*80)
        tree.print_()
