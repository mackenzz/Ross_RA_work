#include <algorithm>
#include <assert.h>
#include <iostream>
#include <fstream>
#include <random>
#include <set>
#include <unordered_map>

#include "environment.h"

using namespace std;

uniform_real_distribution<double> *distribution;
mt19937_64 *generator;

long N, K, R;
double Alpha, Beta, Sim, Delta;

Environment::Environment(const string &inputFile, int inputN) : N(inputN) {
  // If inputFile is an empty string, it means we will construct it later using
  // randomized NK matrix.
  if (inputFile.empty()) {
    return;
  }
  // Check if input file exists
  ifstream data(inputFile);
  if (!data) {
    cout << "No such input file " << endl;
    exit(0);
  }

  int bit;
  for (int i = 0; i < N; i++) {
    vector<int> toPush;
    for (int j = 0; j < N; j++) {
      if (data >> bit) {
        if (bit == 1) toPush.push_back(j);
      } else {
        cout << "Error in reading inputFile" << endl;
        exit(0);
      }
    }
    assert(!toPush.empty());
    interStruct.push_back(toPush);
  }
  // printNKMatrix(); // for debugging
}

void Environment::printNKMatrix() {
  for (const auto &line : interStruct) {
    vector<int> output(N, 0);
    for (const int i : line) {
      output[i] = 1;
    }
    for (const int i : output) {
      cout << i << " ";
    }
    cout << endl;
  }
  cout << endl;
}

// Create a symmetric NK matrix.
void Environment::createRandomNKMatrix(int K) {
  // Clear interStruct before populating.
  interStruct.clear();

  set<int> ids;
  // create the first N/2 attibutes K interaction terms.
  for (int i = 0; i < N / 2; i++) {
    ids.insert(i);
    int count = 0;
    while (count != K) {
      double index = N / 2 * U();
      int pickedIdx = min(int(index), N / 2 - 1); // edge check
      if (ids.find(pickedIdx) == ids.end()) {
        ids.insert(pickedIdx);
        count++;
      }
    }
    vector<int> output(ids.begin(), ids.end());
    interStruct.push_back(output);
    ids.clear();
  }
  // Due to symmetry, the remaining N/2 attributes will have K interaction terms
  // which could be derived from the first N/2 attributes.
  for (int i = 0; i < N / 2; i++) {
    vector<int> output(interStruct[i].begin(), interStruct[i].end());
    for (int &ele : output) {
      ele += N / 2;
    }
    interStruct.push_back(output);
  }
  // printNKMatrix(); // for debugging
}

// Build the unordered_map "comb2fit" by mapping each combination attribute (with a size of K) to
// a random fitness value. Contribution of each attribute depends on K attribf c wutes (self included),
// i.e there are 2^K combinations of attributes which will be mapped to 2^K fitness values
void Environment::construct() {
  // Clear comb2fit before populating.
  comb2fit.clear();

  for (int i = 0; i < N; i++) {
    int K = interStruct[i].size();
    long numOfComb = 1 << K;
    comb2fit.emplace_back(numOfComb, 0.0);
    for (int j = 0; j < numOfComb; j++)
      comb2fit.back()[j] = U();
  }
}

double alpha(long i) {
  double alpha = 0;
#ifdef SYNSET1B
  alpha = (i - N/2) * 2.0 / N;
#else
  if (i >= N / 2 && i < N / 2 + R)
#ifdef SYNSET2
    alpha = 1;
#else
    alpha = Alpha < 0 ? (i * 2.0 / N - 1) : Alpha;
#endif
#endif
  return alpha;
}

double Environment::fitness1(const Form &form, int i) const {
  double fit = 0;
  long comb = 0;
  for (const int id : interStruct[i])
    comb = (comb << 1) + form[id]; // Extract the interacting attributes.
  if (i >= N / 2) {
    double a = alpha(i);
    fit += Sim * ((1 - a) * comb2fit[i][comb] + a * comb2fit[i - N / 2][comb]) + (1 - Sim) * comb2fit[i][comb];
  } else
    fit += comb2fit[i][comb];
  return fit;
}

double Environment::fitness1n(const Form &form, int i) const {
  double fit = 0;
  long comb = 0;
  for (const int id : interStruct[i])
    comb = (comb << 1) + form[id]; // Extract the interacting attributes.
  f;
  return fit;
}

// Return the fitness value of the substring, within [start,end), of a string,
// e.g. start = 0, end = N means the to calculate the fitness of entire string.
double Environment::calcFitness(const Form &form, int start, int end) const {
  double fit = 0;
  for (int i = start; i < end; i++)
    fit += fitness1(form, i);
  return fit / (end - start); // average
}

#define SYNEQ0 ((1.0 - std::pow(i * 2.0 / N - 1.0, Beta)) * fitness1(form, i))
#define SYNEQ1 ((1.0 - alpha(i)) * fitness1(form, i))
#define SYNEQ2 (Sim * (1.0 - alpha(i)) * fitness1(form, i))
#define SYNEQ3 (fitness1(form, i))
#define SYNEQ4 (Sim * fitness1n(form, i))

#define SYNEQ SYNEQ2

double Environment::calcSynergy(const Form &form) const {
  double syn = 0;
#ifdef SYNERGY
  for (int i = N / 2; i < N; i++)
    if (form[i] == form[i - N / 2]) {
      syn += Delta * (SYNEQ);
    }
#endif
  return syn / N; // average
}
