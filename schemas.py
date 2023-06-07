from prog import LatticeSchema,ResiduatedSchema,DerivedSchema
import attributes as lp

lattice_properties = LatticeSchema("lattices - standard properties", [
  ("modular", lp.modular),
  ("distributive", lp.distributive),
  ("complemented", lp.complemented),
  ("Boolean", lp.boolean),
  ("relatively complemented", lp.relatively_complemented),
  ("pseudo-complemented", lp.pseudocomplemented),
  ("relatively pseudo-complemented", lp.relatively_pseudocomplemented),
])

lattice_dimensions = LatticeSchema("lattices - width and height", [
  ("height", lp.height),
  ("width", lp.width),
])

residuated_properties = ResiduatedSchema("residuated lattices - standard properties", [
  ("modular", lp.modular),
  ("distributive", lp.distributive),
  ("prelinear", lp.prelinear),
  ("pi1", lp.pi1),
  ("pi2", lp.pi2),
  ("strict", lp.strict),
  ("weak nilpotent minimum", lp.wnm),
  ("divisible", lp.divisible),
  ("involutive", lp.involutive),
  ("idempotent", lp.idempotent),
])

special_algebras = DerivedSchema("residuated lattices - special algebras", residuated_properties, [
  ("MTL", ["prelinear"]),
  ("SMTL", ["prelinear","pi2"]),
  ("WNM", ["prelinear","weak nilpotent minimum"]),
  ("BL", ["prelinear","divisible"]),
  ("SBL", ["prelinear","divisible","pi2"]),
  ("IMTL", ["prelinear","involutive"]),
  ("Heyting", ["divisible","idempotent"]),
  ("G", ["prelinear","divisible","idempotent"]),
  ("NM", ["prelinear","involutive","weak nilpotent minimum"]),
  ("MV", ["divisible","involutive"]),
  ("Pi", ["prelinear","divisible","pi1","pi2"]),
  ("PiMTL", ["prelinear","pi1","pi2"]),
])

residuated_dimensions = ResiduatedSchema("residuated lattices - width and height", [
  ("height", lp.height),
  ("width", lp.width),
])

all_properties = ResiduatedSchema("residuated lattices - all properties", [
  ("MOD", lp.modular),
  ("DIS", lp.distributive),
  ("MTL", lp.prelinear),
  ("S-MTL", lp.semi_prelinear),
  ("P1", lp.pi1),
  ("WNM", lp.wnm),
  ("DIV", lp.divisible),
  ("S-DIV", lp.semi_divisible),
  ("INV", lp.involutive),
  ("IDE", lp.idempotent),
  ("S-IDE", lp.semi_idempotent),
  ("DMO", lp.demorgan),
  ("STO", lp.stonean),
  ("BOO", lp.boolean),
  ("IMP", lp.imp),
])

mixed_properties = ResiduatedSchema("residuated lattices - mixed properties", [
  ("MTL", lp.prelinear),
  ("S-MTL", lp.semi_prelinear),
  ("IDE", lp.idempotent),
  ("S-IDE", lp.semi_idempotent),
  ("DIV", lp.divisible),
  ("S-DIV", lp.semi_divisible),
  ("DMO", lp.demorgan),
  ("STO", lp.stonean),
])

publication_properties = ResiduatedSchema("residuated lattices - publication properties", [
  ("MTL", lp.prelinear),
  ("S-MTL", lp.semi_prelinear),
  ("IDE", lp.idempotent),
  ("S-IDE", lp.semi_idempotent),
  ("DIV", lp.divisible),
  ("S-DIV", lp.semi_divisible),
  ("DMO", lp.demorgan),
  ("STO", lp.stonean),
  ("INV", lp.involutive),
  ("BOO", lp.boolean),
])

