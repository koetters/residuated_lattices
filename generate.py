import sys
from prog import DataStore

if len(sys.argv) == 1:
  ds = DataStore()
  ds.populate(12)

else:
  name = sys.argv[1]
  module = __import__('schemas')
  schema = getattr(module,name)
  ds = DataStore()
  ds.build_contexts(schema,12)

