import itertools
import importlib
import sys

if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python deriv.py <module_name>")
    exit(0)

module_name = sys.argv[1]
module = importlib.import_module(module_name)
lattice = module.lattice

domain = lattice.domain
meet = lattice.meet
join = lattice.join
leq = lattice.leq

####### endomorphisms #######

def check_endomorphism(f):

    for x in domain:
        for y in domain:
            if not ( {f[z] for z in meet(x,y)} <= meet(f[x],f[y]) ):
                return False
            if not ( {f[z] for z in join(x,y)} <= join(f[x],f[y]) ):
                return False
    return True

# the function computes all endomorphisms of a residuated lattice
def endomorphisms():

    result = []
    # generate all possible choices of f (this can be quite a lot!)
    for values in itertools.product(domain,repeat=len(domain)):
        f = {x:y for x,y in zip(domain,values)}
        if check_endomorphism(f):
            result.append([(a,f[a]) for a in domain])
    # return the list of endomorphisms
    return result

####### (f,g)-derivations #######

def check_derivation(d,f,g,lookup):
    for x in domain:
        for y in domain:
            if not ({d[z] for z in meet(x,y)} <= lookup[(d[x],f[y],f[x],d[y])]):
                return False

    return True

# the function computes all (f,g)-derivations of a multilattice, for given endomorphisms f and g
# note: definition of multi-supremum between sets: see e.g. article "The Prime Filter Theorem for Multilattices"
def derivations(f,g):

    f = dict(f)
    g = dict(g)

    lookup = {}
    for r in domain:
        for s in domain:
            for t in domain:
                for u in domain:
                    lookup[(r,s,t,u)] = set().union(*(join(x,y) for x in meet(r,s) for y in meet(t,u)))

    result = []
    # generate all possible choices of d (this can be quite a lot!)
    for values in itertools.product(domain,repeat=len(domain)):
        d = {x:y for x,y in zip(domain,values)}
        # if d is an (f,g)-derivation, append it to the list
        if check_derivation(d,f,g,lookup):
            result.append([(a,d[a]) for a in domain])
    # return the list of (f,g)-derivations
    return result

# compute all endomorphisms, ...
print("Endomorphisms:")
endos = endomorphisms()
# ... list them on the screen, ...
for i,f in enumerate(endos):
    print(str(i+1)+") "+str(f))

i = None
j = None

# ... and ask the user to select f and g from that list
while True:
    iplus1 = int(input("Press number to select f:"))
    i = iplus1 - 1
    if 0<=i and i<len(endos):
        break
    else:
        print("Number out of range")

f = endos[i]
print("f="+str(f))

while True:
    jplus1 = int(input("Press number to select g:"))
    j = jplus1 - 1
    if 0<=j and j<len(endos):
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

