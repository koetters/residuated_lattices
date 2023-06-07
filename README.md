# residuated_lattices
The program does computations on residuated lattices. It has the following features:

1. Check if a given algebra of type (2,2,2,2,0,0) is a residuated lattice

2. Generate all residuated lattices with up to n elements, where 1 <= n <= 12  
   (for n=12, this takes about 2 days and requires 16GB RAM)

3. Create formal contexts (cf. Ganter & Wille, "Formal concept analysis") from the stored  
   residuated lattices. These formal contexts show the number of residuated lattices with  
   given properties, or combinations of properties. This feature was inspired by a paper  
   of Belohlavek & Vichodyl, "Residuated Lattices of Size <= 12 -- Extended Version",  
   which shows such contexts. The paper also provides a link to the a database of residuated  
   lattices (cf. item 2.) above), but the link seems no longer active at the time of this writing.

4. View the formal contexts in a bare-bones graphical user interface.

Below you find instructions on how to use these features:
## Checking if an algebra of type (2,2,2,2,0,0) is a residuated lattice
First, create a Python file which describes the algebra. The files expl1.py, expl2.py, expl3.py,  
expl4.py, expl5.py and expl6.py can be used as templates. To check e.g. for expl1.py,  
run **python check.py expl1** (without the .py ending!!!).

## Generate all residuated lattices with up to n elements
Running **python generate.py** creates a `data` folder in the same folder which contains  
the Python file, and writes files lat<n\>.db and reslat<n\>.db into that folder.  
The file lat<n\>.db contains all lattices with exactly n elements, up to isomorphism  
(i.e. it contains exactly one lattice from each isomorphism class). Likewise, reslat<n\>.db  
contains all residuated lattices with exactly n elements, up to isomorphism. By default,  
the program generates all files up to (and including) n=10. If you want to change this  
to n=12, open the file generate.py with a text editor, and change *ds.populate(10)*  
to *ds.populate(12)* (but note that it will take about 2 days and requires 16GB RAM).  
The size of the data folder, after generating the (residuated) lattices, will be 12MB for n=10,  
and 1.7GB for n=12. For convenience, the source tree contains a tarball `data.tar.gz`,  
size 427MB, which has all lattices and residuated lattices up to n=12 precomputed,  
but due to GitHubs large file policy, you might have to download it separately.

The files lat<n\>.db and reslat<n\>.db are stored as Python pickles  
(https://docs.python.org/3/library/pickle.html). While the program takes care of this,  
it should be pointed out that the use of pickles from an untrusted source is considered  
unsafe practice, because evil people are known to put malicious code in their pickles.  
Which I didn't do, of course, but I wanted to make you aware of the potential concern.  

## Create formal contexts from the (residuated) lattice data
Once you have the data files, you can generate formal contexts from the data.  
This is done by running **python generate.py <schema\>**, where by default,  
**<schema\>** can be one of the following: lattice_properties, residuated_properties,  
special_algebras, all_properties, publication_properties.  
This will create a formal context for each 1<=n<=10, which describes the (residuated)  
lattices with n elements (to create contexts up to n=12, open the file `generate.py`  
in a text editor, and replace the line *n=10* by *n=12*, but as before, the case n=12  
can take a long time, like 1-2 days, and probably also requires 16GB RAM).  
The context files themselves are small, and are stored beneath the `context` folder.  
The `context` folder in the source tree already contains precomputed contexts;  
unlike the data files, the context files are small (in the KB range);  
they are stored as Python pickles (cf. the remark in the previous section).  

You can also create your own formal contexts, but this involves some programming.  
In the file `schemas.py`, create a Lattice Schema object (if you want to study lattices)  
or a ResiduatedSchema object (if you want to study residuated lattices).  
The existing schemas in `schemas.py` can be used as a template.  
As you can see, in order to create a schema, you have to provide a name,  
and a list of pairs (m,f), where m is the name of some property of (residuated) lattices,  
and f is a Python function which takes a (residuated) lattice as its argument,  
and returns True if the (residuated) lattice has the property, and False otherwise.  
You can choose the existing functions from the file `attributes.py`. In this case,  
creating a ResiduatedSchema is easy. But you can also write your own functions.

## Viewing formal contexts
Running **python gui.py** starts a graphical user interface. In the top right pane,    
you see a list of available context schemas, for which contexts have been computed.  
If you click on one of them, a row of numbers will appear in the bottom right pane,  
and below the numbers, you can see two buttons, "Aggregate" and "Sum".  
Clicking on one of the numbers, say n, will show the formal context describing the  
(residuated) lattices with exactly n elements. Clicking on the "Sum" button will show  
a derived context, which shows the formal context for (residuated) lattices with any  
number of elements, up to the maximum n in the row above. Clicking on the "Aggregate"  
button shows a table with numbers n in the top row, and property names in the left row,  
the entries are the numbers of lattices with n elements having the respective properties.  
By selecting the precomputed schemas "lattices - standard properties",  
"residuated lattices - standard properties" and "residuated lattices - special algebras"  
the tables in the appendix of Belohlavek and Vichodyl's paper  
"Residuated Lattices of Size <= 12 -- Extended Version" can be reproduced.  
There are also schemas "lattices - width and height" and  
"residuated lattices - width and height", but they do not produce formal contexts  
(they produce many-valued contexts, cf. Ganter & Wille "Formal Context Analysis").




