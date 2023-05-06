from prog import LatticeSchema,ResiduatedSchema
import attributes as lp

lattice_properties = LatticeSchema("lattices - standard properties", {
  "modular": lp.modular,
  "distributive": lp.distributive,
  "complemented": lp.complemented,
  "Boolean": lp.boolean,
  "relatively complemented": lp.relatively_complemented,
  "pseudo-complemented": lp.pseudocomplemented,
  "relatively pseudo-complemented": lp.relatively_pseudocomplemented,
})

lattice_dimensions = LatticeSchema("lattices - width and height", {
  "height": lp.height,
  "width": lp.width,
})

residuated_properties = ResiduatedSchema("residuated lattices - standard properties", {
  "modular": lp.modular,
  "distributive": lp.distributive,
  "prelinear": lp.prelinear,
  "pi1": lp.pi1,
  "pi2": lp.pi2,
  "strict": lp.strict,
  "weak nilpotent minimum": lp.wnm,
  "divisible": lp.divisible,
  "involutive": lp.involutive,
  "idempotent": lp.idempotent,
})

residuated_dimensions = ResiduatedSchema("residuated lattices - width and height", {
  "height": lp.height,
  "width": lp.width,
})

#special_algebras = DerivedSchema("residuated lattices - special algebras", {
#  "MTL-algebra" : [],
#  "SMTL-algebra" : [],
#  "WNM-algebra" : [],
#  "BL-algebra" : [],
#  "SBL-algebra" : [],
#  "IMTL-algebra" : [],
#  "G-algebra" : [],
#  "NM-algebra" : [],
#  "MV-algebra" : [],
#  "Pi-algebra" : [],
#  "PiMTL-algebra" : [],
#})

extra_properties = ResiduatedSchema("residuated lattices - extra properties", {
  "semi-prelinear": lp.semi_prelinear,
  "semi-idempotent": lp.semi_idempotent,
  "semi-divisible": lp.semi_divisible,
  "deMorgan": lp.demorgan,
  "Stonean": lp.stonean,
  "semi-G-algebra": lp.semig,
})

