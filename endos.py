import itertools
import inspect
import importlib
import sys

if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python endos.py <module_name>")
    exit(0)

module_name = sys.argv[1]
module = importlib.import_module(module_name)
lattice = module.lattice

domain = lattice.domain
meet = lattice.meet
join = lattice.join
prod = lattice.prod
arrow = lattice.arrow
zero = lattice.zero
one = lattice.one

# derived functions
leq = lambda x,y: x == meet(x,y)

class Expression:
    def __init__(self,predicate):
        self.predicate = predicate
        self.params = inspect.getargspec(self.predicate).args
        self.nparams = len(self.params)

    def __str__(self):
        return inspect.getsource(self.predicate)

expressions = [
    Expression(lambda x,y: f(meet(x,y)) == meet(f(x),f(y))),
    Expression(lambda x,y: f(join(x,y)) == join(f(x),f(y))),
    Expression(lambda x,y: f(prod(x,y)) == prod(f(x),f(y))),
    Expression(lambda x,y: f(arrow(x,y)) == arrow(f(x),f(y))),
    Expression(lambda : f(one) == one),
    Expression(lambda : f(zero) == zero),
]

ndom = len(domain)
for values in itertools.product(domain,repeat=ndom):
    satisfied = True
    fdir = {x:y for x,y in zip(domain,values)}
    f = lambda x:fdir[x]
    for exp in expressions:
        for args in itertools.product(domain,repeat=exp.nparams):
            res = exp.predicate(*args)
            if not res:
                satisfied = False
                break
        if not satisfied:
            break
    if satisfied:
        print("endomorphism: "+str(fdir))

