import itertools
import inspect
import importlib
import sys

# Check if the user provides a residuated lattice
if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python check.py <module_name>")
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

# ad hoc definition for "Axiom" class (should probably be defined elsewhere)
class Axiom:
    def __init__(self,predicate):
        self.predicate = predicate
        self.params = inspect.getfullargspec(self.predicate).args
        self.nparams = len(self.params)

    def __str__(self):
        return inspect.getsource(self.predicate)

# The axioms for residuated lattices
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

# for every axiom, check if it is satisfied by the "residuated lattice" ...
naxiom = 0
for axiom in axioms:
    naxiom += 1
    satisfied = True
    # ... by evaluating it for all possible values of x,y,z (or whatever variables are applicable)
    for args in itertools.product(domain,repeat=axiom.nparams):
        res = axiom.predicate(*args)
        if not res:
            # if the axiom fails for some variables, print some details
            if satisfied:
                print(str(naxiom)+") Fail")
                print(axiom)
                satisfied = False
            print("    fails for "+str(tuple(axiom.params))+" = "+str(args))
    # otherwise, print a message indicating that the axiom is satisfied
    if satisfied:
        print(str(naxiom)+") Pass")

