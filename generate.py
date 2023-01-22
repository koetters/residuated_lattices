import sys
import time
import pickle
import shelve
from pathlib import Path

class ResiduatedLattice:

  def __init__(self,lattice,mult):
    n = len(lattice._relation)
    self.n = n
    self._leq = [[None] * n for _ in range(n)]
    for i in range(n):
      for j in range(n):
        self._leq[i][j] = lattice._relation[i][j]
    self._inf = lattice.infimum_operation().table
    self._sup = lattice.supremum_operation().table
    self._mult = [[None] * n for _ in range(n)]
    for i in range(n):
      for j in range(n):
        self._mult[i][j] = mult[i][j]
    self._arrow = [[None] * n for _ in range(n)]
    for i in range(n):
      for j in range(n):
        value = 0
        for k in range(n):
          if self._leq[self._mult[i][k]][j]:
            value = self._sup[value][k]
        if not self._leq[self._mult[i][value]][j]:
          raise ValueError("not a residuated lattice. arrow operation can not be defined.")
        self._arrow[i][j] = value

  @classmethod
  def decode(cls,encoding,n):
    upper_triangle_size = n * (n+1) // 2
    part1_length = upper_triangle_size // 8
    if upper_triangle_size % 8 != 0:
      part1_length += 1
    part1 = encoding[:part1_length]
    part2 = encoding[part1_length:]

    # decoding the underlying lattice
    lattice = UpperTriangularMatrix.decode(part1,n)

    # decoding the multiplication operation
    seq = list(part2)
    mult_op = BinaryOperation(n)
    mult = mult_op.table
    upperbyte = 1
    byte = 0
    for i in range(n):
      for j in range(i,n):
        mult[i][j] = (seq[byte] >> (4 * upperbyte)) & 15
        mult[j][i] = mult[i][j]
        upperbyte -= 1
        if upperbyte < 0:
          upperbyte = 1
          byte += 1

    return ResiduatedLattice(lattice,mult_op.table)

  def __eq__(self,other):
    n = self.n
    if n != other.n:
      return False
    for i in range(n):
      for j in range(n):
        if self._leq[i][j] != other._leq[i][j]:
          return False
        if self._mult[i][j] != other._mult[i][j]:
          return False
    return True

  def leq(self,i,j):
    return self._leq[i][j]

  def inf(self,i,j):
    return self._inf[i][j]

  def sup(self,i,j):
    return self._sup[i][j]

  def mult(self,i,j):
    return self._mult[i][j]

  def arrow(self,i,j):
    return self._arrow[i][j]

  def encode(self):
    part1 = self.encode_order()
    part2 = self.encode_mult()
    encoding = part1 + part2
    return encoding

  def encode_mult(self):
    n = self.n
    upperbyte = 1
    byte = 0
    upper_triangle_size = n * (n+1) // 2
    nbytes = upper_triangle_size // 2
    if upper_triangle_size % 2 != 0:
      nbytes += 1
    seq = [0] * nbytes
    for i in range(n):
      for j in range(i,n):
        seq[byte] += (self.mult(i,j) << (4 * upperbyte))
        upperbyte -= 1
        if upperbyte < 0:
          upperbyte = 1
          byte += 1
    return bytes(seq)

  def encode_order(self):
    n = self.n
    bit = 7
    byte = 0
    upper_triangle_size = n * (n+1) // 2
    nbytes = upper_triangle_size // 8
    if upper_triangle_size % 8 != 0:
      nbytes += 1
    seq = [0] * nbytes
    for i in range(n):
      for j in range(i,n):
        if self.leq(i,j):
          seq[byte] += (1 << bit)
        bit -= 1
        if bit < 0:
          bit = 7
          byte += 1
    return bytes(seq)

  def is_distributive(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        for c in range(n):
          if self.sup(a,self.inf(b,c)) != self.inf(self.sup(a,b),self.sup(a,c)):
            return False
    return True

  def is_modular(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        if not self.leq(a,b):
          continue
        for c in range(n):
          if self.inf(self.sup(a,c),b) != self.sup(a,self.inf(c,b)):
            return False
    return True

  def is_prelinear(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        if self.sup(self.arrow(a,b),self.arrow(b,a)) != n-1:
          return False
    return True

  def satisfies_pi1(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        for c in range(n):
          lhs = self.arrow(self.arrow(c,0),0)
          rhs = self.arrow(self.arrow(self.mult(a,c),self.mult(b,c)),self.arrow(a,b))
          if not self.leq(lhs,rhs):
            return False
    return True

  def satisfies_pi2(self):
    n = self.n
    for a in range(n):
      if self.inf(a,self.arrow(a,0)) != 0:
        return False
    return True

  def is_strict(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        if self.arrow(self.mult(a,b),0) != self.sup(self.arrow(a,0),self.arrow(b,0)):
          return False
    return True

  def satisfies_wnm(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        if self.sup(self.arrow(self.mult(a,b),0),self.arrow(self.inf(a,b),self.mult(a,b))) != n-1:
          return False
    return True

  def is_divisible(self):
    n = self.n
    for a in range(n):
      for b in range(n):
        if self.inf(a,b) != self.mult(a,self.arrow(a,b)):
          return False
    return True

  def is_involutive(self):
    n = self.n
    for a in range(n):
      if a != self.arrow(self.arrow(a,0),0):
        return False
    return True

  def is_idempotent(self):
    n = self.n
    for a in range(n):
      if a != self.mult(a,a):
        return False
    return True

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

class UpperTriangularMatrix:

  def __init__(self,n):
    self.n = n
    self._relation = [n*[0] for _ in range(n)]
    for i in range(n):
      self._relation[i][i] = 1
      self._relation[0][i] = 1
      self._relation[i][n-1] = 1
    self._profile = None
    self._multiplications = None

  @classmethod
  def decode(self,encoding,n):
    seq = list(encoding)
    lattice = UpperTriangularMatrix(n)
    order = lattice._relation
    bit = 7
    byte = 0
    for i in range(n):
      for j in range(i,n):
        order[i][j] = (seq[byte] >> bit) & 1
        bit -= 1
        if bit < 0:
          bit = 7
          byte += 1
    return lattice

  def __str__(self):
    return str(self._relation)

  def __eq__(self,other):
    n = self.n
    if n != other.n:
      return False
    for i in range(n):
      for j in range(n):
        if self._relation[i][j] != other._relation[i][j]:
          return False
    return True

  def height(self):
    n = self.n
    strict_order = []
    for i in range(n):
      for j in range(i+1,n):
        if self.leq(i,j):
          strict_order.append((i,j))
    maxlength = 1
    power = strict_order
    while power:
      maxlength += 1
      power = self._product(power,strict_order)
    return maxlength

  def _product(self,A,B):
    C = []
    for a,b1 in A:
      for b2,c in B:
        if b1==b2:
          C.append((a,c))
    return C

  def width(self):
    n = self.n
    self.incomparables = [set() for _ in range(n)]
    for i in range(n):
      for j in range(i+1,n):
        if self.leq(i,j) or self.leq(j,i):
          continue
        self.incomparables[i].add(j)
    result = self._find_width((),set(range(n)),0)
    del(self.incomparables)
    return result

  def _find_width(self,antichain,choices,maxlength):
    for i in choices:
      antichain2 = antichain + (i,)
      maxlength = max(maxlength,len(antichain2))
      choices2 = choices & self.incomparables[i]
      if maxlength < len(antichain2) + len(choices2):
        result = self._find_width(antichain2,choices2,maxlength)
        maxlength = max(maxlength,result)
    return maxlength

  def encode_order(self):
    n = self.n
    bit = 7
    byte = 0
    upper_triangle_size = n * (n+1) // 2
    nbytes = upper_triangle_size // 8
    if upper_triangle_size % 8 != 0:
      nbytes += 1
    seq = [0] * nbytes
    for i in range(n):
      for j in range(i,n):
        if self.leq(i,j):
          seq[byte] += (1 << bit)
        bit -= 1
        if bit < 0:
          bit = 7
          byte += 1
    return bytes(seq)

  def is_distributive(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    for a in range(n):
      for b in range(n):
        for c in range(n):
          if sup[a][inf[b][c]] != inf[sup[a][b]][sup[a][c]]:
            return False
    return True

  def is_modular(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    for a in range(n):
      for b in range(n):
        if not self.leq(a,b):
          continue
        for c in range(n):
          if inf[sup[a][c]][b] != sup[a][inf[c][b]]:
            return False
    return True

  def is_complemented(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    complements = [set() for _ in range(n)]
    for a in range(n):
      for b in range(n):
        if inf[a][b] == 0 and sup[a][b] == n-1:
          complements[a].add(b)
      if len(complements[a]) == 0:
        return False
    return True

  def is_boolean(self):
    return self.is_distributive() and self.is_complemented()

  def is_relatively_complemented(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    for a in range(n):
      intervals = set()
      upper_cone = [i for i in range(n) if self.leq(a,i)]
      lower_cone = [i for i in range(n) if self.leq(i,a)]
      for b in range(n):
        intervals.add((inf[a][b],sup[a][b]))
      if len(intervals) < len(upper_cone) * len(lower_cone):
        return False
    return True

  def is_pseudocomplemented(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    for a in range(n):
      p = 0
      for c in range(n):
        if inf[a][c] == 0:
          p = sup[p][c]
      if inf[a][p] != 0:
        return False
    return True

  def is_relatively_pseudocomplemented(self):
    n = self.n
    sup = self.supremum_operation().table
    inf = self.infimum_operation().table
    for a in range(n):
      for b in range(n):
        rp = 0
        for c in range(n):
          if self.leq(inf[a][c],b):
            rp = sup[rp][c]
        if not self.leq(inf[a][rp],b):
          return False
    return True

  def leq(self,i,j):
    if self._relation[i][j] == 1:
      return True
    return False

  def infimum(self,i,j):
    if self.leq(i,j):
      return i
    if self.leq(j,i):
      return j
    for k in range(min(i,j)-1,-1,-1):
      if self.leq(k,i) and self.leq(k,j):
        return k

  def supremum(self,i,j):
    if self.leq(i,j):
      return j
    if self.leq(j,i):
      return i
    for k in range(max(i,j)+1,self.n):
      if self.leq(i,k) and self.leq(j,k):
        return k

  def get_profile(self):
    if self._profile is None:
      self._create_profile()
    return self._profile

  # Returns a binary operation op, such that op[i][j] is a maximal lower bound of i and j. In a lattice, this is the infimum operation.
  def infimum_operation(self):
    n = self.n
    op = BinaryOperation(n)
    for i in range(n):
      for j in range(i,n):
        lb = self.infimum(i,j)
        op.table[i][j] = lb
        op.table[j][i] = lb
    return op

  def supremum_operation(self):
    n = self.n
    op = BinaryOperation(n)
    for i in range(n):
      for j in range(i,n):
        ub = self.supremum(i,j)
        op.table[i][j] = ub
        op.table[j][i] = ub
    return op

  def _create_profile(self):
    n = self.n
    inf_op = self.infimum_operation()
    sup_op = self.supremum_operation()
    profile = [[0,0,0,0] for _ in range(n)]

    for i in range(n):
      for j in range(i,n):
        if self.leq(i,j):
          profile[j][0] += 1 # count i in the lower cone of j
          profile[i][1] += 1 # count j in the upper cone of i
        else: # i and j are incomparable
          a = inf_op.table[i][j]
          b = sup_op.table[i][j]
          profile[a][2] += 1 # count (i,j) as a generating pair (infimum-wise) for a
          profile[b][3] += 1 # count (i,j) as a generating pair (supremum-wise) for b

    self._profile = [tuple(profile[i]) for i in range(n)]

  def copy(self):
    n = self.n
    res = UpperTriangularMatrix(n)
    for i in range(n):
      for j in range(n):
        res._relation[i][j] = self._relation[i][j]
    return res

  # Returns a lower neighbor of i. If i is supremum-irreducible, this is the unique lower neighbor.
  # If i=0 (no lower neighbor exists), None is returned.
  def lower_neighbor(self,i):
    for l in range(i-1,-1,-1):
      if self.leq(l,i):
        return l
    return None

  def get_children(self):
    n = self.n
    lower = {0}
    upper = set()
    rest = set(range(n-1))
    children = self._find_children(lower,upper,rest)
    return children

  def _find_children(self,lower,upper,rest):
    n = self.n
    if rest:
      k = min(rest)
      children = []
      delta = set(self.supremum(i,k) for i in lower) - {n-1}
      if delta.isdisjoint(upper):
        lower1 = lower | delta
        upper1 = upper.copy()
        rest1 = rest - delta
        children += self._find_children(lower1,upper1,rest1)
      cone = set(j for j in range(k,n-1) if self.leq(k,j))
      if cone.isdisjoint(lower):
        lower2 = lower.copy()
        upper2 = upper | cone
        rest2 = rest - cone
        children += self._find_children(lower2,upper2,rest2)
      return children
    else:
      if len(lower)+len(upper) != n-1:
        raise ValueError
      if not lower.isdisjoint(upper):
        raise ValueError
      child = UpperTriangularMatrix(n+1)
      for i in range(n-1):
        for j in range(n-1):
          child._relation[i][j] = self._relation[i][j]
      for i in lower:
        child._relation[i][n-1] = 1
      return [child]

  def get_multiplications(self):
    mg = MultiplicationGenerator(self)
    mg.run()
    self._multiplications = mg.multiplications
    return mg.multiplications

class MultiplicationGenerator:

  def __init__(self,lattice):
    self.lattice = lattice
    self.profile = lattice.get_profile()
    self.multiplications = dict()
    n = lattice.n
    subsemilattice = set([0,n-1])
    self.inf = lattice.infimum_operation()
    self.sup = lattice.supremum_operation()
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
        k = self.sup.table[i][j]
        if k not in subsemilattice:
          new_elements.append(k)
          new_generators.append((i,j))
          subsemilattice.add(k)
      self.irreducibles.append(i)
      s = subsemilattice.copy()
      self.subsemilattices.append(s)
      self.delta.append(new_elements)
      self.delta_generators.append(new_generators)

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

    a0 = self.irreducibles[i0]
    b0 = self.irreducibles[j0]

    nextpos = None
    if j0 < i0:
      nextpos = (i0,j0+1)
    if j0 == i0 and i0+1 < len(self.irreducibles):
      nextpos = (i0+1,0)

    lna0 = self.lattice.lower_neighbor(a0)
    lnb0 = self.lattice.lower_neighbor(b0)
    lower_bound = self.sup.table[mult.table[lna0][b0]][mult.table[a0][lnb0]]
    upper_bound = self.inf.table[a0][b0]
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
            k1 = self.sup.table[a1][a2]
            k2 = self.sup.table[b1][b2]
            l1 = extmult.table[a1][b1]
            l2 = extmult.table[a1][b2]
            l3 = extmult.table[a2][b1]
            l4 = extmult.table[a2][b2]
            extmult.table[k1][k2] = self.sup.table[self.sup.table[l1][l2]][self.sup.table[l3][l4]]
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
              if extmult.table[self.sup.table[a][b]][c] != self.sup.table[extmult.table[a][c]][extmult.table[b][c]]:
                valid = False

        if valid == False:
          continue

        # distributive law (part 2)
        for a in self.delta[j0]:
          for b in self.subsemilattices[j0]:
            for c in self.delta[i0]:
              if extmult.table[self.sup.table[a][b]][c] != self.sup.table[extmult.table[a][c]][extmult.table[b][c]]:
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
    profile = L.get_profile()
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

class IsomorphismCheck:

  def __init__(self,L1,L2):
    if L1.n != L2.n:
      raise ValueError
    self.domain = L1
    self.codomain = L2
    self.targets = [[] for _ in range(L1.n)]
    pro1 = L1.get_profile()
    pro2 = L2.get_profile()
    for i in range(L1.n):
      for j in range(L2.n):
        if pro1[i] == pro2[j]:
          self.targets[i].append(j)

  def run(self,f):
    i = len(f)
    for j in self.targets[i]:
      if j in f:
        continue
      valid = True
      for l in range(i):
        if self.domain.leq(l,i) != self.codomain.leq(f[l],j):
          valid = False
      if valid == True:
        if i+1 == len(self.targets):
          return True
        if self.run(f+[j]):
          return True
    return False

class LatticeGenerator:

  def __init__(self):
    self.levels = {}

  def store_level(self,n):
    prefix = Path("database") / str(n)
    prefix.mkdir(parents=True)
    hashtable = self.levels[n]
    for key,lst in hashtable.items():
      dirpath = prefix / key
      dirpath.mkdir()
      for i,lattice in enumerate(lst):
        p = dirpath / str(i)
        with p.open(mode='wb') as f:
          pickle.dump(lattice,f)

#  def load_level(self,n):
#    hashtable = dict()
#    lvldir = Path("database") / str(n)
#    for keydir in lvldir.iterdir():
#      key = keydir.name
#      nlst = sum(1 for _ in keydir.iterdir())
#      lst = []
#      for i in range(nlst):
#        p = keydir / str(i)
#        with p.open(mode='rb') as f:
#          lattice = pickle.load(f)
#          lst.append(lattice)
#      hashtable[key] = lst
#    self.levels[n] = hashtable

  def load_level(self,n):
    lvldir = Path("reducts") / str(n)
    lvlset = set()
    for p in lvldir.iterdir():
      with p.open(mode='rb') as f:
        lattice = pickle.load(f)
        lvlset.add(lattice)
    self.levels[n] = lvlset

#  def load_level(self,n):
#    lvldir = Path("mults") / str(n) / "lattices"
#    lvlset = set()
#    for p in lvldir.iterdir():
#      with p.open(mode='rb') as f:
#        lattice = pickle.load(f)
#        lvlset.add(lattice)
#    for l in lvlset:
#      print(l._relation)
#      print(l._multiplications)

  def build_level(self,n):
    if n==1:
      self.levels[1] = {"1-1-0-0":[UpperTriangularMatrix(1)]}
    else:
      level = self.levels[n-1]
      hashtable = dict()
      for key,lst in level.items():
        for lattice in lst:
          children = lattice.get_children()
          for child in children:
            profile = child.get_profile()
            key = self.get_hash(profile)
            if key not in hashtable:
              hashtable[key] = [child]
            else:
              lst = hashtable[key]
              known = False
              for r in lst:
                if self.is_isomorphic(child,r):
                  known = True
                  break
              if not known:
                lst.append(child)
      self.levels[n] = hashtable

  def get_hash(self,profile):
    slst = sorted(profile) # sorts profile in lexicographic order
    flatlist = sum(slst,()) # concatenation
    key = "-".join(str(i) for i in flatlist)
    return key

  def is_isomorphic(self,L1,L2):
    check = IsomorphismCheck(L1,L2)
    result = check.run([])
    return result

  def build_residuated(self,k):
    count = 0
    prefix = Path("mults") / str(k)
    prefix.mkdir(parents=True)
    prefix0 = prefix / "reducts"
    prefix0.mkdir()
    prefix1 = prefix / "lattices"
    prefix1.mkdir()
    lvlset = set()
    lvlset = self.levels[k]
    while lvlset:
      lattice = lvlset.pop()
      count += 1
      mcount = 0
      p0 = prefix0 / str(count)
      with p0.open(mode='wb') as f0:
        pickle.dump(lattice._relation,f0)
      time0 = time.time()
      mlst = lattice.get_multiplications()
      time1 = time.time() - time0
      if time1 > 600:
        print("very difficult lattice: %s in %s seconds" % (count,time1))
      elif time1 > 300:
        print("difficult lattice: %s in %s seconds" % (count,time1))
      for key,lst in mlst.items():
        mcount += len(lst)
      p1 = prefix1 / ("%s_%s" % (count,mcount))
      with p1.open(mode='wb') as f:
        pickle.dump(lattice,f)

############################

#count = 0
##result = {}
#result = 0
#start_time = time.time()
#with shelve.open("shelves/lat3.db",flag='r') as shelf:
#  for key,lst in shelf.items():
#    for lattice in lst:
#      count += 1
##      if lattice.is_relatively_complemented():
##        result += 1
##      h = lattice.height()
##      w = lattice.width()
##      if (h,w) in result:
##        result[(h,w)] += 1
##      else:
##        result[(h,w)] = 1
#      if count % 1000 == 0:
#        print("*",end="",flush=True)
#print("--- %s seconds ---" % (time.time() - start_time))
#print(count)
#print(result)

start_time = time.time()
n = 12
count = 0
result = {}
p = Path("pickles/level%s.db" % n)
with p.open(mode='rb') as f:
  lvlset = pickle.load(f)
  for encoding in lvlset:
    count += 1
    rlat = ResiduatedLattice.decode(encoding,n)
    row = [0] * 10
    if rlat.is_modular():
      row[0] = 1
    if rlat.is_distributive():
      row[1] = 1
    if rlat.satisfies_pi1():
      row[2] = 1
    if rlat.is_prelinear():
      row[3] = 1
    if rlat.satisfies_pi2():
      row[4] = 1
    if rlat.is_strict():
      row[5] = 1
    if rlat.satisfies_wnm():
      row[6] = 1
    if rlat.is_divisible():
      row[7] = 1
    if rlat.is_involutive():
      row[8] = 1
    if rlat.is_idempotent():
      row[9] = 1
    key = tuple(row)
    if key in result:
      result[key] += 1
    else:
      result[key] = 1
    if count % 100000 == 0:
      print("*",end="",flush=True)
print("--- %s seconds ---" % (time.time() - start_time))
print(count)
print(result)
print(len(result))

#count = 0
#mcount = 0
##result = {}
#result = [0] * 10
#start_time = time.time()
##lvlset = set()
#with shelve.open("shelves/reslat10.db",flag='r') as shelf:
#  for lattice_id,lattice in shelf.items():
#    count +=1
##    h = lattice.height()
##    w = lattice.width()
#    for key,lst in lattice._multiplications.items():
#      for mult in lst:
#        rlat = ResiduatedLattice(lattice,mult.table)
#        mcount += 1
##        encoding = rlat.encode()
##        lvlset.add(encoding)
#        if rlat.is_modular():
#          result[0] += 1
#        if rlat.is_distributive():
#          result[1] += 1
#        if rlat.satisfies_pi1():
#          result[2] += 1
#        if rlat.is_prelinear():
#          result[3] += 1
#        if rlat.satisfies_pi2():
#          result[4] += 1
#        if rlat.is_strict():
#          result[5] += 1
#        if rlat.satisfies_wnm():
#          result[6] += 1
#        if rlat.is_divisible():
#          result[7] += 1
#        if rlat.is_involutive():
#          result[8] += 1
#        if rlat.is_idempotent():
#          result[9] += 1
#        if mcount % 100000 == 0:
#          print("*",end="",flush=True)
##    if (h,w) in result:
##      result[(h,w)] += m
##    else:
##      result[(h,w)] = m
##    if count % 1000 == 0:
##      print("*",end="",flush=True)
##p = Path("pickles/level1.db")
##with p.open(mode='wb') as f:
##  pickle.dump(lvlset,f)
#print("--- %s seconds ---" % (time.time() - start_time))
#print(count)
#print(mcount)
#print(result)

#start_time = time.time()
#count = 0
## dcount = 0
#path = Path("mults/1/lattices")
#with shelve.open("shelves/reslat1.db") as shelf:
#  for p in path.iterdir():
#    with p.open(mode="rb") as f:
#      lattice_id = p.name.split("_")[0]
#      lattice = pickle.load(f)
#      shelf[lattice_id] = lattice
##    distributive = True
##    for a in range(n):
##      for b in range(n):
##        for c in range(n):
##          if inf[a][sup[b][c]] != sup[inf[a][b]][inf[a][c]]:
##            distributive = False
##    if distributive:
##      dcount += 1
#      count += 1
#      if count % 1000 == 0:
#        print("*",end="",flush=True)
##    for key,lst in lattice._multiplications.items():
##      count += len(lst)
#print("--- %s seconds ---" % (time.time() - start_time))
#print(count)

##############################

#lit = LatticeGenerator()
#lit.load_level(1)
#with shelve.open("shelves/lat1.db") as shelf:
#  for key,lst in lit.levels[1].items():
#    shelf[key] = lst

#n = 12
#start_time = time.time()
#lit = LatticeGenerator()
#lit.load_level(n)
#lit.build_residuated(n)
#print("--- %s seconds ---" % (time.time() - start_time))
#lit.build_level(12)
#lit.store_level(12)
#print("--- %s seconds ---" % (time.time() - start_time))

