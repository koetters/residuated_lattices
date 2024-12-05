# multilattice with 12 elements (the one which can be extended to a pure prelinear residuated multilattice)
from multilattice import Multilattice

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

lattice = Multilattice(domain,line_diag)
