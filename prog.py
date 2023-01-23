import os
import pickle
from pathlib import Path
from multiplication_generator import MultiplicationGenerator

class BoundedLattice:

  def __init__(self,order):

    n = len(order)

    # at the moment, the encoding of residuated lattices (used for saving memory) does not support n >= 16,
    # so we make this a restriction for bounded lattices too.
    assert 1 <= n and n < 16

    # assert that the order is reflexive, with least element 0 and greatest element n-1
    for i in range(n):
      assert order[i][i] == 1
      assert order[0][i] == 1
      assert order[i][n-1] == 1

    self.n = n
    self.bottom = 0
    self.top = n-1

    # assert that the order is represented by an upper triangular matrix. this amounts to a topological sorting:
    # if i <= j in the order, then i <= j numerically. this also asserts that the order is antisymmetric.
    for i in range(n):
      for j in range(0,i):
        assert order[i][j] == 0

    # assert that the order is transitive
    for i in range(n):
      for j in range(i,n):
        if order[i][j] == 1:
          for k in range(j,n):
            if order[j][k] == 1:
              assert order[i][k] == 1

    # the lattice order is the supplied order
    self._leq = [n*[None] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        self._leq[i][j] = order[i][j]

    # define the infimum operation. assert that the infimum is unique.
    self._inf = [n*[None] for _ in range(n)]
    for i in range(n):
      for j in range(i,n):
        for k in range(i,-1,-1):
          if self._leq[k][i] and self._leq[k][j]:
            if self._inf[i][j] == None:
              self._inf[i][j] = k
              self._inf[j][i] = k
            else:
              assert self._leq[k][self._inf[i][j]]

    # define the supremum operation. assert that the supremum is unique.
    self._sup = [n*[None] for _ in range(n)]
    for i in range(n):
      for j in range(i,n):
        for k in range(j,n):
          if self._leq[i][k] and self._leq[j][k]:
            if self._sup[i][j] == None:
              self._sup[i][j] = k
              self._sup[j][i] = k
            else:
              assert self._leq[self._sup[i][j]][k]

    # create the profile for each element, and for the lattice as a whole. the profile gathers some structural properties.
    # this is used for isomorphism checks.
    profile = [[0,0,0,0] for _ in range(n)]
    for i in range(n):
      for j in range(i,n):
        if self._leq[i][j] == 1:
          profile[j][0] += 1 # count i in the lower cone of j
          profile[i][1] += 1 # count j in the upper cone of i
        else: # i and j are incomparable
          a = self._inf[i][j]
          b = self._sup[i][j]
          profile[a][2] += 1 # count (i,j) as a generating pair (infimum-wise) for a
          profile[b][3] += 1 # count (i,j) as a generating pair (supremum-wise) for b
    self._profile = [tuple(profile[i]) for i in range(n)]

    self._multiplications = None

  @classmethod
  def decode(self,encoding,n):
    seq = list(encoding)
    order = [[0]*n for _ in range(n)]
    bit = 7
    byte = 0
    for i in range(n):
      for j in range(i,n):
        order[i][j] = (seq[byte] >> bit) & 1
        bit -= 1
        if bit < 0:
          bit = 7
          byte += 1
    return __class__(order)

  def encode(self):
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
        if self._leq[i][j]:
          seq[byte] += (1 << bit)
        bit -= 1
        if bit < 0:
          bit = 7
          byte += 1
    return bytes(seq)

  def __eq__(self,other):
    n = self.n
    if n != other.n:
      return False
    for i in range(n):
      for j in range(n):
        if self._leq[i][j] != other._leq[i][j]:
          return False
    return True

  def __str__(self):
    return str(self._leq)

  def leq(self,i,j):
    return self._leq[i][j]

  def inf(self,i,j):
    return self._inf[i][j]

  def sup(self,i,j):
    return self._sup[i][j]

  # Returns a lower neighbor of i. If i is supremum-irreducible, this is the unique lower neighbor.
  # If i=0 (no lower neighbor exists), None is returned.
  def lower_neighbor(self,i):
    for l in range(i-1,-1,-1):
      if self.leq(l,i):
        return l
    return None

  def profile(self):
    return self._profile

  def hash(self):
    slst = sorted(self._profile) # sorts profile in lexicographic order
    flatlist = sum(slst,()) # concatenation
    value =  "-".join(str(i) for i in flatlist)
    return value

  def children(self):
    n = self.n
    lower = {0,n-1}
    upper = {n}
    rest = set(range(1,n-1))
    return self._find_children(lower,upper,rest)

  def _find_children(self,lower,upper,rest):
    n = self.n
    if rest:
      k = min(rest)
      result = []
      delta = set(self._sup[i][k] for i in lower) - {self.top}
      if delta.isdisjoint(upper):
        lower1 = lower | delta
        upper1 = upper.copy()
        rest1 = rest - delta
        result += self._find_children(lower1,upper1,rest1)
      cone = set(j for j in range(k,n-1) if self._leq[k][j])
      if cone.isdisjoint(lower):
        lower2 = lower.copy()
        upper2 = upper | cone
        rest2 = rest - cone
        result += self._find_children(lower2,upper2,rest2)
      return result
    else:
      assert len(lower)+len(upper) == n+1
      assert lower.isdisjoint(upper)
      order = [[0]*n + [1] for _ in range(n+1)]
      for i in range(n-1):
        for j in range(n-1):
          order[i][j] = self._leq[i][j]
      for i in lower:
        order[i][n-1] = 1
      order[n-1][n-1] = 1
      child = BoundedLattice(order)
      return [child]

  def isomorphic(self,other):
    assert self.n == other.n
    n = self.n
    targets = [[] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        if self._profile[i] == other._profile[j]:
          targets[i].append(j)
    result = self._find_isomorphism(other,[],targets)
    return result

  def _find_isomorphism(self,other,f,targets):
    i = len(f)
    for j in targets[i]:
      if j in f:
        continue
      valid = True
      for l in range(i):
        if self._leq[l][i] != other._leq[f[l]][j]:
          valid = False
      if valid == True:
        if i+1 == len(targets):
          return True
        if self._find_isomorphism(other,f+[j],targets):
          return True
    return False

  def multiplications(self):
    mg = MultiplicationGenerator(self)
    mg.run()
    return mg.multiplications

  def height(self):

    n = self.n
    strict_order = []
    for i in range(n):
      for j in range(i+1,n):
        if self._leq[i][j]:
          strict_order.append((i,j))
    result = 1
    power = strict_order
    while power:
      result += 1
      power = self._product(power,strict_order)
    return result

  # this is just a helper function. it composes the binary relations A and B.
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

class ResiduatedLattice(BoundedLattice):

  def __init__(self,order,mult):
    super().__init__(order)
    n = self.n

    # the lattice multiplication is the supplied multiplication
    self._mult = [n*[None] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        self._mult[i][j] = mult[i][j]

    # the arrow operation is derived
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
    lattice = BoundedLattice.decode(part1,n)

    # decoding the multiplication operation
    seq = list(part2)
    mult = [[None]*n for _ in range(n)]
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

    return ResiduatedLattice(lattice._leq,mult)

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

  def mult(self,i,j):
    return self._mult[i][j]

  def arrow(self,i,j):
    return self._arrow[i][j]

  def encode(self):
    order_encoding = super().encode()
    mult_encoding = self._encode_mult()
    encoding = order_encoding + mult_encoding
    return encoding

  def _encode_mult(self):
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

class DataStore:
  path = "data"
  lattice_prefix = "lat"
  lattice_dict_prefix = "extlat"
  residuated_prefix = "reslat"

  def __init__(self):
    path = Path(__class__.path)
    datadir = self.base_path()
    datadir.mkdir(exist_ok=True)

  def base_path(self):
    path = Path(__class__.path)
    if path.is_absolute() or path.is_relative_to("/"):
      return path
    scriptdir = Path(os.path.dirname(os.path.realpath(__file__)))
    return scriptdir / path

  def lattices_exist(self,n):
    datadir = self.base_path()
    filename = __class__.lattice_prefix + str(n) + ".db"
    path = datadir / filename
    return path.exists()

  def lattice_dict_exists(self,n):
    datadir = self.base_path()
    filename = __class__.lattice_dict_prefix + str(n) + ".db"
    path = datadir / filename
    return path.exists()

  def residuated_exist(self,n):
    datadir = self.base_path()
    filename = __class__.residuated_prefix + str(n) + ".db"
    path = datadir / filename
    return path.exists()

  # FileNotFoundError is raised (by Python) if file does not exist
  def _get_lattices(self,n):
     datadir = self.base_path()
     filename = __class__.lattice_prefix + str(n) + ".db"
     path = datadir / filename
     with path.open(mode='rb') as f:
       data = pickle.load(f)
     return data

  # FileNotFoundError is raised (by Python) if file does not exist
  def _get_lattice_dict(self,n):
    datadir = self.base_path()
    filename = __class__.lattice_dict_prefix + str(n) + ".db"
    path = datadir / filename
    with path.open(mode='rb') as f:
      data = pickle.load(f)
    return data

  # FileNotFoundError is raised (by Python) if file does not exist
  def _get_residuated(self,n):
    datadir = self.base_path()
    filename = __class__.residuated_prefix + str(n) + ".db"
    path = datadir / filename
    with path.open(mode='rb') as f:
      data = pickle.load(f)
    return data

  def lattices(self,n):
    data = self._get_lattices(n)
    for encoding in data:
      lattice = BoundedLattice.decode(encoding,n)
      yield lattice

  def lattices_dict(self,n):
    data = self._get_lattice_dict(n)
    for encoding,nmult in data.items():
      lattice = BoundedLattice.decode(encoding,n)
      yield (lattice,nmult)

  def residuated_lattices(self):
    data = self._get_residuated(n)
    for encoding in data:
      reslat = ResiduatedLattice.decode(encoding,n)
      yield reslat

  def store_lattices(self,data,n):
    datadir = self.base_path()
    filename = __class__.lattice_prefix + str(n) + ".db"
    path = datadir / filename
    with path.open(mode='xb') as f:
      pickle.dump(data,f)

  def store_lattice_dict(self,data,n):
    datadir = self.base_path()
    filename = __class__.lattice_dict_prefix + str(n) + ".db"
    path = datadir / filename
    with path.open(mode='xb') as f:
      pickle.dump(data,f)

  def store_residuated(self,data,n):
    datadir = self.base_path()
    filename = __class__.residuated_prefix + str(n) + ".db"
    path = datadir / filename
    with path.open(mode='xb') as f:
      pickle.dump(data,f)

  def populate(self,nmax=12):
    assert 1 <= nmax and nmax <= 12
    for n in range(1,nmax+1):
      if self.lattices_exist(n):
        print("Lattice Level %s exists" % n)
      else:
        print("Building lattice level %s" % n)
        if n == 1:
          root = BoundedLattice([[1]])
          encoding = root.encode()
          lvlset = {encoding}
          self.store_lattices(lvlset,1)
        else:
          parents = self.lattices(n-1)
          lvlset = set()
          level = dict()
          for lattice in parents:
            children = lattice.children()
            for child in children:
              key = child.hash()
              clst = level.setdefault(key,[])
              if any(child.isomorphic(other) for other in clst):
                continue
              clst.append(child)
              encoding = child.encode()
              lvlset.add(encoding)
          self.store_lattices(lvlset,n)
      if self.residuated_exist(n):
        print("Residuated Lattice Level %s exists" % n)
      else:
        print("Building residuated lattice level %s" % n)
        lattices = self.lattices(n)
        lvlset = set()
        lvldict = dict()
        for lattice in lattices:
          nmult = 0
          hashtable = lattice.multiplications()
          for key,lst in hashtable.items():
            for mult in lst:
              nmult += 1
              reslat = ResiduatedLattice(lattice._leq,mult.table)
              encoding = reslat.encode()
              lvlset.add(encoding)
          latkey = lattice.encode()
          lvldict[latkey] = nmult
        self.store_residuated(lvlset,n)
        self.store_lattice_dict(lvldict,n)

class ContextSchema:

  def __init__(self,name,attributes):
    self.name = name
    self.attributes = attributes
    self.dists = {i:None for i in range(1,13)}

  def propnames(self):
    return [f.name for f in self.attributes]

  def distribution(self,n):
    assert 1 <= n and n <= 12
    if self.dists[n] != None:
      return self.dists[n]
    ds = DataStore()
    it = ds.lattices(n)
    result = dict()
    for lattice in it:
      profile = tuple(f(lattice) for f in self.attributes)
      if profile in result:
        result[profile] += 1
      else:
        result[profile] = 1
    self.dists[n] = result
    return result

if __name__=='__main__':
  ds = DataStore()
  ds.populate(9)

