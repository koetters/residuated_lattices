# The "spindle" multilattice (same as expl2)
from multilattice import Multilattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"

domain = [0,a,b,c,d,e,f,1]

line_diag = [(0,a),(a,b),(a,c),(b,d),(b,e),(c,d),(c,e),(d,f),(e,f),(f,1)]

lattice = Multilattice(domain,line_diag)
