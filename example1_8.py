from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"

domain = [0,a,b,c,d,1]

line_diag = [(0,b),(b,a),(a,1),(0,d),(d,c),(c,a)]

arrow_matrix = [
    [1,1,1,1,1,1],
    [0,1,b,c,c,1],
    [c,a,1,c,c,1],
    [b,a,b,1,a,1],
    [b,a,b,a,1,1],
    [0,a,b,c,d,1],
]

prod_matrix = [
    [0,0,0,0,0,0],
    [0,a,b,d,d,a],
    [c,b,b,0,0,b],
    [b,d,0,d,d,c],
    [b,d,0,d,d,d],
    [0,a,b,c,d,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

