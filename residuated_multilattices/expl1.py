# The residuated multilattice ML7
from residuated_multilattice import ResiduatedMultilattice

a="a"
b="b"
c="c"
d="d"
e="e"

domain = [0,a,b,c,d,e,1]

line_diag = [(0,a),(0,b),(a,c),(a,d),(b,c),(b,d),(c,e),(d,e),(e,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1],
    [e,1,e,1,1,1,1],
    [a,a,1,1,1,1,1],
    [a,a,e,1,e,1,1],
    [a,a,e,e,1,1,1],
    [a,a,e,e,e,1,1],
    [0,a,b,c,d,e,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,a],
    [0,0,b,b,b,b,b],
    [0,0,b,b,b,b,c],
    [0,0,b,b,b,b,d],
    [0,0,b,b,b,b,e],
    [0,a,b,c,d,e,1],
]

lattice = ResiduatedMultilattice(domain,line_diag,prod_matrix,arrow_matrix)
