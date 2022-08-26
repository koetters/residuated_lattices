import itertools
import inspect
import importlib
import sys

if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python check.py <module_name>")
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

class Axiom:
    def __init__(self,predicate):
        self.predicate = predicate
        self.params = inspect.getargspec(self.predicate).args
        self.nparams = len(self.params)

    def __str__(self):
        return inspect.getsource(self.predicate)

# axioms
axioms = [
    ### bounded lattice ###
    # associative laws
    Axiom(lambda x,y,z: meet(x,meet(y,z)) == meet(meet(x,y),z)),
    Axiom(lambda x,y,z: join(x,join(y,z)) == join(join(x,y),z)),

    # commutative laws
    Axiom(lambda x,y: meet(x,y) == meet(y,x)),
    Axiom(lambda x,y: join(x,y) == join(y,x)),

    # absorption laws
    Axiom(lambda x,y: join(x,meet(x,y)) == x),
    Axiom(lambda x,y: meet(x,join(x,y)) == x),

    # neutral elements
    Axiom(lambda x: meet(x,one) == x),
    Axiom(lambda x: join(x,zero) == x),

    ### commutative ordered monoid ###
    # associative law
    Axiom(lambda x,y,z: prod(x,prod(y,z)) == prod(prod(x,y),z)),

    # commutative law
    Axiom(lambda x,y: prod(x,y) == prod(y,x)),

    # neutral element
    Axiom(lambda x: prod(x,one) == x),

    # compatibility
    Axiom(lambda x,y,z: leq(x,y) <= leq(prod(x,z),prod(y,z))),

    ### adjunction ###
    Axiom(lambda x,y,z: leq(z,arrow(x,y)) == leq(prod(x,z),y)),
]

naxiom = 0
for axiom in axioms:
    naxiom += 1
    satisfied = True
    for args in itertools.product(domain,repeat=axiom.nparams):
        res = axiom.predicate(*args)
        if not res:
            if satisfied:
                print(str(naxiom)+") Fail")
                print(axiom)
                satisfied = False
            print("    fails for "+str(tuple(axiom.params))+" = "+str(args))
    if satisfied:
        print(str(naxiom)+") Pass")

