# GWSAT and GA Implementation

## Package
1. **main.py**: Main entry point for the program which executes `GWSAT` or `GA` accordingly
2. **localsearch.py**: TSP Python code. Functionality offered from here are used in `GWSAT` and `GA` implementation
3. **gwsat.py**: `GWSAT` implementation
4. **ga.py**: `GA` implementation

## Prerequistes
1. **Python**: version 3.7.0 or higher
2. **Dependencies**: matplotlib, run `pip3 install matplotlib` in terminal to install. If it does not work, try `pip install matplotlib` to install the dependencies

For information on how to install python, follow this [link](https://www.python.org/downloads/)

For information on how to install pip/pip3, follow this [link](https://pip.pypa.io/en/stable/installing/)

## Execution
 **General Format**: `python main.py <algorithm> <filename>`
###### How to run GWSAT
 *Example*: `python main.py gwsat sat/uf20-02.cnf`
###### How to run GA
*Example*: `python main.py ga ga/aes-mul_8_9.wcnf`

## Input File Format
If you wish to run `GWSAT` or `GA` against a dataset different than a one give, follow this guideline
1. Store the input file for `GA` in the folder `ga`
2. Store the input file for `GWSAT` in the folder `sat`

###### Format
**Comments** : Comment line give human-readable information about the file and
are ignored by programs. Comment lines appear at the beginning of the
preamble. Each line begins with a lower-case character c

**Problem line** : There is one problem line per input file. The problem line must
appear before any node or arc descriptor lines. For cnf instances, the problem
line has the following format.

`p FORMAT VARIABLES CLAUSES`

The lower-case character p means that this is the problem line. The FORMAL
field allows programs to determine the format that will be expected, and should
contains the word “cnf”. The VARIABLES field contains an integer value
specifying n, the number of variables in the instance. The CLAUSES field
contains an integer value specifying m, the number of clauses in the instance.
This line must occur as the last line of the preamble.

**The CLAUSES** : The clauses appear immediately after the problem line. The
variables are assumed to be numbered from 1 up to n. It is not necessary that
every variable appear in an instance. Each clause will be represented by a
sequence of number, each separated by either a space, a tab, or a newline
character. The non-negated version of a variable i is represented by i; the
negated version is represented by -i.

Each clause is terminated by “0”. Unlike many formats that represent the end of a
clause by a new-line symbol, this format allows clauses to be on multiple lines.

*Example*: `(x 1 ∨ x 3 ∨ -x 4 ) ∧ (x 4 ) ∧ (x 2 ∨ -x 3 )`

A possible input file would be

```
c Example CNF format file
c
p cnf 4 3
1 3 -4 0
4 0 2
-3 0
```






