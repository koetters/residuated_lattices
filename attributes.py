# lattice property
def distributive(lattice):
  n = lattice.n
  for a in range(n):
    for b in range(n):
      for c in range(n):
        if lattice.sup(a,lattice.inf(b,c)) != lattice.inf(lattice.sup(a,b),lattice.sup(a,c)):
          return False
  return True

# lattice property
def modular(lattice):
  n = lattice.n
  for a in range(n):
    for b in range(n):
      if not lattice.leq(a,b):
        continue
      for c in range(n):
        if lattice.inf(lattice.sup(a,c),b) != lattice.sup(a,lattice.inf(c,b)):
          return False
  return True

# lattice property
def complemented(lattice):
  n = lattice.n
  complements = [set() for _ in range(n)]
  for a in range(n):
    for b in range(n):
      if lattice.inf(a,b) == 0 and lattice.sup(a,b) == n-1:
        complements[a].add(b)
    if len(complements[a]) == 0:
      return False
  return True

# lattice property
def relatively_complemented(lattice):
  n = lattice.n
  for a in range(n):
    intervals = set()
    upper_cone = [i for i in range(n) if lattice.leq(a,i)]
    lower_cone = [i for i in range(n) if lattice.leq(i,a)]
    for b in range(n):
      intervals.add((lattice.inf(a,b),lattice.sup(a,b)))
    if len(intervals) < len(upper_cone) * len(lower_cone):
      return False
  return True

# lattice property
def pseudocomplemented(lattice):
  n = lattice.n
  for a in range(n):
    p = 0
    for c in range(n):
      if lattice.inf(a,c) == 0:
        p = lattice.sup(p,c)
    if lattice.inf(a,p) != 0:
      return False
  return True

# lattice property
def relatively_pseudocomplemented(lattice):
  n = lattice.n
  for a in range(n):
    for b in range(n):
      rp = 0
      for c in range(n):
        if lattice.leq(lattice.inf(a,c),b):
          rp = lattice.sup(rp,c)
      if not lattice.leq(lattice.inf(a,rp),b):
        return False
  return True

# lattice property
def boolean(lattice):
  return distributive(lattice) and complemented(lattice)

# lattice property
def height(lattice):
  return lattice.height()

# lattice property
def width(lattice):
  return lattice.width()

# residuated property
def prelinear(rlat):
  n = rlat.n
  for a in range(n):
    for b in range(n):
      if rlat.sup(rlat.arrow(a,b),rlat.arrow(b,a)) != n-1:
        return False
  return True

# residuated property
def pi1(rlat):
  n = rlat.n
  for a in range(n):
    for b in range(n):
      for c in range(n):
        lhs = rlat.arrow(rlat.arrow(c,0),0)
        rhs = rlat.arrow(rlat.arrow(rlat.mult(a,c),rlat.mult(b,c)),rlat.arrow(a,b))
        if not rlat.leq(lhs,rhs):
          return False
  return True

# residuated property
def pi2(rlat):
  n = rlat.n
  for a in range(n):
    if rlat.inf(a,rlat.arrow(a,0)) != 0:
      return False
  return True

# residuated property
def strict(rlat):
  n = rlat.n
  for a in range(n):
    for b in range(n):
      if rlat.arrow(rlat.mult(a,b),0) != rlat.sup(rlat.arrow(a,0),rlat.arrow(b,0)):
        return False
  return True

# residuated property
def wnm(rlat):
  n = rlat.n
  for a in range(n):
    for b in range(n):
      if rlat.sup(rlat.arrow(rlat.mult(a,b),0),rlat.arrow(rlat.inf(a,b),rlat.mult(a,b))) != n-1:
        return False
  return True

# residuated property
def divisible(rlat):
  n = rlat.n
  for a in range(n):
    for b in range(n):
      if rlat.inf(a,b) != rlat.mult(a,rlat.arrow(a,b)):
        return False
  return True

# residuated property
def involutive(rlat):
  n = rlat.n
  for a in range(n):
    if a != rlat.arrow(rlat.arrow(a,0),0):
      return False
  return True

# residuated property
def idempotent(rlat):
  n = rlat.n
  for a in range(n):
    if a != rlat.mult(a,a):
      return False
  return True

# residuated property
def semi_prelinear(rlat):
  n = rlat.n
  for x in range(n):
    for y in range(n):
      if rlat.sup(rlat.arrow(rlat.neg(x),rlat.neg(y)),rlat.arrow(rlat.neg(y),rlat.neg(x))) != n-1:
        return False
  return True

# residuated property
def semi_idempotent(rlat):
  n = rlat.n
  for x in range(n):
    if rlat.neg(rlat.mult(rlat.neg(x),rlat.neg(x))) != rlat.neg(rlat.neg(x)):
      return False
  return True

# residuated property
def semi_divisible(rlat):
  n = rlat.n
  for x in range(n):
    for y in range(n):
      if rlat.neg(rlat.mult(rlat.neg(x),rlat.arrow(rlat.neg(x),rlat.neg(y)))) != rlat.neg(rlat.inf(rlat.neg(x),rlat.neg(y))):
        return False
  return True

# residuated property
def demorgan(rlat):
  n = rlat.n
  for x in range(n):
    for y in range(n):
      if rlat.neg(rlat.inf(x,y)) != rlat.sup(rlat.neg(x),rlat.neg(y)):
        return False
  return True

# residuated property
def stonean(rlat):
  n = rlat.n
  for x in range(n):
    if rlat.sup(rlat.neg(x),rlat.neg(rlat.neg(x))) != n-1:
      return False
  return True

# residuated property
def semig(rlat):
  n = rlat.n
  for x in range(n):
    if rlat.neg(rlat.mult(x,x)) != rlat.neg(x):
      return False
  return True

