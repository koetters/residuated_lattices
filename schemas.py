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

extra_properties = ResiduatedSchema("residuated lattices - extra properties", [
  ("semi-prelinear", lp.semi_prelinear),
  ("semi-idempotent", lp.semi_idempotent),
  ("semi-divisible", lp.semi_divisible),
  ("deMorgan", lp.demorgan),
  ("Stonean", lp.stonean),
  ("semi-G-algebra", lp.semig),
])

all_properties = ResiduatedSchema("residuated lattices - all properties", [
  ("MOD", lp.modular),
  ("DIS", lp.distributive),
  ("MTL", lp.prelinear),
  ("P1", lp.pi1),
  ("P2", lp.pi2),
  ("STR", lp.strict),
  ("WNM", lp.wnm),
  ("DIV", lp.divisible),
  ("INV", lp.involutive),
  ("IDE", lp.idempotent),
  ("S-MTL", lp.semi_prelinear),
  ("S-DIV", lp.semi_divisible),
  ("DMO", lp.demorgan),
  ("STO", lp.stonean),
  ("S-G", lp.semig),
  ("QCO", lp.quasicomplemented),
])
