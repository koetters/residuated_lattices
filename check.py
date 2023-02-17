import itertools
import inspect
import importlib
import sys

# This Python script (i.e. "check.py") is executed with the command "python check.py <module>", where <module> is the name of a module
# (and <module>.py is the name of the corresponding module file, which defines the module).
# For example, if the command is "python check.py example1_6", then "example1_6" is the name of the module, and "example1_6.py" is the module file.
# The variable "sys.argv" gives access to the parts of the command following "python"; if the script was e.g. called with "python check.py example1_6",
# sys.argv is the list ["check.py","example1_6"], containing the script name and the arguments (i.e. the words following the script name).
# Uncommenting the next two lines (and then running the script) causes Python to print sys.argv and then stop execution (via "exit(0)").
#print(sys.argv)
#exit(0)

# We expect that the script is run with one argument (the module name). If sys.argv contains less than 2 arguments, this means the module
# name is missing: We print an error message and then stop execution.
if len(sys.argv) < 2:
    print("Missing parameter")
    print("Usage: python check.py <module_name>")
    exit(0)

# If we get to this point, we know that sys.argv has (at least) two elements, i.e. a module name is given.
# It is the second element of the list sys.argv, accessed by "sys.argv[1]" (the first element would be accessed by "sys.argv[0]")
# So we store the module name in the variable "module_name" ...
module_name = sys.argv[1]
# ... and then import the module with the line below. This has the same effect as the four "import [...]" statements at the very beginning
# of this script (in particular, "import sys" was needed for getting access to "sys.argv"), but we can not import the module in the same way,
# because every time script is executed, there can be a different module name, so we need to import the module in a different way
# (this is called a "dynamic import").
module = importlib.import_module(module_name)
# The "module" variable above gives access to the module (or more precisely, Python's internal representation of the module).
# Uncommenting the next two lines causes Python to print some information about the module (the module name, and the path where
# the module file is stored on the computer) and then exit.
#print(module)
#exit(0)
# We can get other, potentially more useful information: dir(module) provides a list of the things defined by the module.
# E.g. if the module is "example1_6" (see the module file "example1_6.py"), these are the objects "a","b","c","domain","prod_matrix"
# and "lattice", which are explicitly defined in that file; also the class "ResiduatedLattice", which was not defined in the file,
# but imported in the first line (from the "residuated_lattice" module); and finally a few other objects, whose names start and end
# with double underscores (like "__builtins__" etc.); the latter were added by Python and are not important now.
#print(dir(module))
#exit(0)

# As we have seen, the module provides an object called "lattice". This is the residuated lattice defined by the model.
# Below, we introduce shorter variable names, for convenience: the variable "lattice" then gives access to that lattice,
# and the other variables provide shorter names for its most important attributes and methods (as defined by the "Residuated Lattice" class
# in the "residuated_lattice" module).
lattice = module.lattice
domain = lattice.domain
meet = lattice.meet
join = lattice.join
prod = lattice.prod
arrow = lattice.arrow
zero = lattice.zero
one = lattice.one
leq = lattice.leq

# The following class describes axioms. The __init__ method below is a special method, called a "constructor",
# which is called whenever an object of the "Axiom" class is generated. We can see that it defines three attributes,
# that each axiom has: predicate, params and nparams. We can also see that the first of these attributes, predicate,
# is passed as an argument to the constructor. Before we have a more detailed look at these attributes, we have a look
# at the 13 different objects belonging to the "Axiom" class, which are defined in the "axioms" list further down ...
class Axiom:
    def __init__(self,predicate):
        self.predicate = predicate
        self.params = inspect.getfullargspec(self.predicate).args
        self.nparams = len(self.params)

    def __str__(self):
        return inspect.getsource(self.predicate)

# ... which is here! Every expression of the form "Axiom(f)" generates an "Axiom" object, where the function f is the "predicate" argument
# that is expected by the "__init__" constructor. More precisely, it is expected that f is a function which returns "True" or "False",
# depending on the arguments (like "x", "y" and "z" for a function with three arguments). In each case, we define f as a so-called
# "lambda" function, which is a short way of defining simple functions in Python; the more conventional way is to define functions
# with the "def" keyword, as we have done above. As an example of a lambda function, we have a look at the first one below,
# which defines the associative law for the meet operation. We can see that it has three parameters, "x", "y" and "z".
# When the axiom is constructed (with the __init__ function above), the "predicate" attribute is the lambda function itself,
# the "params" attribute is the list of parameters (i.e. ["x","y","z"]), which is obtained using "inspect.getfullargspec"
# (this is some more advanced programming), and "nparams" contains the number of parameters (which is 3 in this case).
# The expression "meet(x,meet(y,z)) == meet(meet(x,y),z))", which constitutes the body of the function, evaluates to "True" if both terms are equal
# and to "False" if they are not, and this is the value returned by the function (i.e. either "True" or "False")
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
# Here we loop over the axioms in the "axioms" list above
for axiom in axioms:
    naxiom += 1
    satisfied = True
    # for each of the axioms (numbered by "naxioms" above) we loop over all possible arguments (e.g. for the associative law,
    # over all possible values for "x","y" and "z"). Each of these variables takes values in the domain of the lattice
    # (e.g. in the case of "example1_6", we have domain=[0,a,b,c,1]). So there are 5^3=125 possible combinations of values for variables "x", "y" and "z".
    # The possible combinations are described by the Cartesion product domain X domain X domain.
    # The function call "itertools.product(domain,repeat=axiom.nparams)" below returns a kind of list, which contains
    # all elements of the n-fold Cartesion product of the domain
    # with itself (where n = axiom.nparams, e.g. n=3 for the associative law). Each of these elements is an n-tuple, stored in
    # the "args" variable.
    for args in itertools.product(domain,repeat=axiom.nparams):
        # Usually we would call axiom.predicate(args[0]) if the predicate takes one argument, and we would call axiom.predicate(args[0],args[1])
        # if it takes two arguments, and we would call axiom.predicate(args[0],args[1],args[2]) if it takes three arguments.
        # But this would be a different expression in each case. A Python feature called "argument unpacking" provides a convenient solution
        # to this problem: we may just pass the "args" tuple to the function, if we prefix it with a "*".
        res = axiom.predicate(*args)
        # at this point, we have res=True if the axiom holds for the specific values, and otherwise res=False
        if not res:
            # We print some information about the values for which the axiom fails.
            if satisfied:
                print(str(naxiom)+") Fail")
                print(axiom)
                satisfied = False
            print("    fails for "+str(tuple(axiom.params))+" = "+str(args))
    # If, after completing the inner loop, the "satisfied" variable still has the value "True",
    # the axiom holds for all possible values, and we output this accordingly:
    if satisfied:
        print(str(naxiom)+") Pass")

