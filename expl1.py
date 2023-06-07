from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"
e="e"

domain = [0,a,b,c,d,e,1]

line_diag = [(0,a),(0,c),(a,b),(c,d),(b,e),(d,e),(e,1)]

arrow_matrix = [
    [1,1,1,1,1,1,1],
    [d,1,1,d,d,1,1],
    [d,e,1,d,d,1,1],
    [b,b,b,1,1,1,1],
    [b,b,b,e,1,1,1],
    [0,b,b,d,d,1,1],
    [0,a,b,c,d,e,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0],
    [0,a,a,0,0,a,a],
    [0,a,a,0,0,a,b],
    [0,0,0,c,c,c,c],
    [0,0,0,c,c,c,d],
    [0,a,a,c,c,e,e],
    [0,a,b,c,d,e,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

