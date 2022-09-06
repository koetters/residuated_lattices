import itertools
import inspect
import importlib
import sys

# Check if the user provides a residuated lattice
if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python endos.py <module_name>")
    exit(0)

# Load the residuated lattice
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
leq = lattice.leq

# ad hoc definition for "Expression" class (should probably be defined elsewhere, and maybe is unified with the axiom class)
class Expression:
    def __init__(self,predicate):
        self.predicate = predicate
        self.params = inspect.getargspec(self.predicate).args
        self.nparams = len(self.params)

    def __str__(self):
        return inspect.getsource(self.predicate)

# the function computes all endomorphisms of a residuated lattice
def endomorphisms():

    print("Endomorphisms:")

    # a list of expressions which together say that a given function f is an endomorphism
    expressions = [
        Expression(lambda x,y: f(meet(x,y)) == meet(f(x),f(y))),
        Expression(lambda x,y: f(join(x,y)) == join(f(x),f(y))),
        Expression(lambda x,y: f(prod(x,y)) == prod(f(x),f(y))),
        Expression(lambda x,y: f(arrow(x,y)) == arrow(f(x),f(y))),
        Expression(lambda : f(one) == one),
        Expression(lambda : f(zero) == zero),
    ]

    ndom = len(domain)
    result = []
    # iterate over all transformations on the domain (this can be quite a lot!)
    for values in itertools.product(domain,repeat=ndom):
        satisfied = True
        fdir = {x:y for x,y in zip(domain,values)}
        f = lambda x:fdir[x]
        # check if the transformation f is an endomorphism, by checking for each preservation property ...
        for exp in expressions:
            # ... whether it holds for all values of x and y (or whatever variables are applicable)
            for args in itertools.product(domain,repeat=exp.nparams):
                res = exp.predicate(*args)
                if not res:
                    satisfied = False
                    break
            if not satisfied:
                break
        # if all preservation properties are satisfied, include f in the list of endomorphisms
        if satisfied:
            result.append([(a,fdir[a]) for a in domain])
    # return the list of endomorphisms
    return result

# the function computes all (f,g)-derivations of a residuated lattice,
# for given endomorphisms f and g
def derivations(f,g):

    fdir = dict(f)
    gdir = dict(g)
    f = lambda x:fdir[x]
    g = lambda x:gdir[x]

    expressions = [
        # the definition of (f,g)-derivation
        Expression(lambda x,y: d(prod(x,y))==join(prod(d(x),f(y)),prod(g(x),d(y)))),
    ]

    ndom = len(domain)
    result = []
    # iterate over all transformations on the domain (this can be quite a lot!)
    for values in itertools.product(domain,repeat=ndom):
        satisfied = True
        ddir = {x:y for x,y in zip(domain,values)}
        d = lambda x:ddir[x]
        # check if the transformation d is an (f,g)-derivation ...
        for exp in expressions:
            # ... by checking if the definition holds for all values of x and y
            for args in itertools.product(domain,repeat=exp.nparams):
                res = exp.predicate(*args)
                if not res:
                    satisfied = False
                    break
            if not satisfied:
                break
        # if so, include d in the list of (f,g)-derivations
        if satisfied:
            print(str([(a,ddir[a]) for a in domain]))
            result.append([(a,ddir[a]) for a in domain])
    # return the list of (f,g)-derivations
    return result

# compute all endomorphisms, ...
endos = endomorphisms()
# ... list them on the screen, ...
for i,f in enumerate(endos):
    print(str(i+1)+") "+str(f))

i = None
j = None

# ... and ask the user to select f and g from that list
while True:
    iplus1 = int(input("Press number to select f:"))
    i = iplus1-1
    if 0<=i and i<len(domain):
        break
    else:
        print("Number out of range")

f = endos[i]
print("f="+str(f))

while True:
    jplus1 = int(input("Press number to select g:"))
    j = jplus1-1
    if 0<=j and j<len(domain):
        break
    else:
        print("Number out of range")

g = endos[j]
print("g="+str(g))

# Now that f and g have been chosen, compute the (f,g)-derivations
print("(f,g)-derivations:")
dlist = derivations(f,g)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))


