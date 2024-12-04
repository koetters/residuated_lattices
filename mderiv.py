import itertools
import importlib
import sys

if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python mderiv.py <module_name>")
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
leq = lattice.leq

####### endomorphisms #######

def check_endomorphism(f):

    for x in domain:
        for y in domain:
            if not ( {f[z] for z in meet(x,y)} <= meet(f[x],f[y]) ):
                return False
            if not ( {f[z] for z in join(x,y)} <= join(f[x],f[y]) ):
                return False
            if f[prod(x,y)] != prod(f[x],f[y]):
                return False
            if f[arrow(x,y)] != arrow(f[x],f[y]):
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

# the function computes all (f,g)-derivations of a residuated lattice,
# for given endomorphisms f and g
# note: definition of multi-supremum between sets: see e.g. article "The Prime Filter Theorem for Multilattices"
# note: definition of (f,g)-derivation via multi-supremum: where is this in the literature? is the definition wrong?
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

####### (f,g)-derivations (using the product) #######
# note: definition from article "(f,g)-derivation in residuated multilattices"
def check_derivation2(d,f,g):
    for x in domain:
        for y in domain:
            if not d[prod(x,y)] in join(prod(d[x],f[y]),prod(g[x],d[y])):
                return False
    return True

def derivations2(f,g):

    f = dict(f)
    g = dict(g)

    result = []
    # generate all possible choices of d (this can be quite a lot!)
    for values in itertools.product(domain,repeat=len(domain)):
        d = {x:y for x,y in zip(domain,values)}
        # if d is an (f,g)-derivation, append it to the list
        if check_derivation2(d,f,g):
            result.append([(a,d[a]) for a in domain])
    # return the list of (f,g)-derivations
    return result

####### implicative (f,g)-derivations #######

def check_implicative_derivation(d,f,g):
    for x in domain:
        for y in domain:
            if not d[arrow(x,y)] in join(arrow(d[x],f[y]),arrow(g[x],d[y])):
                return False
    return True

def implicative_derivations(f,g):

    f = dict(f)
    g = dict(g)

    result = []
    # generate all possible choices of d (this can be quite a lot!)
    for values in itertools.product(domain,repeat=len(domain)):
        d = {x:y for x,y in zip(domain,values)}
        # if d is an implicative (f,g)-derivation, append it to the list
        if check_implicative_derivation(d,f,g):
            result.append([(a,d[a]) for a in domain])
    # return the list of implicative (f,g)-derivations
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
    if 0<=i and i<len(domain):
        break
    else:
        print("Number out of range")

f = endos[i]
print("f="+str(f))

while True:
    jplus1 = int(input("Press number to select g:"))
    j = jplus1 - 1
    if 0<=j and j<len(domain):
        break
    else:
        print("Number out of range")

g = endos[j]
print("g="+str(g))

# Now that f and g have been chosen, compute the (f,g)-derivations
print("(f,g)-derivations (defined using multi-infimum; wrong definition?):")
dlist = derivations(f,g)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))

print("(f,g)-derivations (defined using product):")
dlist = derivations2(f,g)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))

print("implicative (f,g)-derivations:")
dlist = implicative_derivations(f,g)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))

print("implicative (g,f)-derivations:")
dlist = implicative_derivations(g,f)
for i,d in enumerate(dlist):
    print(str(i+1)+") "+str(d))

