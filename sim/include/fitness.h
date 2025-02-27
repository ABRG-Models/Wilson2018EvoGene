/*
 * This is a header used to selectively include one of the fitness
 * functions.
 */

#ifndef __FITNESS_H__
#define __FITNESS_H__

#include "endpoint.h"

// The default is fitness1.h; pass -DUSE_FITNESS_0 in compiler command
// line to select fitness0.h.
#if defined USE_FITNESS_0
// The fitness function created by Stuart Wilson, based on distance from target to attractor
# include "fitness0.h"

#elif defined USE_FITNESS_1
// The fitness function created by Dan Whiteley based on Hamming distance from target
# include "fitness1.h"

#elif defined USE_FITNESS_2
// Another fitness function, explored by Seb James, similar to ff0
# include "fitness2.h"

#elif defined USE_FITNESS_3
// Another fitness function, explored by Seb, again similar to ff0
# include "fitness3.h"

#elif defined USE_FITNESS_4
// The most successful fitness function, considering the limit cycle
// as defining "proportional expression" of the target proteins.
# include "fitness4.h"

#elif defined USE_FITNESS_5
// Like FF4, considers the limit cycle as defining "proportional
// expression" of the target proteins, but takes a mean of the time
// each gene spends in the correct state, rather than computing a
// multiplicative score like FF4.
# include "fitness5.h"

#elif defined USE_FITNESS_6
// Like FF4 (multiplicative between the genes), but takes the mean of
// the anterior and posterior scores.
# include "fitness6.h"

#elif defined USE_FITNESS_7
// Like FF5 (additive between the genes), but multiplies the anterior
// and posterior scores.
# include "fitness7.h"

#elif defined USE_FITNESS_8
// Seb's fitness function which pays attention to whether the gradient
// from ant->pos is in the correct direction.
# include "fitness8.h"

#else
# error "When you include fitness.h you have to make sure to define USE_FITNESS_N"
#endif

#endif // __FITNESS_FUNCTION__
