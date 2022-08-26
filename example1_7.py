from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"

domain = [0,a,b,c,d,e,f,1]

line_diag = [(0,d),(d,c),(c,b),(b,a),(d,e),(e,f),(f,a),(a,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1,1],
    [d,1,a,a,f,f,f,1],
    [e,1,1,a,f,f,f,1],
    [f,1,1,1,f,f,f,1],
    [a,1,1,1,1,1,1,1],
    [b,1,a,a,a,1,1,1],
    [c,1,a,a,a,a,1,1],
    [1,a,b,c,d,e,f,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0,0],
    [0,c,c,c,0,d,d,a],
    [0,c,c,c,0,0,d,b],
    [0,c,c,c,0,0,0,c],
    [0,0,0,0,0,0,0,d],
    [0,d,0,0,0,d,d,e],
    [0,d,d,0,0,d,d,f],
    [0,a,b,c,d,e,f,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

