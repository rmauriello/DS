Trying out some recommenders with Mahout and Hadoop.
=======

Installation is straightforward on Mac and Ubuntu but configuration is tricky.

Got a test example of collaborative filtering working on the Mac with current Hadoop (1.2.1) and Mahout (0.8).  Also watch my attempts at Java.

1) lensmovielens-1M.recommendations: Mahout's recommendations using the Movielens 1 million dataset and collaborative filtering

Fairly default parameters as this is the second example I got running. 
90/10 training/probe split; 10 iterations; 20 features. 

Uses the ALS-WR algorithm. Don't know anything about it and have to read the Zhou et al paper. However, it sounds like an SVD approach where the user - movie matrix (assuming rows are movie ratings for each user) are approximated by U.transpose and M. The iteration is as follows:
- initialize M using average of known ratings and then perturb balance with noise so everything has a value; sounds like sparse to dense matrix 
- hold M constant, solve for U
- hold U constant, solve for M
- stop when tolerance is met


2) movies.dat - names of movies. Yes I could write a script to label the recommendations but searching if there's a way to do it in Mahout

