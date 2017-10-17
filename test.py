# -*- encoding: utf-8 -*-
from earley import *

if __name__ == "__main__":
    N = Rule("N", Production("time"), Production("flight"), Production("banana"), Production("flies"), Production("boy"), Production("telescope"))
    D = Rule("D", Production("the"), Production("a"), Production("an"))
    V = Rule("V", Production("book"), Production("eat"), Production("sleep"), Production("saw"))
    P = Rule("P", Production("with"), Production("in"), Production("on"), Production("at"), Production("through"))

    PP = Rule("PP")
    NP = Rule("NP", Production(D, N), Production(N), Production("john"), Production("houston"))
    NP.add(Production(NP, PP))
    PP.add(Production(P, NP))

    VP = Rule("VP", Production(V, NP))
    VP.add(Production(VP, PP))
    S = Rule("S", Production(NP, VP), Production(VP))

    for tree in build_trees(parse(S, "john saw the boy with telescope")):
        print "--------------------------"
        tree.print_()

    print repr(N)
    print repr(VP)
    print repr(S)
    print repr(PP)
