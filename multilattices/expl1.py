# The multilattice ML7
from multilattice import Multilattice

a="a"
b="b"
c="c"
d="d"
e="e"

domain = [0,a,b,c,d,e,1]

line_diag = [(0,a),(0,b),(a,c),(a,d),(b,c),(b,d),(c,e),(d,e),(e,1)]

lattice = Multilattice(domain,line_diag)
