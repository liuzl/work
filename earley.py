# -*- encoding: utf-8 -*-

class Production(object):
    def __init__(self, *terms):
        self.terms = list(terms)
    def __len__(self):
        return len(self.terms)
    def __getitem__(self, index):
        return self.terms[index]
    def __iter__(self):
        return iter(self.terms)
    def __repr__(self):
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(tuple(self.terms))

class Rule(object):
    def __init__(self, name, *productions):
        self.name = name
        self.productions = list(productions)
    def __str__(self):
        return self.name
    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))
    def add(self, *productions):
        self.productions.extend(productions)

class State(object):
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % \
                (self.name, " ".join(terms), self.start_column, self.end_column)
    def __eq__(self, other):
        return (self.name, self.production, self.dot_index, self.start_column) == \
            (other.name, other.production, other.dot_index, other.start_column)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.name, self.production))
    def completed(self):
        return self.dot_index >= len(self.production)
    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dot_index]

class Column(object):
    def __init__(self, index, token):
        self.index = index
        self.token = token
        self.states = []
        self._unique = set()
    def __str__(self):
        return str(self.index)
    def __len__(self):
        return len(self.states)
    def __iter__(self):
        return iter(self.states)
    def __getitem__(self, index):
        return self.states[index]
    def enumfrom(self, index):
        for i in range(index, len(self.states)):
            yield i, self.states[i]
    def add(self, state):
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False
    def print_(self, completedOnly = False):
        print "[%s] %r" % (self.index, self.token)
        print "=" * 35
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print repr(s)
        print

class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def print_(self, level = 0):
        print "  " * level + str(self.value)
        for child in self.children:
            child.print_(level + 1)

def predict(col, rule): #操作当前Column
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col))

def scan(col, state, token): #操作下一个Column
    print state, token, col.token, token != col.token, type(token), type(col.token)
    if token != col.token: #col表示输入串，token是Rule里面next_term
        return
    col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

def complete(col, state): #操作当前Column
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        #如果来源state的dot位置是left-hand non-terminal，添加dot+1的st到当前Column
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

GAMMA_RULE = u"GAMMA"

def parse(rule, text):
    # word个数+1个Column
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
    table[0].add(State(GAMMA_RULE, Production(rule), 0, table[0]))

    # 对每一个token
    for i, col in enumerate(table):
        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule): #如果是non-terminals，需要predict
                    predict(col, term)
                elif i + 1 < len(table):
                    scan(table[i+1], state, term)
        
        #col.print_(completedOnly = True)
        col.print_(completedOnly = False)

    # find gamma rule in last table column (otherwise fail)
    for st in table[-1]:
        if st.name == GAMMA_RULE and st.completed():
            return st
    else:
        raise ValueError("parsing failed")

def build_trees(state):
    return build_trees_helper([], state, len(state.rules) - 1, state.end_column)

def build_trees_helper(children, state, rule_index, end_column):
    if rule_index < 0:
        return [Node(state, children)]
    elif rule_index == 0: #如果是rule的第一个non-terminal
        start_column = state.start_column
    else:
        start_column = None
    
    rule = state.rules[rule_index]
    outputs = []
    for st in end_column:
        if st is state:
            break
        #if st is state or not st.completed() or st.name != rule.name:
        if not st.completed() or st.name != rule.name:
            continue
        if start_column is not None and st.start_column != start_column:
            continue
        for sub_tree in build_trees(st):
            for node in build_trees_helper([sub_tree] + children, state, rule_index - 1, st.start_column):
                outputs.append(node)
    return outputs

