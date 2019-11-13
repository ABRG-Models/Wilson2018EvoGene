# Implementation of the model described in the paper 'Limit cycle dynamics can guide the evolution of gene regulatory networks towards point attractors'

## A summary of the paper

The paper associated with this code repository considers a system of
Boolean gene regulator networks. I'll include a short summary of the
system which this code implements.


![Figure 1](/paper/figures/Fig1.jpg)

## The code

This implementation of the Boolean network model is written in C++,
writing out data in text files (comma separated values) into the
directory data/. It has some python scripts for data visualisation in
the subdirectory plot/ and scripts to run multiple instances of the
model in the subdirectory scripts/.

The code is flexible enough to specify 3, 4, 5 or 6 genes for the 'k=n'
network in which every gene receives input from every other gene,
including itself. It can also compute an n=k-1 network for 7
genes. The number of genes, as well as the choice of k=n-1 or k=n and
some other features are set at compile time.

The code builds using cmake. There is a cpp file for every program,
though some programs are compiled into several binaries, with
different #defines resulting in different program behaviour. Consult
the **sim(_supp)/CMakeLists.txt** file for details of the compilation.

The state space is represented by the type state_t (which is an
unsigned char). This contains sufficient bits for 4, 5 or 6 genes. The
genome space is represented by a fixed size array of genosect_t (which
is set to either an unsigned int or an unsigned long long int at
compile time). There are N_Genes genosect_t variables in a full
genome, but not all bits of each genosect_t may be used. For 'k=n',
2^(N_Genes) bits are required in each genosect_t (That's 16 for
N_Genes=4, 32 for N_Genes=5 and 64 for N_Genes=6).

The main, reported program code is in the directory
sim/. Supplementary analysis code is in sim_supp/. There are some
CTests in tests/. Results are written into data/. There are python
scripts in plot/ to visualise the results. factorial/ contains some
code by Peter Luschny for computing factorials. You should build in
build/.

## Prerequisites:

cmake, a c++ compiler and the libraries mpir and jsoncpp are required. On Ubuntu or Debian:

```bash
sudo apt install cmake build-essential
```
Ensures you have a compiler and cmake.

You will then need to obtain, build and install mpir from github:
git://github.com/wbhart/mpir.git (see also http://mpir.org)


I compiled mpir like this:
```bash
sudo apt install libtool autoconf yasm texinfo # Required only for the mpir build
git clone git://github.com/wbhart/mpir.git
cd mpir
autoreconf -is # I ignored a couple of warnings here
./configure --enable-cxx --prefix=/usr/local
make -j6 # or however many cores you have
sudo make install
sudo ldconfig # To ensure your system's dynamic linker can find the new libraries
```

I compiled jsoncpp like this:
```sh
git clone https://github.com/open-source-parsers/jsoncpp.git
cd jsoncpp
mkdir build
cd build
cmake ..
make
sudo make install
```

## Compiling

You should create a sub-directory called build to compile
AttractorScaffolding.

```bash
mkdir -p build && pushd build
cmake .. # alternatively use `CXX=icpc cmake ..` or `CXX=clang++ cmake ..` to compile with an optimised compiler
make -j6 # or however many cores you have
popd
```

## Running

See the sim/README.md for details about all the programs that are
compiled in build/sim/

To reproduce the essential result of this work, first run:

```
cd ./scripts/
./runevolve_c2.sh
```

This will generate data files in data/. These can then be plotted with
plot/main/fig4.py.

```
cd plot/main
python fig4.py
```

The result of exhaustively searching the n=3 gene system can be
reproduced by running:

```
./build/sim/proprandom3
```

## Directories

### sim

Simulation programs and header files.

### sim_supp

Supplementary simulation programs.

### standalone

The standalone implementation, evolve.cpp.

### scripts

Some bash scripts to run the programs in **sim/** and **sim_supp/**.

### data

A directory into which the results of simulations are written.

### plot

Scripts to plot results from data found in **data/**.

### combinatorics

Contains a document analysing the probability of fit states as a
function of the ending limit cycle size.

### factorial

Contains factorial code from Peter Luschny and some test programs
using this library.

### tests

A few unit testing programs.
