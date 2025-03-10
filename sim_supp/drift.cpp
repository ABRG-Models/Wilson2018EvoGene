/*
 * 'Drift' with the p value provided by the user on the command line.
 *
 * The drifting algorithm evolves the genome at every generation, recording how often an f=1 genome
 * is happened upon. With the drift algorithm, all p values should give the same mean time to f=1.

 * Author: S James
 * Date: October 2018.
 */

#include <iostream>
#include <vector>
#include <set>
#include <sstream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

using namespace std;

// Choose debugging level. If you uncomment one of these, then you
// should probably reduce N_Generations
//
// #define DEBUG 1
// #define DEBUG2 1

// Number of genes in a state is set at compile time.
#ifndef N_Genes
# define N_Genes 5
#endif

// The number of generations to evolve for
#ifndef N_Generations
# define N_Generations 100000000
#endif

// Common code
#include "lib.h"

#ifdef RECORD_ALL_FITNESS
# include "basins.h"
# include <algorithm>
#endif

// The fitness function used here
#include "fitness.h"

// Perform a loop N_Generations long during which an initially
// randomly selected genome is evolved until a maximally fit state is
// achieved.
int main (int argc, char** argv)
{
    // Obtain pOn from command line.
    if (argc < 2) {
        LOG ("Usage: " << argv[0] << " pOn");
        LOG ("Supply the probability of flipping a gene during drift, pOn (float, 0 to 1.0f)");
        return 1;
    }
    pOn = static_cast<float>(atof (argv[1]));
    LOG ("Probability of flipping = " << pOn);

    // Seed the RNG.
    unsigned int seed = mix(clock(), time(NULL), getpid());
    srand (seed);
    // Set up the Mersenne Twister RNG
    rngDataInit (&rd);
    zigset (&rd, DUMMYARG);
    rd.seed = seed;

    // Initialise masks
    masks_init();

    // generations records the relative number of generations required
    // to achieve fitness 1.
    vector<unsigned int> generations;

#ifdef RECORD_ALL_FITNESS
    // Records the evolution of the fitness of a genome. Fig 3. The
    // (abs) generation for each fitness is recorded along with the
    // floating point fitness value. Record this in a vector of
    // vectors, with one vector for each evolution towards F=1
    vector<vector<NetInfo> > netinfo;
    vector<NetInfo> ni0;
    netinfo.push_back (ni0);
#endif

    // Set to true when a new, random genome should be generated
    bool need_new_genome = true;

    // Holds the drifting genome
    array<genosect_t, N_Genes> genome;

    unsigned int lastgen = 0;
    double f = 0.0;
#ifdef RECORD_ALL_FITNESS
    double lastf = 0.0;
    AllBasins ab1;
#endif

    // The main loop. Repeatedly evolve from a random genome starting
    // point, recording the number of generations required to achieve a
    // maximally fit state of 1.
    for (unsigned int gen = 0; gen < N_Generations; ++gen) {

        // At the start of the loop, and every time fitness of 1.0 is
        // achieved, generate a random genome starting point.
        if (need_new_genome == true) {
            DBG ("Generate new random genome");
            random_genome (genome);
            need_new_genome = false;
        }

        f = evaluate_fitness (genome);
        DBG2 ("Fitness f = " << f);

#ifdef RECORD_ALL_FITNESS
        ab1.update (genome);
        NetInfo ni(ab1, gen, f);
        ni.deltaF = f - lastf;
        netinfo.back().push_back (ni);
#endif

        // Test fitness to determine whether we should evolve.
        if (f == 1.0) {
            DBG ("Fitness max. F=" << f);
            // Record data
            generations.push_back (gen-lastgen);
            lastgen = gen;

#ifdef RECORD_ALL_FITNESS
            if (gen < N_Generations) {
                vector<NetInfo> vni;
                netinfo.push_back (vni);
            }
            lastf = 0.0;
#endif
            // Reset loop variables
            need_new_genome = true;

        } else {
            evolve_genome (genome);
#ifdef RECORD_ALL_FITNESS
            lastf = f;
#endif
        }
    }

    LOG ("Generations size: " << generations.size());

    // Save data to file. These data files can be graphed using the python scripts.
    ofstream fout;
    stringstream pathss;
    pathss << "./data/drift_";
    pathss << "a" << (unsigned int)target_ant << "_p" << (unsigned int)target_pos << "_";
    pathss << FF_NAME << "_" << N_Generations << "_gens_" << pOn << ".csv";
    fout.open (pathss.str().c_str());
    if (!fout.is_open()) {
        cerr << "Error opening " << pathss.str() << endl;
        return 1;
    }
    for (unsigned int i = 0; i < generations.size(); ++i) {
        fout << generations[i] << endl;
    }
    fout.close();

#ifdef RECORD_ALL_FITNESS
    // Open file
    stringstream pathss2;
    pathss2 << "./data/drift_withf_";
    pathss2 << "a" << (unsigned int)target_ant << "_p" << (unsigned int)target_pos << "_";
    pathss2 << FF_NAME << "_" << N_Generations <<  "_fitness_" << pOn << ".csv";
    fout.open (pathss2.str().c_str());
    if (!fout.is_open()) {
        cerr << "Error opening " << pathss2.str() << endl;
        return 1;
    }
    for (unsigned int i = 0; i < netinfo.size(); ++i) {
        if (!netinfo[i].empty()) {
            // Now the actual data.
            for (unsigned int j = 0; j < netinfo[i].size(); ++j) {
                // New genome:
                fout << static_cast<int>(netinfo[i][j].generation) << "," << netinfo[i][j].fitness;
                fout << "," << genome_id(netinfo[i][j].ab.genome);
                fout << "," << netinfo[i][j].ab.getNumBasins();
                fout << "," << netinfo[i][j].ab.meanAttractorLength();
                fout << "," << netinfo[i][j].ab.maxAttractorLength();
                fout << "," << netinfo[i][j].numChangedTransitions;
                fout << "," << netinfo[i][j].deltaF;
                fout << endl;
            }
        }
    }
    fout.close();
#endif

    return 0;
}
