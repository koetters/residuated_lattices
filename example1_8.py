from residuated_lattice import ResiduatedLattice

# The definitions below are given for convenience, so we can easily refer to elements of the algebra.
a="a"
b="b"
c="c"
d="d"

# The domain (or base set) of the algebra. The order in which the elements are stated is important:
# the list serves as a column header and row header for the operation tables below.
domain = [0,a,b,c,d,1]

# The "line diagram" of the lattice order: only the neighboring pairs in the order have to be given.
line_diag = [(0,b),(b,a),(a,1),(0,d),(d,c),(c,a)]

# The operation table for the arrow operation.
arrow_matrix = [
    [1,1,1,1,1,1],
    [0,1,b,c,c,1],
    [c,a,1,c,c,1],
    [b,a,b,1,a,1],
    [b,a,b,a,1,1],
    [0,a,b,c,d,1],
]

# The operation table for the multiplication.
prod_matrix = [
    [0,0,0,0,0,0],
    [0,a,b,d,d,a],
    [c,b,b,0,0,b],
    [b,d,0,d,d,c],
    [b,d,0,d,d,d],
    [0,a,b,c,d,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

