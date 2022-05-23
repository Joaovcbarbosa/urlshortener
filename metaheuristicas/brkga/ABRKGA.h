#include <vector>

int debug = 1;               // 0 - run mode      			 1 - debug mode
int ls = 1;  				 // 0 - without local search     1 - with local search

int MAXTIME = 1000;                         // maximum runtime
int MAXRUNS =  1;                           // maximum number of runs of the method
unsigned MAX_THREADS = 1;            		// number of threads


/***********************************************************************************
 Struct: TVecSol
 Description: struct to represent the two vector solutions (rk and problem)
************************************************************************************/
struct TVecSol
{
	int sol;
	double rk;

};

// Sort TSol by objective function
bool sortByRk(const TVecSol &lhs, const TVecSol &rhs) { return lhs.rk < rhs.rk; }


/***********************************************************************************
 Struct: TSol
 Description: struct to represent a solution problem
************************************************************************************/
struct TSol
{
    vector <TVecSol> vec;      // solution of the problem and random key
    double fo;                 // objetive function value
    int label;                 // defines a community solution with a number
    int similar;               // indicates if a solution is similar to other (0 no, 1 yes)
    int flag;                  // indicates if a local search has already been performed on this solution (0 no, 1 yes)
    int promising;             // indicates if a solution is promising to apply local search
};

// Sort TSol by objective function
bool sortByFitness(const TSol &lhs, const TSol &rhs) { return lhs.fo < rhs.fo; }


//************************** Problem Specific Functions *****************************


/************************************************************************************
 Method: Decoder()
 Description: Convert a random key solution in a real problem solution
*************************************************************************************/
TSol Decoder(TSol s);

/************************************************************************************
Method: CALCULATEFO
Description: Calculate the objective function of the problem
*************************************************************************************/
double CalculateFO(TSol s);

/************************************************************************************
 Method: LocalSearch()
 Description: Apply local search in a promising solution
*************************************************************************************/
TSol LocalSearch(TSol s);

/************************************************************************************
Method: READ DATA
Description: read data of test intances
*************************************************************************************/
void ReadData(char nomeTabela[]);


//****************************** General Functions **********************************

/************************************************************************************
 Method: ABRKGA()
 Description: Apply the method A-BRKGA to solve the problem
*************************************************************************************/
void A_BRKGA();

/************************************************************************************
 Method: CREATE INITIAL SOLUTIONS
 Description: create a initial chromossom with random keys
*************************************************************************************/
TSol CreateInitialSolutions();


/************************************************************************************
 Method: PERTURBATION
 Description: perturbation similar chromossom
*************************************************************************************/
TSol Perturbation(TSol s, double beta);

/************************************************************************************
 Method: PARAMETRICUNIFORMCROSSOVER
 Description: create a new offspring with parametric uniform crossover
*************************************************************************************/
TSol ParametricUniformCrossover(int Tpe);

/************************************************************************************
 Method: PEARSON CORRELATION
 Description: calculate the Pearson correlation coefficient between two chromossoms
*************************************************************************************/
double PearsonCorrelation(std::vector <TVecSol> s1, std::vector <TVecSol> s2);

/************************************************************************************
 Metodo: IC(TSol Pop)
 Description: apply clustering method to find promising solutions in the population
*************************************************************************************/
void IC(int tInitial, int tEnd, double sigma);

/************************************************************************************
 Method: LP
 Description: Apply Label Propagation to find communities in the population
*************************************************************************************/
void LP(int tInitial, int tEnd, std::vector< std::vector <int> > matArestas);

/************************************************************************************
 Method: PROMISINGLP
 Description: Find the promising solutions to represent the communities
*************************************************************************************/
void PromisingLP(int tInitial, int tEnd);



//********************************** IO Functions ***********************************


/************************************************************************************
Method: WRITE RESULTS
Description: write the results in .XLS file
*************************************************************************************/
void WriteResults(double fo, double foMedia, float tempoMelhor, float tempoTotal);

/************************************************************************************
Method: WRITE SOLUTION
Description: write the solution in .TXT file
*************************************************************************************/
void WriteSolution(TSol s, float timeBest, float timeTotal);

/************************************************************************************
Method: WRITE SOLUTION SCREEN
Funcao: write the solution in the screen
*************************************************************************************/
void WriteSolutionScreen(TSol s, float timeBest, float timeTotal);

/************************************************************************************
 Method: RANDOMICO
 Description: Generate a double random number between min and max
*************************************************************************************/
double randomico(double min, double max);

/************************************************************************************
 Method: IRANDOMICO
 Description: Generate a int random number between min and max
*************************************************************************************/
int irandomico(int min, int max);

