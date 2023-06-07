from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"

domain = [0,a,b,c,d,1]

line_diag = [(0,a),(0,b),(a,c),(b,c),(c,d),(d,1)]

arrow_matrix = [
    [1,1,1,1,1,1],
    [b,1,b,1,1,1],
    [c,c,1,1,1,1],
    [b,c,b,1,1,1],
    [0,a,b,c,1,1],
    [0,a,b,c,d,1],
]

prod_matrix = [
    [0,0,0,0,0,0],
    [0,a,0,a,a,a],
    [0,0,0,0,b,b],
    [0,a,0,a,c,c],
    [0,a,b,c,d,d],
    [0,a,b,c,d,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

