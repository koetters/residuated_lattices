from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"
g="g"

domain = [0,a,b,c,d,e,f,g,1]

line_diag = [(0,a),(a,b),(b,e),(e,1),(0,c),(c,f),(f,g),(g,1),(a,d),(d,g),(c,d),(d,e)]

#arrow_matrix = [
#    [1,1,1,1,1,1,1,1,1],
#    [g,1,1,g,1,1,g,1,1],
#    [f,g,1,f,g,1,f,g,1],
#    [e,e,e,1,1,1,1,1,1],
#    [d,e,e,g,1,1,g,1,1],
#    [c,d,e,f,g,1,f,g,1],
#    [b,b,b,e,e,e,1,1,1],
#    [a,b,b,d,e,e,g,1,1],
#    [0,a,b,c,d,e,f,g,1],
#]

prod_matrix = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,a,0,0,a,0,0,a],
    [0,a,b,0,a,b,0,a,b],
    [0,0,0,0,0,0,c,c,c],
    [0,0,a,0,0,a,c,c,d],
    [0,a,b,0,a,b,c,d,e],
    [0,0,0,c,c,c,f,f,f],
    [0,0,a,c,c,d,f,f,g],
    [0,a,b,c,d,e,f,g,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix)

