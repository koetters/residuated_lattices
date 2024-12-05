class ResiduatedMultilattice:

    def __init__(self,domain,line_diag,prod_matrix,arrow_matrix=None):

        # the underlying set (aka domain) of the lattice
        self.domain = domain

        # from the Hasse diagram (line_diag), we obtain the prime ideals and prime filters
        self._prime_ideal = {x:{x} for x in self.domain}
        self._prime_filter = {x:{x} for x in self.domain}
        for x,y in line_diag:
            prime_ideal = frozenset(self._prime_ideal[x])
            prime_filter = frozenset(self._prime_filter[y])
            for u in prime_ideal:
                for v in prime_filter:
                    self._prime_ideal[v].add(u)
                    self._prime_filter[u].add(v)

        # creating "matrices" for the meet, join and product operations
        self._meet_matrix = {x:{} for x in self.domain}
        self._join_matrix = {x:{} for x in self.domain}
        self._prod_matrix = {x:{} for x in self.domain}
        for i,x in enumerate(domain):
            for j,y in enumerate(domain):
                self._meet_matrix[x][y] = self._meet(x,y)
                self._join_matrix[x][y] = self._join(x,y)
                self._prod_matrix[x][y] = prod_matrix[i][j]

        # creating a "matrix" for the arrow operation
        self._arrow_matrix = {x:{} for x in self.domain}
        for i,x in enumerate(domain):
            for j,y in enumerate(domain):
                # if the arrow matrix was not given explicitly, we compute it from the product
                if arrow_matrix is None:
                    self._arrow_matrix[x][y] = self._maximals({z for z in domain if self.leq(self.prod(z,x),y)}).pop()
                else:
                    self._arrow_matrix[x][y] = arrow_matrix[i][j]

        self.one = self._maximals(set(domain)).pop()
        self.zero = self._minimals(set(domain)).pop()

    def _meet(self,x,y):
        return self._maximals(self._prime_ideal[x] & self._prime_ideal[y])

    def _join(self,x,y):
        return self._minimals(self._prime_filter[x] & self._prime_filter[y])

    def _maximals(self,A):
        result = set()
        for x in A:
            if len(self._prime_filter[x] & A) == 1:
                result.add(x)
        return result

    def _minimals(self,A):
        result = set()
        for x in A:
            if len(self._prime_ideal[x] & A) == 1:
                result.add(x)
        return result

    def meet(self,x,y):
        return self._meet_matrix[x][y]

    def join(self,x,y):
        return self._join_matrix[x][y]

    def leq(self,x,y):
        return x in self._prime_ideal[y]

    def prod(self,x,y):
        return self._prod_matrix[x][y]

    def arrow(self,x,y):
        return self._arrow_matrix[x][y]


