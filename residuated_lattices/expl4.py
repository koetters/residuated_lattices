from residuated_lattice import ResiduatedLattice

a="a"
b="b"
c="c"
d="d"
e="e"
f="f"
m="m"
n="n"


domain = [0,n,a,b,c,d,e,f,m,1]

line_diag = [(0,n),(n,a),(n,b),(a,c),(b,c),(b,d),(c,e),(d,e),(e,m),(d,f),(f,m),(m,1)]
# line_diag = [(0,n),(n,a),(n,b),(a,c),(b,d),(c,e),(d,f),(e,m),(f,m),(m,1)]


arrow_matrix = [
    [1,1,1,1,1,1,1,1,1,1],
    [m,1,1,1,1,1,1,1,1,1],
    [f,f,1,f,1,f,1,f,1,1],
    [e,e,e,1,1,1,1,1,1,1],
    [d,d,e,f,1,f,1,f,1,1],
    [c,c,c,e,e,1,1,1,1,1],
    [b,b,c,d,e,f,1,f,1,1],
    [a,a,a,c,c,e,e,1,1,1],
    [n,n,a,b,c,d,e,f,1,1],
    [0,n,a,b,c,d,e,f,m,1],
]

prod_matrix = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,n],
    [0,0,a,0,a,0,a,0,a,a],
    [0,0,0,0,0,0,0,b,b,b],
    [0,0,a,0,a,0,a,b,c,c],
    [0,0,0,0,0,b,b,d,d,d],
    [0,0,a,0,a,b,c,d,e,e],
    [0,0,0,b,b,d,d,f,f,f],
    [0,0,a,b,c,d,e,f,m,m],
    [0,n,a,b,c,d,e,f,m,1],
]

lattice = ResiduatedLattice(domain,line_diag,prod_matrix,arrow_matrix)

