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

#a = "a"
#b = "b"
#c = "c"
#fdir = {0:0,a:a,b:a,c:1,1:1}
#f = lambda x:fdir[x]
#gdir = {0:0,a:c,b:c,c:1,1:1}
#g = lambda x:gdir[x]


def endomorphisms():

    print("Endomorphisms:")

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
            result.append([(a,fdir[a]) for a in domain])
    return result

def derivations(f,g):

    fdir = dict(f)
    gdir = dict(g)
    f = lambda x:fdir[x]
    g = lambda x:gdir[x]

    expressions = [
        Expression(lambda x,y: d(prod(x,y))==join(prod(d(x),f(y)),prod(g(x),d(y)))),
    ]

    ndom = len(domain)
    result = []
    for values in itertools.product(domain,repeat=ndom):
        satisfied = True
        ddir = {x:y for x,y in zip(domain,values)}
        d = lambda x:ddir[x]
        for exp in expressions:
            for args in itertools.product(domain,repeat=exp.nparams):
                res = exp.predicate(*args)
                if not res:
                    satisfied = False
                    break
            if not satisfied:
                break
        if satisfied:
            result.append([(a,ddir[a]) for a in domain])
    return result

endos = endomorphisms()
for i,f in enumerate(endos):
    print(str(i+1)+") "+str(f))

i = None
j = None

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

print("(f,g)-derivations:")
dlist = derivations(f,g)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))


