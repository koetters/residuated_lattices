from prog import LatticeSchema,ResiduatedSchema
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
  ("MTL-algebra", ["prelinear"]),
  ("SMTL-algebra", ["prelinear","pi2"]),
  ("WNM-algebra", ["prelinear","weak nilpotent minimum"]),
  ("BL-algebra", ["prelinear","divisible"]),
  ("SBL-algebra", ["prelinear","divisible","pi2"]),
  ("IMTL-algebra", ["prelinear","involutive"]),
  ("Heyting algebra", ["divisible","idempotent"]),
  ("G-algebra", ["prelinear","divisible","idempotent"]),
  ("NM-algebra", ["prelinear","involutive","weak nilpotent minimum"]),
  ("MV-algebra", ["divisible","involutive"]),
  ("Pi-algebra", ["prelinear","divisible","pi1","pi2"]),
  ("PiMTL-algebra", ["prelinear","pi1","pi2"]),
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

