import sys
import time
import pickle
from pathlib import Path

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

  def __str__(self):
    return str(self._relation)

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
#    return mg.run()
    mg.run()
    self._multiplications = mg.multiplications
    return mg.multiplications

class TableBuilder:
  def __init__(self,lattice):
    n = lattice.n
    self.lattice = lattice
    supremum = lattice.supremum_operation()
    infimum = lattice.infimum_operation()
    self.sup = supremum.table
    self.inf = infimum.table
    self.ideal = [None for _ in range(n)]
    self.ideal[0] = {0}
    for i in range(1,n):
      self.ideal[i] = self.ideal[i-1] | {self.sup[i][j] for j in range(0,i)}
#    self.delta = [None for _ in range(n)]
#    self.delta[0] = {0}
#    for i in range(1,n):
#      self.delta[i] = self.ideal[i] - self.ideal[i-1]
    self.mult = [n*[None] for _ in range(n)]
    for i in range(n):
      self.mult[0][i] = 0
      self.mult[i][0] = 0
      self.mult[n-1][i] = i
      self.mult[i][n-1] = i
    self.results = []

  def build_table(self):

    n = self.lattice.n
    pos = None
    for k,i in ((k0,i0) for k0 in range(n) for i0 in range(k0+1)):
      if self.mult[k][i] == None:
        pos = (k,i)
        break

    if pos == None:
      m = self.mult
      s = self.sup
      for a in range(n):
        for b in range(n):
          for c in range(n):
            assert m[m[a][b]][c] == m[a][m[b][c]]
            assert m[a][s[b][c]] == s[m[a][b]][m[a][c]]
      copy = [n*[None] for _ in range(n)]
      for r in range(n):
        for s in range(n):
          copy[r][s] = self.mult[r][s]
      self.results.append(copy)
      return

    k,i = pos

#    print("pos=(%s,%s)" % (k,i))
#    print("table:")
#    print(self.mult)

    below_k = self.lattice.lower_neighbor(k)
    below_i = self.lattice.lower_neighbor(i)
    lbound = self.sup[self.mult[k][below_i]][self.mult[below_k][i]]
    ubound = self.inf[k][i]

#    print("next pos (%s,%s) in (%s,%s)" % (k,i,lbound,ubound))
    for a in range(lbound,ubound+1):
      if not (self.lattice.leq(lbound,a) and self.lattice.leq(a,ubound)):
        continue

      undo = [(k,i)]
      self.mult[k][i] = a
      self.mult[i][k] = a
#      print("trying mult(%s,%s)=%s from (%s,%s)" % (k,i,a,lbound,ubound))
#      print(self.mult)

      valid = True

      for l,j in ((l0,j0) for l0 in self.ideal[k] for j0 in self.ideal[i]):
        x = self.sup[k][l]
        y = self.sup[i][j]
        if self.mult[x][y] == None:
          self.mult[x][y] = self.sup[self.sup[a][self.mult[k][j]]][self.sup[self.mult[l][i]][self.mult[l][j]]]
          self.mult[y][x] = self.mult[x][y]
          undo.append((x,y))
        else:
          if self.mult[x][y] != self.sup[self.sup[a][self.mult[k][j]]][self.sup[self.mult[l][i]][self.mult[l][j]]]:
            valid = False
            break

      if valid:
        for j in range(k):
          if self.mult[self.mult[k][i]][j] != self.mult[k][self.mult[i][j]]:
            valid = False
            break

      if valid:
        self.build_table()

      for x,y in undo:
        self.mult[x][y] = None
        self.mult[y][x] = None

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
    return self.fill_table(mult,0,0)

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
#    tb = TableBuilder(lattice)
#    tb.build_table()
#    for m in tb.results:
#      print(m)
#    mlst = lattice.get_multiplications()
#    for key,lst in mlst.items():
#      count += len(lst)
    prefix = Path("mults") / str(k)
    prefix.mkdir(parents=True)
    prefix0 = prefix / "reducts"
    prefix0.mkdir()
    prefix1 = prefix / "lattices"
    prefix1.mkdir()
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


n = 12
start_time = time.time()
lit = LatticeGenerator()
lit.load_level(n)
lit.build_residuated(n)
print("--- %s seconds ---" % (time.time() - start_time))
#lit.build_level(12)
#lit.store_level(12)
#print("--- %s seconds ---" % (time.time() - start_time))

