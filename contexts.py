from prog import ContextSchema
import attributes as lp

schemas = []

schemas.append(ContextSchema("lattices - standard properties",[
  lp.modular,
  lp.distributive,
  lp.complemented,
  lp.boolean,
  lp.relatively_complemented,
  lp.pseudocomplemented,
  lp.relatively_pseudocomplemented,
]))

schemas.append(ContextSchema("height and width",[
  lp.height,
  lp.width,
]))

