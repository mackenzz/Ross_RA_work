#ifndef GUARD_environment_h
#define GUARD_environment_h

#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <map>

// #define SYNSET1
// #define SYNSET1B
// #define SYNSET2
#define SYNERGY

using namespace std;

extern uniform_real_distribution<double> *distribution;
extern mt19937_64 *generator;

typedef std::vector<int> Form;

inline double U() {
  return (*distribution)(*generator);
}

class Environment {
private:
  double fitness1(const Form &form, int i) const;
  double fitness1n(const Form &form, int i) const;

public:
  // the interaction matrix
  vector<vector<int> > interStruct;
  // For each row in interStruct, use an unordered_map to store key-value pair,
  // where key is a string of length (K+1), and value is its fitness value.
  // Note: K is different for each row
  vector<vector<double> > comb2fit;
  int N; // N of NK model
  int R; // number of relateness

  Environment(const string &inputFile, int inputN);

  void printNKMatrix(); // for debugging purpose.
  void createRandomNKMatrix(int K);

  //! Construct the landscape (w. synergy)
  void construct();

  double calcFitness(const Form &form, int start, int end) const;

  double calcSynergy(const Form &form) const;
};

extern long N, K, R;
extern double Alpha, Beta, Sim, Delta;

#endif
