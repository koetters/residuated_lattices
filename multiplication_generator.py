class BinaryOperation:
  def __init__(self,n):
    self.n = n
    self.table = [n*[None] for _ in range(n)]

  def __str__(self):
    return str(self.table)

  def copy(self):
    n = self.n
    res = BinaryOperation(n)
    for i in range(n):
      for j in range(n):
        res.table[i][j] = self.table[i][j]
    return res

class MultiplicationGenerator:

  def __init__(self,lattice):
    self.lattice = lattice
    self.profile = lattice.profile()
    self.multiplications = dict()
    n = lattice.n
    subsemilattice = set([0,n-1])
    self.irreducibles = []
    self.subsemilattices = []
    self.delta = []
    self.delta_generators = []
    for i in range(n):
      if i in subsemilattice:
        continue
      new_elements = []
      new_generators = []
      s = subsemilattice.copy()
      for j in s:
        k = lattice.sup(i,j)
        if k not in subsemilattice:
          new_elements.append(k)
          new_generators.append((i,j))
          subsemilattice.add(k)
      self.irreducibles.append(i)
      s = subsemilattice.copy()
      self.subsemilattices.append(s)
      self.delta.append(new_elements)
      self.delta_generators.append(new_generators)
      # self.count = 0

  def is_automorphic_image(self,m1,m2):
    check = AutomorphismCheck(self.lattice,m1,m2)
    result = check.run([])
    return result

  def run(self):
    n = self.lattice.n
    mult = BinaryOperation(n)
    for i in range(n):
      mult.table[0][i] = 0
      mult.table[i][0] = 0
      mult.table[n-1][i] = i
      mult.table[i][n-1] = i
    # we deal with the trivial cases n=1 and n=2 separately
    if n <= 2:
      extmult = mult.copy()
      extprofile = self.get_extended_profile(extmult)
      key = self.get_hash(extprofile)
      self.multiplications[key] = [extmult]
      return
    self.fill_table(mult,0,0)

  def fill_table(self,mult,i0,j0):

    # self.count += 1
    # weight = tuple([mult.table[x][y] for x in range(1,self.lattice.n-1) for y in range(1,x+1) if mult.table[x][y] is not None])
    # print(f"{self.count}) {weight}")

    a0 = self.irreducibles[i0]
    b0 = self.irreducibles[j0]

    nextpos = None
    if j0 < i0:
      nextpos = (i0,j0+1)
    if j0 == i0 and i0+1 < len(self.irreducibles):
      nextpos = (i0+1,0)

    lna0 = self.lattice.lower_neighbor(a0)
    lnb0 = self.lattice.lower_neighbor(b0)
    lower_bound = self.lattice.sup(mult.table[lna0][b0],mult.table[a0][lnb0])
    upper_bound = self.lattice.inf(a0,b0)
    for new_value in range(lower_bound,upper_bound+1):
      if self.lattice.leq(lower_bound,new_value) and self.lattice.leq(new_value,upper_bound):
        extmult = mult.copy()
        extmult.table[a0][b0] = new_value
        for a1,a2 in self.delta_generators[i0]:
          for b1,b2 in self.delta_generators[j0]:
            # we extend the partial multiplication, defining k1 * k2 for all k1 in self.delta[i0] and k2 in self.delta[j0].
            # such k1 is represented by k1 = a1 v a2 for some (a1,a2) in self.delta_generators[i0], and likewise for k2.
            # Multiplication distributes over supremum, so necessarily k1 * k2 = (a1 v a2) * (b1 v b2) = (a1 * b1) v (a1 * b2) v (a2 * b1) v (a2 * b2).
            # We still have to check afterwards, whether the algebraic laws are satisfied.
            k1 = self.lattice.sup(a1,a2)
            k2 = self.lattice.sup(b1,b2)
            l1 = extmult.table[a1][b1]
            l2 = extmult.table[a1][b2]
            l3 = extmult.table[a2][b1]
            l4 = extmult.table[a2][b2]
            extmult.table[k1][k2] = self.lattice.sup(self.lattice.sup(l1,l2),self.lattice.sup(l3,l4))
            extmult.table[k2][k1] = extmult.table[k1][k2] # required by commutative law

        # now check whether extmult is a valid extension of mult

        # this should not be possible, but we check to make sure
        if extmult.table[a0][b0] != new_value:
          raise ValueError

        valid = True

        # distributive law (part 1)
        for a in self.delta[i0]:
          for b in self.subsemilattices[i0]:
            for c in self.delta[j0]:
              if extmult.table[self.lattice.sup(a,b)][c] != self.lattice.sup(extmult.table[a][c],extmult.table[b][c]):
                valid = False

        if valid == False:
          continue

        # distributive law (part 2)
        for a in self.delta[j0]:
          for b in self.subsemilattices[j0]:
            for c in self.delta[i0]:
              if extmult.table[self.lattice.sup(a,b)][c] != self.lattice.sup(extmult.table[a][c],extmult.table[b][c]):
                valid = False

        if valid == False:
          continue

        # associative law (part 1)
        for i in range(i0+1):
          c = self.irreducibles[i]
          if extmult.table[extmult.table[a0][b0]][c] != extmult.table[a0][extmult.table[b0][c]]:
            valid = False

        if valid == False:
          continue

        # associative law (part 2)
        for j in range(j0+1):
          c = self.irreducibles[j]
          if extmult.table[extmult.table[c][a0]][b0] != extmult.table[c][extmult.table[a0][b0]]:
            valid = False

        if valid == False:
          continue

        if nextpos == None: # this means that multiplication is totally defined
#          return True
          extprofile = self.get_extended_profile(extmult)
          key = self.get_hash(extprofile)
          if key not in self.multiplications:
            self.multiplications[key] = [extmult]
          else:
            lst = self.multiplications[key]
            unknown = True
            for m in lst:
              if self.is_automorphic_image(extmult,m):
                unknown = False
                break
            if unknown:
              lst.append(extmult)

        else:
          self.fill_table(extmult,nextpos[0],nextpos[1])
#          success = self.fill_table(extmult,nextpos[0],nextpos[1])
#          if success:
#            return True

#    return False

  def get_extended_profile(self,mult):
    n = self.lattice.n
    profile = self.profile
    count = [0] * n
    for i in range(0,n):
      for j in range(i,n):
        k = mult.table[i][j]
        count[k] += 1
    extended_profile = [profile[i]+(count[i],) for i in range(n)]
    return extended_profile

  # this is copied from LatticeGenerator; maybe put it somewhere else
  def get_hash(self,profile):
    slst = sorted(profile) # sorts profile in lexicographic order
    flatlist = sum(slst,()) # concatenation
    key = "-".join(str(i) for i in flatlist)
    return key

class AutomorphismCheck:

  def __init__(self,L,m1,m2):
    if len(m1.table) != L.n or len(m2.table) != L.n:
      raise ValueError
    self.domain = L
    self.mult1 = m1
    self.mult2 = m2
    self.targets = [[] for _ in range(L.n)]
    profile = L.profile()
    for i in range(L.n):
      for j in range(L.n):
        if profile[i] == profile[j]:
          self.targets[i].append(j)

  def run(self,f):
    if len(self.targets) <= len(f):
      raise ValueError
    i = len(f) # we want to find suitable values for f[i]
    for j in self.targets[i]: # so we look in the target list ...
      if j in f: # ... and check that setting f[i]:=j results in an injective function
        continue
      g = f+[j] # g is a possible extension of f
      k = len(g)
      valid = True
      for i in range(k):
        if self.domain.leq(i,k-1) != self.domain.leq(g[i],g[k-1]):
          valid = False
        if g[self.mult1.table[i][k-1]] != self.mult2.table[g[i]][g[k-1]]: # note that g[i*(k-1)] is defined, since i*(k-1) leq i,k-1
          valid = False
      if valid:
        if len(g) == len(self.targets): # g is a residual lattice isomorphism
          return True
        if self.run(g): # g can be extended to a residual lattice isomorphism
          return True
    return False # g can not be extended to a residual lattice isomorphism


