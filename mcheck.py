import itertools
import importlib
import sys

if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python mcheck.py <module_name>")
    exit(0)

module_name = sys.argv[1]
module = importlib.import_module(module_name)

lattice = module.lattice
domain = lattice.domain
meet = lattice.meet
join = lattice.join
prod = lattice.prod
arrow = lattice.arrow
one = lattice.one
zero = lattice.zero
leq = lattice.leq

# check whether "lattice" is a residual multilattice
# note: we can skip a few checks: if "lattice" is a poset, it is also a finite poset, and thus a multilattice
def check():
    for x in domain:
        # order: check reflexivity
        if not leq(x,x):
            print(f"Failure (Order, Reflexivity): x={x}")
            return False
        # order: check top element
        if not leq(x,one):
            print(f"Failure (Order, Top Element): x={x}")
            return False
        # order: check bottom element
        if not leq(zero,x):
            print(f"Failure (Order, Bottom Element): x={x}")
            return False
        # multiplication: check neutral element
        if prod(x,one) != x:
            print(f"Failure (Multiplication, Neutral Element): x={x}")
            return False
        for y in domain:
            # order: check antisymmetry
            if x != y and leq(x,y) and leq(y,x):
                print(f"Failure (Order, Antisymmetry): x={x}, y={y}")
                return False
            # multiplication: check commutative law
            if prod(x,y) != prod(y,x):
                print(f"Failure (Multiplication, Commutative Law): x={x}, y={y}")
                return False
            for z in domain:
                # order: check transitivity
                if leq(x,y) and leq(y,z) and not leq(x,z):
                    print(f"Failure (Order, Transitivity): x={x}, y={y}, z={z}")
                    return False
                # multiplication: check associative law
                if prod(x,prod(y,z)) != prod(prod(x,y),z):
                    print(f"Failure (Multiplication, Associative Law): x={x}, y={y}, z={z}")
                    return False
                # check adjunction
                if leq(prod(x,y),z) != leq(x,arrow(y,z)):
                    print(f"Failure (Adjunction): x={x}, y={y}, z={z}")
                    return False
    return True

if check():
    print("Success: This is a multilattice")
else:
    print("Failure: This is not a multilattice")

