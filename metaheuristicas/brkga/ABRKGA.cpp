using namespace std;

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <vector>
#include <cstring>
#include <string.h>
#include <omp.h>
#include <algorithm>
#include <sys/time.h>

#include "ABRKGA.h"


//------DEFINITION OF CONSTANTS, TYPES AND VARIABLES--------

// Run
char instance[50];                          // name of instance

//A-BRKGA
int n;                                      // size of cromossoms
int p;          	                        // size of population
int maxGenerations;                         // max number of generations
double pe;              	                // fraction of population to be the elite-set
double pm;          	                    // fraction of population to be replaced by mutants
double rhoe;             	                // probability that offspring inherit an allele from elite parent
double alfa;                                // threashold of restrict chromossoms list
double beta;                                // perturbation intensity
double sigma;                               // pearson correlation factor
double teta;								// percentage of generations in an epoch
double gama;								// cooling rate of the population

vector <TSol> Pop;                      	// current population
vector <TSol> PopInter;               		// intermediary population

TSol bestSolution;                          // best solution found in the A-BRKGA

// computational time (windows systems)
clock_t CPUbegin,							// initial run time
        CPUbest,							// time to find the best solution in a run
        CPUend;								// end run time

// computational time (unix systems)
struct timeval Tstart, Tend, Tbest;         

//Problem specific data
vector <vector <double> > dist;				// matrix with Euclidean distance

struct TNode								// struct with node informations
{
	int id;
	double x;
	double y;
};

vector <TNode> node;						// vector of TSP nodes


/************************************************************************************
								FUNCTIONS AREA
*************************************************************************************/
int main()
{
    // file with test instances
	FILE *arqProblems;
    arqProblems = fopen ("arqProblems.txt", "r"); 

    if (arqProblems == NULL)
    {
        printf("\nERROR: File arqProblems.txt not found\n");
        getchar();
        exit(1);
    }

    // best solution that is saved in out file
    TSol sBest;

	// run the A-BRKGA for all test instances
	while (!feof(arqProblems))
	{
		// read the name of instances, debug mode, local search module, method, maximum time, maximum number of runs, maximum number of threads
		char nameTable[100];
		fscanf(arqProblems,"%s %d %d %d %d %d", nameTable, &debug, &ls, &MAXTIME, &MAXRUNS, &MAX_THREADS);

		//read the informations of the instance
        ReadData(nameTable);

        double foBest = INFINITY,
               foAverage = 0;

        float timeBest = 0,
              timeTotal = 0;

        // best solutions found in MAXRUNS
        sBest.fo = INFINITY;

		// run ABRKGA MaxRuns for each instance
        printf("\n\nInstance: %s \nRun: ", instance);
        for (int j=0; j<MAXRUNS; j++)
        {
            // fixed seed
            srand(j+1);

            printf("%d ", j+1);
            CPUbegin = CPUend = CPUbest = clock();
            gettimeofday(&Tstart, NULL);
            gettimeofday(&Tend, NULL);
            gettimeofday(&Tbest, NULL);

            // best solution found in this run
            bestSolution.fo = INFINITY;

            // execute the evolutionary method
            A_BRKGA();

            CPUend = clock();
            gettimeofday(&Tend, NULL);

            if (bestSolution.fo < sBest.fo)
                sBest = bestSolution;

            // calculate average results
            if (bestSolution.fo < foBest)
                foBest = bestSolution.fo;
            foAverage += bestSolution.fo;
            //timeBest += (float)(CPUbest - CPUbegin)/CLOCKS_PER_SEC;
            //timeTotal += (float)(CPUend - CPUbegin)/CLOCKS_PER_SEC;
            timeBest += ((Tbest.tv_sec  - Tstart.tv_sec) * 1000000u + Tbest.tv_usec - Tstart.tv_usec) / 1.e6;
            timeTotal += ((Tend.tv_sec  - Tstart.tv_sec) * 1000000u + Tend.tv_usec - Tstart.tv_usec) / 1.e6; 
        }

        // create a .xls file with average results
        foAverage = foAverage / MAXRUNS;
        timeBest = timeBest / MAXRUNS;
        timeTotal = timeTotal / MAXRUNS;

        if (!debug)
        {
        	   WriteSolution(sBest, timeBest, timeTotal);
        	   WriteResults(foBest, foAverage, timeBest, timeTotal);
        }
        else
        {
            WriteSolutionScreen(sBest, timeBest, timeTotal);
        }

        // free memory of problem variables
        dist.clear();
        node.clear();
    }

    fclose(arqProblems);
    return 0;
}

/************************************************************************************
			                  PROBLEM SPECIFIC FUNCTIONS
*************************************************************************************/

TSol Decoder(TSol s)
{
    // save the random-key sequence of current solution 
    TSol temp = s;

    // create a initial solution of the problem
    s.fo = 0;
    for (int i=0; i<n; i++)
        s.vec[i].sol = i;

    // sort random-key vector 
    sort(s.vec.begin(), s.vec.end()-2, sortByRk);

    // calculate objective function
    s.fo = CalculateFO(s);

    // return initial random-key sequence
    for (int i=0; i<n; i++)
        s.vec[i].rk = temp.vec[i].rk;

    return s;
}

double CalculateFO(TSol s)
{
	s.fo = 0;
	for (int i=0; i<n; i++)
	{
		s.fo += dist[s.vec[i%n].sol][s.vec[(i+1)%n].sol];
	}

	// save the best solution found in this run
    if (s.fo < bestSolution.fo)
    {
        bestSolution = s;
        CPUbest = clock();
        gettimeofday(&Tbest, NULL);
    }

	return s.fo;
}

TSol LocalSearch(TSol s)
{
	/* 2opt MOVEMENT
	 *
	 * BEFORE
	 * 0 1 2 3 4 5 6 7 8 9 10 11 12 13 13 15
	 *
	 * AFTER move with begin=5 and end=10:
	 * 0 1 2 3 4 10 9 8 7 6 5 11 12 13 14 15
	 */

	int melhorou = 1;
	int numTentativas = 0;
	while (melhorou)
	{
		melhorou = 0;
		numTentativas++;
		int t = 0,
			i = 0,
			j = 0,
			Mi1= 0,
			Mj = 0;

		int foOpt = 0;

		t = n; // use a circular list
		if (t > 4)
		{
			for (i=0; i < t; i++)
			{
			  j = i + 2;
			  while (((j+1)%t) != i)
			  {
			    int vi  = s.vec[i].sol;
			    int vi1 = s.vec[(i+1)%t].sol;
			    int vj  = s.vec[j%t].sol;
			    int vj1 = s.vec[(j+1)%t].sol;

			    foOpt = - dist[vi][vi1]
			            - dist[vj][vj1]
			            + dist[vi][vj]
			            + dist[vi1][vj1];

			    if (foOpt < 0)
			    {
			    	// first improvement strategy
			    	melhorou = 1;
					Mi1 = (i+1)%t;
					Mj  = j%t;

					int inicio = Mi1,
					  fim = Mj;

					int tam, p1, p2, aux;

					if(inicio > fim)
						tam = t - inicio + fim + 1;
					else
						tam = fim - inicio + 1;

					p1=inicio;
					p2=fim;

					for(int k=0; k < tam/2; k++)
					{
						//printf("\n %d %d %d %d  =>  %d", Mi1, Mj, p1%t, p2%t, t);
						aux = s.vec[p1%t].sol;
						s.vec[p1%t].sol = s.vec[p2%t].sol;
						s.vec[p2%t].sol = aux;

						p1 = (p1==t-1)?0:p1+1;
						p2 = (p2 == 0)?t-1:p2-1;
					}

					s.fo = s.fo + foOpt;
			    }
			    j++;
			  }//while
			}//for
		}//if t > 4

		if (melhorou)
		{
			// shift(1,0) MOVEMENT
			TSol sViz = s;

			for (int i=0; i<n-1; i++)
			{
				for (int j=i+1; j<n; j++)
				{

					TVecSol aux;

					aux.sol = sViz.vec[i%t].sol;
					aux.rk = sViz.vec[i%t].rk;

					sViz.vec.insert(sViz.vec.begin()+(j%t), aux);
					sViz.vec.erase(sViz.vec.begin()+(i%t));

					sViz.fo = CalculateFO(sViz);

					if (sViz.fo < s.fo)
					{
						s = sViz;
						melhorou = 1;
					}
					else
						sViz = s;

				}
			}
		}
	}

	// save the best solution found in this run
    if (s.fo < bestSolution.fo)
    {
        bestSolution = s;
        CPUbest = clock();
    }

 	return s;
}

void ReadData(char nameTable[])
{
    char name[200] = "";
    strcat(name,nameTable);

    FILE *arq;
    arq = fopen(name,"r");

    if (arq == NULL)
    {
        printf("\nERROR: File (%s) not found!\n",name);
        getchar();
        exit(1);
    }

    // => name of instance
    strcpy(instance,nameTable);

    // => read data

    // read instance head
    char temp[100];
    fgets(temp, sizeof(temp), arq);
    fgets(temp, sizeof(temp), arq);
    fgets(temp, sizeof(temp), arq);
    fgets(temp, sizeof(temp), arq);
    fgets(temp, sizeof(temp), arq);
    fgets(temp, sizeof(temp), arq);

    // read node informations
    n = 0;
    node.clear();
    TNode nodeTemp;

    while (!feof(arq))
    {
    	fscanf(arq, "%d %lf %lf", &nodeTemp.id, &nodeTemp.x, &nodeTemp.y);
    	node.push_back(nodeTemp);

    	n++;
    }

    fclose(arq);

    // calculate the euclidean distance
    dist.clear();
    dist.resize(n, vector<double>(n));

    for (int i=0; i<n; i++)
    {
    	for (int j=i; j<n; j++)
    	{

    		dist[i][j] = dist[j][i] = (floor (sqrt( (node[j].x - node[i].x) * (node[j].x - node[i].x) +
    										        (node[j].y - node[i].y) * (node[j].y - node[i].y) ) + 0.5 ) )/1.0;
    	}
    }
}


/************************************************************************************
			                  GENERAL FUNCTIONS
*************************************************************************************/

void A_BRKGA()
{
    // max and min population size
    int pMax = 1000;
    int pMin = 100;

    // cooling rate [0.999, 0.998, 0.997]
    gama = 0.999;

    // define epoch interval
    teta = 0.01;

    // initial population size
    p = pMax;

    // initialize populations
    Pop.clear();
    PopInter.clear();

    Pop.resize(p);
    PopInter.resize(p);


    // Stop criterium
    maxGenerations = (pow(gama, (log(pMin)/log(gama) - pMax)));

    // top population size
    int Tpe;

    // top max population size
    int TpeMax;

    // number of chromossoms in top with no similarity
    int numTop;

    // mutation population size
    int Tpm;

    // number of local search applied in this generation
    int numLS = 0;

    // Create the initial chromossoms with random keys
    #pragma omp parallel for num_threads(MAX_THREADS)
    for (int i=0; i<p; i++)
    {
        TSol ind = CreateInitialSolutions();
        ind = Decoder(ind);
        Pop[p-i-1] = PopInter[p-i-1] = ind;
    }

    int numGenerations = 0;
    double mediaPop;
    float currentTime = 0;

    // run the evolutionary process until stop criterion
    while (numGenerations < maxGenerations)
    {
    	// number of generations
        numGenerations++;

        // sort population in increase order of fitness
        sort(Pop.begin(), Pop.end(), sortByFitness);

        // ** update parameters (p, pe and pm) **

        // population size: cooling annealing
        p = (int)(p * gama);
        Pop.resize(p);
        PopInter.resize(p);

        // increase max Elite
        pe = 0.10 + ((double)numGenerations/maxGenerations) * (0.25 - 0.10);
        TpeMax = (int)(p * pe);

        // candidate restrictive list of elite chromossoms
        alfa = 0.10 + (1 - (double)numGenerations/maxGenerations) * (0.30 - 0.10);
        double treashold = Pop[0].fo + alfa*(Pop[p-1].fo - Pop[0].fo);
        Tpe = 0;
        while (Pop[Tpe].fo <= treashold && Tpe < TpeMax)
            Tpe++;

        // decrease Mutations
        pm = 0.05 + (1-(double)numGenerations/maxGenerations) * (0.20 - 0.05);
        Tpm = (int)(p * pm);

        // ** end update **

        // We now will set every chromosome of 'current', iterating with 'i':
        int i = 0;	// Iterate chromosome by chromosome

        // number of chromossoms in Top with no similarity
        numTop = 0;

         // calculate media fitness population in the current generation
         mediaPop = 0;

        // The 'pe' best chromosomes (no similar) are maintained, so we just copy these into 'current':
        while(i < Tpe)
        {
            // initially, the chromossom i is not similar with the other chromossoms
            Pop[i].similar = 0;

            // copy the best chromossom for next generation
            if (i == 0)
            {
                PopInter[i] = Pop[i];
                numTop++;
                mediaPop += PopInter[i].fo;
            }

            // for ohter chromossom, calculate the similarity
            else
            {
                // calculate the similarity beetwen chromossoms i and k (chromossoms in top better than i)
                for (int k=0; k<i; k++)
                { 
                    // chromossoms i and k are similar if they have the same fitness
                    if (Pop[i].fo == Pop[k].fo)
                    {
                        Pop[i].similar = 1;
                        break;
                    }
                }

                // copy chromossom i to the next generation if it is not simliar with other chromossoms
                if (Pop[i].similar == 0)
                {
                    PopInter[i] = Pop[i];
                    numTop++;
                    mediaPop += PopInter[i].fo;
                }

                // perturbation the top solution and copy to the next generation
                else
                {
                    PopInter[i] = Pop[i];

                    // perturbation intesity
                    beta = 0.10 + (Pop[i].vec[n+1].rk) * (0.20 - 0.10);

                    // apply perturbation method in a similar solution
                    PopInter[i] = Perturbation(PopInter[i], beta);

                    // calculate fitness
                    PopInter[i] = Decoder(PopInter[i]);
                    PopInter[i].flag = 0;  // set the flag of local search as zero
                    mediaPop += PopInter[i].fo;
                }
            }
        	++i;
        }

        // We'll mate 'p - pe - pm' pairs; initially, i = pe, so we need to iterate until i < p - pm:
        while(i < p - Tpm)
        {
        	// parametric uniform crossover
        	PopInter[i] = ParametricUniformCrossover(Tpe);

            ++i;
        }

        // We'll introduce 'pm' mutants:
        while(i < p)
        {
            PopInter[i] = CreateInitialSolutions();
            ++i;
        }

        // Calculate fitness
        #pragma omp parallel for num_threads(MAX_THREADS)
        for (i=Tpe; i<p; i++)
        {
            PopInter[i] = Decoder(PopInter[i]);
            mediaPop += PopInter[i].fo;
        }
        mediaPop = mediaPop/p;

        // Update the current population
        Pop = PopInter;


        // ***** Local search in communities ***
        if (ls)
        {
			numLS = 0;

        	// update epoch
        	int interval = (int)maxGenerations*0.10;
        	if ((numGenerations+1)%interval == 0)
		    	teta += 0.005;

	        int epoch = (int)maxGenerations*teta;

	        if (numGenerations%epoch == 0)
	        {
	            // Find commuties in Top chromossoms
	            sigma = 0.30 + ((double)numGenerations/maxGenerations) * (0.70 - 0.30);
	            IC(0, Tpe, sigma);

	            vector <int> promisingSol; 
                promisingSol.clear();

	            for (i=0; i < Tpe; i++)
	            {
	                if (Pop[i].promising == 1)
	                {
	                	promisingSol.push_back(i);
	                    numLS++;
	                }
	            }

	            #pragma omp parallel for num_threads(MAX_THREADS)
                for (unsigned int i=0; i < promisingSol.size(); i++)
                {
                    // in this case, local search not influence the evolutionary process
                    LocalSearch(Pop[promisingSol[i]]);
                    Pop[promisingSol[i]].flag = 1;
                }

                promisingSol.clear();
	        }
	    }

        // ******** end local search ******

        if (debug)
            printf("\nGeneration: %3d [%3d - %3d(%.2lf) (%3d : %3d) - %3d(%.2lf)] \t %.2lf \t %.2lf \t %.2lf(%.0lf) ",
                        numGenerations, p, Tpe, pe, numTop, numLS, Tpm, pm, mediaPop, bestSolution.fo, teta, maxGenerations*teta);

		// restart population
        if (p < pMin)
        {
        	int currentP = p;

            // initial size population
            p = pMax;

            // create new chromossoms
            for (int k = 0; k < p-currentP; k++)
            {
                TSol ind = CreateInitialSolutions();
                Pop.push_back(Decoder(ind));
                PopInter.push_back(Decoder(ind));
            }
        }

        // terminate the evolutionary process in MAXTIME
        CPUend = clock();
        currentTime = (float)(CPUend - CPUbegin)/CLOCKS_PER_SEC;
        if (currentTime >= MAXTIME)
            break;
    }

    // free memory
    Pop.clear();
	PopInter.clear();
}

TSol CreateInitialSolutions()
{
	TSol s;
	TVecSol aux;

    s.vec.clear();

	// create a random-key for each allelo
	for (int j=0; j<n; j++)
	{
		aux.rk  = randomico(0,1);
		aux.sol = j;

        s.vec.push_back(aux);
	}

    // create an allelo for rhoe parameter
    aux.rk = randomico(0,1);
	aux.sol = -1;
	s.vec.push_back(aux);

    // create an allelo for beta parameter (perturbation)
    aux.rk = randomico(0,1);
	aux.sol = -1;
    s.vec.push_back(aux);

    // flag to control the local search memory
    s.flag = 0;

	return s;
}

TSol Perturbation(TSol s, double beta)
{
	for (int k=0; k<n; k++)
    {
        if (randomico(0,1) < beta)
        {
            // choose a random position
            int pos = irandomico(0, n-1);

            // swap genes k e pos
            double temp = s.vec[k].rk;
            s.vec[k].rk = s.vec[pos].rk;
            s.vec[pos].rk = temp;
        }
    }
    return s;
}

TSol ParametricUniformCrossover(int Tpe)
{	
	TSol s;

	// create a new offspring
	s.vec.resize(n+2);

    // Select an elite parent:
    int eliteParent = irandomico(0,Tpe - 1);

    // Select a non-elite parent:
    int noneliteParent = Tpe + irandomico(0, p - Tpe - 1);

    // Define self-adaptative rhoe
    rhoe = 0.65 + (Pop[noneliteParent].vec[n].rk) * (0.80 - 0.65);

    // Mate:  // including rhoe and perturbation
    for(int j = 0; j < n+2; j++)
    {
        //copy alelos of top chromossom of the new generation
        if (randomico(0,1) < rhoe)
           s.vec[j].rk = Pop[eliteParent].vec[j].rk;
        else
           s.vec[j].rk = Pop[noneliteParent].vec[j].rk;

        if (j < n)
        	s.vec[j].sol = j;
        else
        	s.vec[j].sol = -1;
    }

    // set the flag of local search as zero
    s.flag = 0;

    return s;
}

double PearsonCorrelation(vector <TVecSol> X, vector<TVecSol> Y)
{
    double correlation = 0;
    double sumXY = 0;
    double sumX2 = 0;
    double sumY2 = 0;
    double sumX = 0;
    double sumY = 0;

    for(int j=0; j<n; j++)
    {
        sumX += X[j].rk;
        sumX2 += X[j].rk * X[j].rk;
        sumXY += X[j].rk * Y[j].rk;
        sumY += Y[j].rk;
        sumY2 += Y[j].rk * Y[j].rk;
    }

    //Pearson
    correlation= ((n*sumXY) - (sumX*sumY) ) / (sqrt( (n*sumX2 - sumX*sumX) * (n*sumY2 - sumY*sumY) ));
    return correlation;
}


void IC(int tInitial, int tEnd, double sigma)
{
    vector <vector <int> >  matArestas;
    int tam = tEnd - tInitial;

    // create similar matrix
    matArestas.clear();
    matArestas.resize(tam, vector<int>(tam));

    for (int i=tInitial; i<tEnd; i++)
    {
        for (int j=i; j<tEnd; j++)
        {
            if (i == j)
                matArestas[i][j] = 0;
            else
            {
                if (Pop[i].fo == Pop[j].fo)
                    matArestas[i][j] = matArestas[j][i] = 1;

                else
                {
                    if(PearsonCorrelation(Pop[i].vec, Pop[j].vec) > sigma)
                        matArestas[i][j] = matArestas[j][i] = 1;
                    else
                        matArestas[i][j] = matArestas[j][i] = 0;
                }
            }
        }
    }

    // apply clustering method
    LP(tInitial, tEnd, matArestas);
    PromisingLP(tInitial, tEnd);
}

void LP(int tInitial, int tEnd, vector< vector <int> > matArestas)
{
    // save the number of times a label appears in the neighbors of node i
    vector <int> v;
    v.resize(tEnd-tInitial);

    int escolhido = -1;
    vector <int> desempate;

    // initialize each node with its own label
    for(int i=tInitial; i<tEnd; i++)
        Pop[i].label = i;

    // search each graph node
    for(int i=tInitial; i<tEnd; i++)
    {
        // initialize v with 0
        for(unsigned int j=0; j<v.size(); j++)
            v[j]=0;

        // detects the most common id in the neighbors of node i
        for(int k=tInitial; k<tEnd; k++)
        {
            if(matArestas[i][k] == 1)
                v[Pop[k].label]++;
        }

        // number of times the most common label appears
        int maior=-1;       
        for(int k=tInitial; k<tEnd; k++)
        {
            if(v[k] > maior)
                maior = v[k];
        }

        // random tiebreaker
        desempate.clear();
        for(unsigned int k=0; k<v.size(); k++)
        {
            if(v[k] == maior)
                desempate.push_back(k);
        }

        // define new label of node i
        escolhido = irandomico(0, desempate.size()-1);
        Pop[i].label = desempate[escolhido];
    }
}

void PromisingLP(int tInitial, int tEnd)
{
    vector <int> grupos;
    int tamanhoGrupos = 0;

    // initialize promisings solutions
    for(int i=tInitial; i<tEnd; i++)
        Pop[i].promising = 0;

    // save labels defined by LP in groups
    for(int i=tInitial; i<tEnd; i++)
    {
        int achei = 0;
        for(unsigned int j=0; j<grupos.size(); j++)
        {
            if(Pop[i].label == grupos[j])
                achei=1;
        }
        if(achei == 0)
        {
            tamanhoGrupos++;
            grupos.push_back(Pop[i].label);
        }
    }

    // find the best solution in the group (with flag = 0)
    for(unsigned int j=0; j<grupos.size(); j++)
    {
        double menorFO = INFINITY;
        int localMenor = -1;
        int local = -1;
        for(int i=tInitial; i<tEnd; i++)
        {
            if(Pop[i].label == grupos[j])
            {
                // find the best solution of the group
                if (local == -1)
                    local = i;

                if(Pop[i].fo < menorFO && Pop[i].flag == 0) // we not apply local search in this solution yet
                {
                    menorFO = Pop[i].fo;
                    localMenor = i;
                }
            }
        }

        if (localMenor == -1)
            localMenor = local;

        if(Pop[localMenor].label != -1)
            Pop[localMenor].promising = 1;
    }
}



/************************************************************************************
									IO Functions
*************************************************************************************/

void WriteSolutionScreen(TSol s, float timeBest, float timeTotal)
{
	printf("\n\n\n Instance: %s \nsol: ", instance);
	for (int i=0; i<n; i++)
		printf("%d ", s.vec[i].sol);
	printf("\nfo: %.5lf",s.fo);
	printf("\nTotal time: %.3f",timeTotal);
	printf("\nBest time: %.3f\n\n",timeBest);
}

void WriteSolution(TSol s, float timeBest, float timeTotal)
{
	FILE *arquivo;
    arquivo = fopen("Solutions.txt","a");

	if (!arquivo)
	{
		printf("\n\nFile not found Solutions.txt!!!");
		getchar();
		exit(1);
	}

    fprintf(arquivo,"\n\nInstance: %s", instance);
	fprintf(arquivo,"\nSol: ");
	for (int i=0; i<n; i++)
		fprintf(arquivo,"%d ", s.vec[i].sol);
	fprintf(arquivo,"\nFO: %.5lf", s.fo);
  	fprintf(arquivo,"\nBest time: %.3f",timeBest);
	fprintf(arquivo,"\nTotal time:%.3f \n",timeTotal);

	fclose(arquivo);
}

void WriteResults(double fo, double foAverage, float timeBest, float timeTotal)
{
	FILE *arquivo;
    arquivo = fopen("Results.xls","a");

	if (!arquivo)
	{
		printf("\n\nFile not found Results.xls!!!");
		getchar();
		exit(1);
	}

	fprintf(arquivo,"\n%s", instance);
	fprintf(arquivo,"\t%lf", fo);
	fprintf(arquivo,"\t%lf", foAverage);
	fprintf(arquivo,"\t%.3f", timeBest);
	fprintf(arquivo,"\t%.3f", timeTotal);

	fclose(arquivo);
}

double randomico(double min, double max)
{
	
	return ((double)(rand()%10000)/10000.0)*(max-min)+min;
}

int irandomico(int min, int max)
{

	return (int)randomico(0,max-min+1.0) + min;
}
