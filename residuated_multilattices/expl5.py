# The smallest pure prelinear residuated multilattice (having 12 elements)
from residuated_multilattice import ResiduatedMultilattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"
g="g"
h="h"
i="i"
j="j"

domain = [0,a,b,c,d,e,f,g,h,i,j,1]

line_diag = [(0,a),(0,b),(a,c),(a,f),(b,e),(b,d),(c,e),(d,f),(e,g),(f,g),(g,h),(h,i),(h,j),(i,1),(j,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [i,1,i,1,i,1,1,1,1,1,1,1],
    [j,j,1,j,1,1,1,1,1,1,1,1],
    [i,i,i,1,i,1,i,1,1,1,1,1],
    [j,j,j,j,1,j,1,1,1,1,1,1],
    [h,h,i,j,i,1,i,1,1,1,1,1],
    [h,j,h,j,i,j,1,1,1,1,1,1],
    [h,h,h,j,i,j,i,1,1,1,1,1],
    [g,g,g,g,g,g,g,g,1,1,1,1],
    [c,c,e,c,g,e,g,g,j,1,j,1],
    [d,f,d,g,d,g,f,g,i,i,1,1],
    [0,a,b,c,d,e,f,g,h,i,j,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,a,a],
    [0,0,0,0,0,0,0,0,0,b,0,b],
    [0,0,0,0,0,0,0,0,0,0,c,c],
    [0,0,0,0,0,0,0,0,0,d,0,d],
    [0,0,0,0,0,0,0,0,0,b,c,e],
    [0,0,0,0,0,0,0,0,0,d,a,f],
    [0,0,0,0,0,0,0,0,0,d,c,g],
    [0,0,0,0,0,0,0,0,h,h,h,h],
    [0,0,b,0,d,b,d,d,h,i,h,i],
    [0,a,0,c,0,c,a,c,h,h,j,j],
    [0,a,b,c,d,e,f,g,h,i,j,1],
]

lattice = ResiduatedMultilattice(domain,line_diag,prod_matrix,arrow_matrix)
