#ifndef FAB_CLOSEST_POINT
#define FAB_CLOSEST_POINT

#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <assert.h>
#include <time.h>

#include <sys/wait.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <pthread.h>

typedef struct
{
    int x;
    int y;
} point;

typedef struct
{
    point p;
    size_t xposition;
} PyElement;

typedef struct
{ //data structure representing the solution: pair of closest points and their distance
    point p1;
    point p2;
    float distance;
} points_distance;

typedef struct
{
    point* Px;
    PyElement* Py;
    size_t length;
    points_distance *result;
    size_t par_threshold;
} thread_arg;

struct pointlist {
    size_t num_points;
    point* P;
};

#define errExit(msg) do { \
    perror(msg); exit(EXIT_FAILURE); \
} while (0)

#define MIN(x, y) ((x < y) ? x : y)


// ==== AUXILIARY FUNCTIONS ====
float distance(point p1, point p2);
PyElement *get_candidates_from_different_halves(point reference, PyElement Py[], size_t length, size_t *candidates_length, float min_distance_upper_bound);
void sort_points(point P[], size_t length, PyElement Py[]);
points_distance closest_points_from_different_halves(PyElement P[], size_t length);
void populateLy(PyElement *Py, size_t Pylength, PyElement *Ly, size_t left_half_upper_bound);
void populateRy(PyElement *Py, size_t Pylength, PyElement *Ry, size_t right_half_lower_bound);
points_distance closest_points(point Px[], PyElement Py[], size_t length);
point* rand_point(int min_value, int max_value);
point *rand_points(size_t num_points);
void print_points_distance(points_distance p);
struct pointlist read_test_file(const char *filename);
double timeit(points_distance (*func)(point P[], size_t length, int num_processes), struct pointlist pd, int num_processes);


// =====  SOLUTIONS ====
//num_processes added to unify interface and simplify signature of testing methods
points_distance quadratic_solution(point P[], size_t length, int num_processes);

//num_processes added to unify interface and simplify signature of testing methods
points_distance nlogn_solution(point P[], size_t length, int num_processes);

//parallel versions of the nlogn solution
points_distance nlogn_solution_multiproc(point P[], size_t length, int num_processes);
points_distance nlogn_solution_multithread(point P[], size_t length, int num_processes);

#endif
