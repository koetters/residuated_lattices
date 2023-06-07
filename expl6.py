from residuated_lattice import ResiduatedLattice

a="a"
b="b"

domain = [0,a,b,1]

line_diag = [(0,a),(0,b),(a,1),(b,1)]

arrow_matrix = [
    [1,1,1,1],
    [b,1,b,1],
    [a,a,1,1],
    [0,a,b,1],
]

prod_matrix = [
    [0,0,0,0],
    [0,a,0,a],
    [0,0,b,b],
    [0,a,b,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

