import sys
from prog import DataStore

if len(sys.argv) == 1:
  ds = DataStore()
  ds.populate(10)

else:
  name = sys.argv[1]
  n = 12
  if len(sys.argv) > 2:
    n = int(sys.argv[2])
  assert 1 <= n <= 12
  module = __import__('schemas')
  schema = getattr(module,name)
  ds = DataStore()
  ds.build_contexts(schema,n)

