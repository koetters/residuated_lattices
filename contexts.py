from prog import LatticeContext,ResiduatedContext
import attributes as lp

schemas = []

schemas.append(LatticeContext("lattices - standard properties",[
  lp.modular,
  lp.distributive,
  lp.complemented,
  lp.boolean,
  lp.relatively_complemented,
  lp.pseudocomplemented,
  lp.relatively_pseudocomplemented,
]))

schemas.append(LatticeContext("lattices - height and width",[
  lp.height,
  lp.width,
]))

schemas.append(ResiduatedContext("residuated lattices - standard properties",[
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
]
))

schemas.append(ResiduatedContext("residuated lattices - height and width",[
  lp.height,
  lp.width,
]
))

