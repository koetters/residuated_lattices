# Another residuated "spindle" multilattice
from residuated_multilattice import ResiduatedMultilattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"

domain = [0,a,b,c,d,e,f,1]

line_diag = [(0,a),(a,b),(a,c),(b,d),(b,e),(c,d),(c,e),(d,f),(e,f),(f,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1],
    [0,f,1,f,1,1,1,1],
    [0,d,d,1,1,1,1,1],
    [0,d,d,f,1,f,1,1],
    [0,b,b,d,d,1,1,1],
    [0,b,b,d,d,f,1,1],
    [0,a,b,c,d,e,f,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0,0],
    [0,a,a,a,a,a,a,a],
    [0,a,a,a,a,a,a,b],
    [0,a,a,a,a,c,c,c],
    [0,a,a,a,a,c,c,d],
    [0,a,a,c,c,e,e,e],
    [0,a,a,c,c,e,e,f],
    [0,a,b,c,d,e,f,1],
]

lattice = ResiduatedMultilattice(domain,line_diag,prod_matrix,arrow_matrix)
