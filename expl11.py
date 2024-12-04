# residuated multilattice with 10 elements
from residuated_multilattice import ResiduatedMultilattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"
g="g"
h="h"

domain = [0,a,b,c,d,e,f,g,h,1]

line_diag = [(0,a),(0,b),(a,c),(a,d),(b,c),(b,d),(c,e),(d,e),(e,f),(e,g),(f,h),(g,h),(h,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1,1,1,1],
    [h,1,h,1,1,1,1,1,1,1],
    [h,h,1,1,1,1,1,1,1,1],
    [h,h,h,1,h,1,1,1,1,1],
    [h,h,h,h,1,1,1,1,1,1],
    [h,h,h,h,h,1,1,1,1,1],
    [g,g,g,g,g,g,1,g,1,1],
    [f,f,f,f,f,f,f,1,1,1],
    [e,e,e,e,e,e,f,g,1,1],
    [0,a,b,c,d,e,f,g,h,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,a],
    [0,0,0,0,0,0,0,0,0,b],
    [0,0,0,0,0,0,0,0,0,c],
    [0,0,0,0,0,0,0,0,0,d],
    [0,0,0,0,0,0,0,0,0,e],
    [0,0,0,0,0,0,f,0,f,f],
    [0,0,0,0,0,0,0,g,g,g],
    [0,0,0,0,0,0,f,g,h,h],
    [0,a,b,c,d,e,f,g,h,1],
]

lattice = ResiduatedMultilattice(domain,line_diag,prod_matrix,arrow_matrix)
