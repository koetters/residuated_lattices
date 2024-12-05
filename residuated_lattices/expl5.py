from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"

domain = [0,a,b,c,d,1]

line_diag = [(0,a),(a,b),(a,c),(b,d),(c,d),(d,1)]

arrow_matrix = [
    [1,1,1,1,1,1],
    [d,1,1,1,1,1],
    [d,d,1,d,1,1],
    [b,b,b,1,1,1],
    [b,b,b,d,1,1],
    [0,a,b,c,d,1],
]

prod_matrix = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,a],
    [0,0,0,0,0,b],
    [0,0,0,c,c,c],
    [0,0,0,c,c,d],
    [0,a,b,c,d,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

