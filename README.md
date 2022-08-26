# residuated_lattices
Check if a given algebra of type (2,2,2,2,0,0) is a residuated lattice (i.e. satisfies the axioms).

Usage: python check.py <algebra>

Getting Started: Try one of the examples, packaged with this program. After downloading the directory,
start a command line shell, move into the directory, and type "python check.py example1_8"
(using Python 2; the program will soon be converted to Python 3).
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

