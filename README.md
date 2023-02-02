# residuated_lattices
Usage: python gui.py

The command launches a graphical user interface, from where a number of formal contexts can be viewed,
which show the numbers of lattices, or residuated lattices, for each combination of properties,
inspired by the paper "Residuated Lattices of Size <= 12, Extended Version" of Radim Belohlavek and Vilem Vychodil.
The script generate.py allows to generate all lattices, and residuated lattices, of size <= 12,
and also the mentioned formal contexts (the computations take about 1-2 days for n=12). It is also possible
to compute custom contexts, but this is currently an undocumented feature.

Below is the documentation for an older version of the program. The features described there are still available,
but have not yet been integrated in the newer version.

--------------------------------------------------------------------------------------------------------------------

Check if a given algebra of type (2,2,2,2,0,0) is a residuated lattice (i.e. satisfies the axioms).

Usage: python check.py \<algebra to be checked\>

Getting Started: Try one of the examples, packaged with this program. After downloading the directory,
start a command line shell, move into the directory, and type "python check.py example1_8".
If all goes well, the program should print stuff on the command line, about axioms being failed, and then end.
You can find the algebra, that has just been checked, in the file example1_8.py (note that the ".py" suffix
was omitted when you ran the command). Open the file in a text editor. The file contains the definition of the algebra.
For details, see the comment lines in that file. If you edit the file, changing the single "0" in the "arrow_matrix" to a "1",
and run the program again, it will confirm that all axioms are now satisfied. The other example files (example1_9.py, ...)
have the same structure; you can use any of these as a template, to define your own algebras.

Axioms: The file check.py contains the 13 axioms that we use to define residuated lattices:
residuated lattices are bounded lattices, equipped with an additional multiplication which forms an ordered monoid
(with the lattice maximum "1" as the neutral element), and also equipped with an arrow operation,
such that multiplication and arrow operation, for any fixed first operand x, form an adjoint pair
(with the former in the role of the the supremum-preserving, and the latter in the role of the infimum-preserving function).
One word of caution: There seems to be no established consensus on the axioms defining a residuated lattice;
other people may use a somewhat different set of axioms.

Extra feature: compute (f,g)-derivations.
Usage: python deriv.py \<algebra\>
This will list the endomorphism of the algebra. Choose f and g from this list.
The (f,g)-derivations are then computed.
