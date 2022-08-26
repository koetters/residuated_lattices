class ResiduatedLattice:

    def __init__(self,domain,line_diag,prod_matrix,arrow_matrix):

        self.domain = domain
        self._row = {x:i for i,x in enumerate(self.domain)}
        self._col = self._row

        self._strict_order = self._transitive_closure(line_diag)

        self._meet_matrix = []
        self._join_matrix = []
        for x in self.domain:
            mrow = []
            jrow = []
            for y in self.domain:
                mrow.append(self._meet(x,y))
                jrow.append(self._join(x,y))
            self._meet_matrix.append(mrow)
            self._join_matrix.append(jrow)

        self._prod_matrix = prod_matrix
        self._arrow_matrix = arrow_matrix
        self.one = self._maximal_element(set(self.domain))
        self.zero = self._minimal_element(set(self.domain))

    def _transitive_closure(self,line_diag):

        ld = set(line_diag)
        tc = ld.copy()

        while True:
            ntc = len(tc)
            tc = tc | self._compose_relations(tc,ld)
            if ntc == len(tc):
                break
    
        return list(tc)

    def _compose_relations(self,A,B):
        result = set()
        for a,b in A:
            for c,d in B:
                if b==c:
                    result.add((a,d))
        return result

    def _meet(self,x,y):
        lower = self._prime_ideal(x) & self._prime_ideal(y)
        return self._maximal_element(lower)

    def _join(self,x,y):
        upper = self._prime_filter(x) & self._prime_filter(y)
        return self._minimal_element(upper)

    def _prime_ideal(self,x):
        lower = set(p for p,q in self._strict_order if q==x)
        lower.add(x)
        return lower

    def _prime_filter(self,x):
        upper = set(q for p,q in self._strict_order if p==x)
        upper.add(x)
        return upper

    def _maximal_element(self,A):
        result = A.copy()
        for p,q in self._strict_order:
            if p in A and q in A:
                result.discard(p)
        if len(result) != 1:
            raise ValueError
        return result.pop()

    def _minimal_element(self,A):
        result = A.copy()
        for p,q in self._strict_order:
            if p in A and q in A:
                result.discard(q)
        if len(result) != 1:
            raise ValueError
        return result.pop()

    def meet(self,x,y):
        return self._meet_matrix[self._row[x]][self._col[y]]

    def join(self,x,y):
        return self._join_matrix[self._row[x]][self._col[y]]

    def prod(self,x,y):
        return self._prod_matrix[self._row[x]][self._col[y]]

    def arrow(self,x,y):
        return self._arrow_matrix[self._row[x]][self._col[y]]

