#define VERSION "20190411"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <limits.h>
#include <signal.h>
#include <setjmp.h>

#define IMAGEFILE "ls9.image"  // specifies the heap image file to load at startup
#define IMAGESRC  "ls9.ls9"    // source file to load if a default image is not available

#define NNODES 	262144        // number of nodes (smallest amount of storage allocatable by the interpreter)
#define NVCELLS 262144        // number of vector cells (a slot in a vector)

#define NPORTS 20             // max number of IO ports at any one time
#define TOKLEN 80             // max size of all tokens

#define CHUNKSIZE 1024        // size by which all objects will grow. TODO: experiment with this value!
#define MXMAX     2000        // max recursion depth to macro expander
#define NTRACE    10          // number of refs to free vars to be printed in case of errors
#define PRDEPTH   1024        // max depth of a structure printer can print

