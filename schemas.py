from prog import LatticeSchema,ResiduatedSchema
import attributes as lp

lattice_properties = LatticeSchema("lattices - standard properties", [
  lp.modular,
  lp.distributive,
  lp.complemented,
  lp.boolean,
  lp.relatively_complemented,
  lp.pseudocomplemented,
  lp.relatively_pseudocomplemented,
])

lattice_dimensions = LatticeSchema("lattices - width and height", [
  lp.height,
  lp.width,
])

residuated_properties = ResiduatedSchema("residuated lattices - standard properties", [
  lp.modular,
  lp.distributive,
  lp.prelinear,
  lp.pi1,
  lp.pi2,
  lp.strict,
  lp.wnm,
  lp.divisible,
  lp.involutive,
  lp.idempotent,
])

residuated_dimensions = ResiduatedSchema("residuated lattices - width and height", [
  lp.height,
  lp.width,
])

