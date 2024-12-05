# multilattice with 10 elements
from multilattice import Multilattice

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

lattice = Multilattice(domain,line_diag)
