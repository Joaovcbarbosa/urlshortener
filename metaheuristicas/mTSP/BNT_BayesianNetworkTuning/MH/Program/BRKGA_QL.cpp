#include "BRKGA_QL.h"

/************************************************************************************
								MAIN FUNCTION AREA
*************************************************************************************/
int main(int argc, char *argv[ ])
{  
    // Exemplo com o formato do comando executado
    // ./runMH MH/Instances/FTSP/gr137_2.sftsp -P 377 -Pe 0.20 -Pm 0.25 -Rhoe 0.70

    char nameTable[100]; 

    // primeiro argumento - nome da instancia
    strncpy(nameTable,argv[1],100);

    // **************************** BRKGA **************************************
    // define os parametros do BRKGA passados como argumentos               //**
    p       = atoi(argv[3]);                                                //**
    pe      = atof(argv[5]);                                                //**
    pm      = atof(argv[7]);                                                //**
    rhoe    = atof(argv[9]);                                                //**
    // *************************************************************************

    // best solution that is saved in out file
    TSol sBest;

        
        strcpy(instance,nameTable);

        debug = 0;
        numDecoders = 5; 
        numLS = 5;  
        MAXRUNS = 1; 
        MAX_THREADS = 10; 
        OPTIMAL = 0;
        
	//read the informations of the instance
        ReadData(nameTable, n);
        MAXTIME = n/3;

        double foBest = INFINITY,
               foAverage = 0;

        float timeBest = 0,
              timeTotal = 0;

        std::vector <double> ofvs;
        ofvs.clear();

        // best solutions found in MAXRUNS
        sBest.ofv = INFINITY;

	// run BRKGA MaxRuns for each instance
        //printf("\n\nInstance: %s \nRun: ", instance);
        for (int j=0; j<MAXRUNS; j++)
        {
            // fixed seed
            if (debug == 1)
                srand(debug); 
            else
                srand(time(NULL));

            //printf("%d ", j+1);
            
            //CPUbegin = CPUend = CPUbest = clock();
            gettimeofday(&Tstart, NULL);
            gettimeofday(&Tend, NULL);
            gettimeofday(&Tbest, NULL);

            // best solution found in this run
            bestSolution.ofv = INFINITY;

            // execute the evolutionary method
            BRKGA();

            // CPUend = clock();
            gettimeofday(&Tend, NULL);

            // output results
            if (bestSolution.ofv < sBest.ofv)
                sBest = bestSolution;

            // calculate best and average results
            if (bestSolution.ofv < foBest)
                foBest = bestSolution.ofv;

            foAverage += bestSolution.ofv;

            // fitness of each solution found in the runs
            ofvs.push_back(bestSolution.ofv);

            //timeBest += (float)(CPUbest - CPUbegin)/CLOCKS_PER_SEC;
            //timeTotal += (float)(CPUend - CPUbegin)/CLOCKS_PER_SEC;
            timeBest += ((Tbest.tv_sec  - Tstart.tv_sec) * 1000000u + Tbest.tv_usec - Tstart.tv_usec) / 1.e6;
            timeTotal += ((Tend.tv_sec  - Tstart.tv_sec) * 1000000u + Tend.tv_usec - Tstart.tv_usec) / 1.e6; 
        }

        // create a .csv file with average results
        foAverage = foAverage / MAXRUNS;
        timeBest = timeBest / MAXRUNS;
        timeTotal = timeTotal / MAXRUNS;
        
        // free memory with Problem data
        FreeMemoryProblem();

        // free memory of BRKGA components
        FreeMemory();



    // Saida padrao para o BNT recuperar o resultado obtido pelo metodo na configuracao passada como argumento
    std::cout << "Result for BNT: Solved, " << timeBest << ", " << 0.0 << ", " << sBest.ofv << ", "  << 0.0;

    return 0;
}

 
/************************************************************************************
			                  GENERAL FUNCTIONS
*************************************************************************************/

void BRKGA()
{
    // free memory of BRKGA components
    FreeMemory();

    // initialize Q-Table
    //InitiateQTable();

    // define the population size with the higher value of P
    //p = sizeP[sizeof(sizeP)/sizeof(sizeP[0]) - 1]; 

    Pop.resize(p);
    PopInter.resize(p);

    // Create the initial chromossoms with random keys
    #pragma omp parallel for num_threads(MAX_THREADS)
    for (int i=0; i<p; i++)
    {
        TSol ind = CreateInitialSolutions(); 
        ind = Decoder(ind);
        Pop[i] = PopInter[i] = ind;
    }

    //TSol solInicial = CreateInitialSolutionsMenorDist(Pop[0], n);
    //Pop[0] = solInicial;
    // printf("\n\nFO inicial = %lf", Pop[0].ofv);
    // getchar();

    
    // sort population in increase order of fitness
    sort(Pop.begin(), Pop.end(), sortByFitness);

    // save the best solution found in this run
    updateBestSolution(Pop[0]);
    
    // useful local variables
    int numGenerations = 0;             // number of generations
    int bestGeneration = 0;             // generation in which found the best solution
    double bestFitness = Pop[0].ofv;    // best fitness found in past generation
    float currentTime = 0;              // computational time of the search process
    int sumLS = 0;                      // number of local search applied in each generation
    double stdev = 0.0;                 // standard deviation of elite partition

    // run the evolutionary process until stop criterion
    while(1)
    {
    	// number of generations
        numGenerations++;

        // *************************** BRKGA-QL **************************************
        // update Q-Learning parameters                                           //**
        //UpdateQLParameters(currentTime);                                          //**
        //                                                                        //**
        // choose a action (value) for each state (parameter)                     //**
        //ChooseAction();                                                           //**
        //                                                                        //**
        // update population size                                                 //**
        //UpdatePopulationSize();                                                   //**
        // ***************************************************************************

        


        // The 'pe' best chromosomes are maintained, so we just copy these into PopInter:
        #pragma omp parallel for num_threads(MAX_THREADS)
        for (int i=0; i<(int)(p*pe); i++){
            // copy the chromosome for next generation
            PopInter[i] = Pop[i];
        }

        // We'll mate 'p - pe - pm' pairs; initially, i = pe, so we need to iterate until i < p - pm:
        #pragma omp parallel for num_threads(MAX_THREADS) 
        for (int i = (int)(p*pe); i < p - (int)(p*pm); i++){
            // Parametric uniform crossover
        	PopInter[i] = ParametricUniformCrossover();
            PopInter[i] = Decoder(PopInter[i]); 
        }
        
        // We'll introduce 'pm' mutants:
        #pragma omp parallel for num_threads(MAX_THREADS)
        for (int i = p - (int)(p*pm) - (int)(p*pe); i < p; i++){
            PopInter[i] = CreateInitialSolutions();
            PopInter[i] = Decoder(PopInter[i]);
        }  
        
        // Update the current population
        Pop = PopInter;   

        // Sort population in increase order of fitness
        sort(Pop.begin(), Pop.end(), sortByFitness);
        updateBestSolution(Pop[0]);

        // calculate the standard deviation of elite partition
        stdev = CalculateStDev();

        // reward
        R = 0.0;

        // we improve the best fitness in the current population 
        if (Pop[0].ofv < bestFitness){
            bestFitness = Pop[0].ofv;
            bestGeneration = numGenerations;
            R = 1.0;
        }

        // we have a high diversification into the Elite
        if (stdev > 1.0){
            R += 0.25; 
        }

        // if (debug)
        // {
        //     FILE *arquivo;
        //     arquivo = fopen("../Results/Reward.txt","a");
        //     //fprintf(arquivo, "\n%d \t %d",numGenerations, R);
        //     fclose(arquivo);
        // }
        
        // Update the Q-Table values
        //if (R > 0)
        //    UpdateQTable();

        // ********************* LOCAL SEARCH IN COMMUNITIES *******************

        // number of local search applied in the current generation
        sumLS = 0;
        if (numLS > 0)
        {   
            //apply local search when BRKGA found a new better solution or Elite are very similar
            if (R >= 1 || stdev < 0.1 || numGenerations%((int)(n*0.2)) == 0) //
	        {
                // Find commuties in the Elite
	            IC();

	            std::vector <int> promisingSol; 
                promisingSol.clear();

	            for (int i=0; i < (int)(p*pe); i++)
	            {
	                if (Pop[i].promising == 1){
	                	promisingSol.push_back(i);
	                }
                    else if (i > 0){ 
                        // generate caotic individual (crossover between one elite and one mutant)
                        Pop[i] = ChaoticInd(Pop[i]);
                        Pop[i] = Decoder(Pop[i]);

                        // set flag as 0 to permit new local search
                        Pop[i].flag = 0;
                    }
	            }

	            #pragma omp parallel for num_threads(MAX_THREADS)
                for (unsigned int i=0; i < promisingSol.size(); i++)
                {
                    // local search not influence the evolutionary process
                    TSol s = LocalSearch(Pop[promisingSol[i]]);
                    updateBestSolution(s);                    

                    // set flag as 1 to prevent new local search in the same solution
                    Pop[promisingSol[i]].flag = 1;
                }

                sumLS = promisingSol.size();
                promisingSol.clear();

                sort(Pop.begin(), Pop.end(), sortByFitness);
                updateBestSolution(Pop[0]);
	        }
	    }

        // ******************************* RESTART *****************************

        if ((numGenerations - bestGeneration) > n || stdev < 0.0001) 
        {
            bestGeneration = numGenerations;
            #pragma omp parallel for num_threads(MAX_THREADS)
            for (int i=1; i<p; i++){
                Pop[i] = Decoder(CreateInitialSolutions());
            }
            sort(Pop.begin(), Pop.end(), sortByFitness);
            updateBestSolution(Pop[0]);
            bestFitness = Pop[0].ofv;

            if (debug) printf("\n\nRestart...\n\n");
        }

        // print screen
        if (debug){
            printf("\nGeneration: %3d [%4d - %3d(%.2lf) (%3d) - %3d(%.2lf) - (%.2lf)] \t %.2lf (%.2lf) \t %.2lf [%.2lf] \t %.5lf \t %.4lf \t %.4lf",
                        numGenerations, p, (int)(p*pe), pe, sumLS, (int)(p*pm), pm, rhoe, bestSolution.ofv, bestSolution.vec[n].rk, bestFitness, R, stdev, epsilon, lf);
        }

        // terminate the evolutionary process in MAXTIME
        gettimeofday(&Tend, NULL);
        currentTime = ((Tend.tv_sec  - Tstart.tv_sec) * 1000000u + Tend.tv_usec - Tstart.tv_usec) / 1.e6; 
        
        // stop criterium
        if (currentTime >= MAXTIME || floor(100*bestSolution.ofv)/100 <= OPTIMAL){
            break;
        }
    }
}

TSol Decoder(TSol s)
{
    // save the random-key sequence of current solution 
    TSol temp = s;

    int dec = floor(s.vec[n].rk*numDecoders)+1;
    
    // define parameter for classic BRKGA
    //dec = 1;

    switch (dec)
    {
        case 1: 
            s = Dec1(s, n);
            break;

        case 2: 
            s = Dec2(s, n);
            break;
        
        case 3: 
            s = Dec3(s, n);
            break;

        case 4: 
            s = Dec4(s, n);
            break;

        case 5: 
            s = Dec5(s, n);
            break;

        default:
            break;
    }

    // return initial random-key sequence and maintain the solution sequence
    for (int i=0; i<n; i++)
    {
        s.vec[i].rk = temp.vec[i].rk;
    }
    
    return s;
}

TSol LocalSearch(TSol s)
{
    // ***** we use a Random Variable Neighborhood Descent (RVND) as local search ****

    // current neighborhood
	int k = 1;

    // predefined number of neighborhood moves
    std::vector <int> NSL;
    std::vector <int> NSLAux;
    
    for (int i=1; i<=numLS; i++)
    {
        NSL.push_back(i);
        NSLAux.push_back(i);
    }

	while (!NSL.empty())
	{
        // current objective function
        double foCurrent = s.ofv;

        // randomly choose a neighborhood
        int pos = rand() % NSL.size();
        k = NSL[pos];

        switch (k)
        {
            case 1: 
                s = LS1(s, n); // LS6(s,n); 
                break;

            case 2:
                s = LS2(s, n); 
                break;

            case 3:
                s = LS3(s, n); 
                break;

            case 4:
                s = LS4(s, n); 
                break;

            case 5:
                s = LS5(s, n); 
                break;

            case 6:
                s = LS6(s, n); 
                break;

            default:
                break;
        }

        // we better the current solution
        if (s.ofv < foCurrent)
        {
            // refresh NSL
            NSL.clear();
            NSL = NSLAux;
        }
        else
        {
            // Remove N(n) from NSL
            NSL.erase(NSL.begin()+pos);
        }
	} //end while

    // apply 3-Opt
    //s = LS6(s,n);

 	return s;
}

void updateBestSolution(TSol s)
{
    // save the best solution found in this run
    if (s.ofv < bestSolution.ofv)
    {
        bestSolution = s;
        // CPUbest = clock();
        gettimeofday(&Tbest, NULL);
    }
}

void InitiateQTable()
{
    // initiate Q-Table with a random value between 0 and 1
    Q.clear();
    Q.resize(par);

    qTotal = 0.0;

    // rho_e
    for (int j=0; j<sizeof(Rhoe)/sizeof(Rhoe[0]); j++)
    {
        TQ aux;
        aux.S = 0;
        aux.pVar = Rhoe[j];
        aux.q = randomico(0,1); 
        aux.k = 0;
        aux.kImp = 0;

        Q[aux.S].push_back(aux);
        qTotal += aux.q;
    }

    // p
    for (int j=0; j<sizeof(sizeP)/sizeof(sizeP[0]); j++)
    {
        TQ aux;
        aux.S = 1;
        aux.pVar = sizeP[j];
        aux.q = randomico(0,1); 
        aux.kImp = 0;

        Q[aux.S].push_back(aux);
        qTotal += aux.q;
    }

    // pm
    for (int j=0; j<sizeof(Pm)/sizeof(Pm[0]); j++)
    {
        TQ aux;
        aux.S = 2;
        aux.pVar = Pm[j];
        aux.q = randomico(0,1); 
        aux.k = 0;
        aux.kImp = 0;

        Q[aux.S].push_back(aux);
        qTotal += aux.q;
    }

    // pe
    for (int j=0; j<sizeof(Pe)/sizeof(Pe[0]); j++)
    {
        TQ aux;
        aux.S = 3;
        aux.pVar = Pe[j];
        aux.q = randomico(0,1); 
        aux.k = 0;
        aux.kImp = 0;

        Q[aux.S].push_back(aux);
        qTotal += aux.q;
    }
}

void ChooseAction()
{
    // choose actions for each state from Q-Table (e-Greedy)
    for (int i=0; i<par; i++)
    {
        int a, aMax, aAux;

        // set variable a with the current action
        if (i == 0)      a = a0;
        else if (i == 1) a = a1;
        else if (i == 2) a = a2;
        else if (i == 3) a = a3;           
                
        // found actions with the highest value of Q(i,-).q 
        double bQ = -INFINITY;  
        for (int j=0; j<Q[i].size(); j++)
        {
            if (Q[i][j].q > bQ)
            {
                bQ = Q[i][j].q;
                aAux = j;
            }
            else
            if (Q[i][j].q == bQ && randomico(0,1) >= 0.5) // trie randomly
            {
                aAux = j;
            }
            aMax = aAux;

            // update the best future reward
            if (Q[i][j].q > Qmax)
                Qmax = Q[i][j].q;
        }

        // e-greedy policy
        if (randomico(0,1) <= 1-epsilon) 
        {
            // choose the action with highest Q value
            a = aAux;
        }
        else
        {
            // choose a randonly selected action (value)
            a = irandomico(0,Q[i].size()-1);
        }

        // set new action
        switch (i)
        {
            case 0:
                a0 = a;
                break;
        
            case 1:
                a1 = a;
                break;
            
            case 2:
                a2 = a;
                break; 

            case 3:
                a3 = a;
                break;
        }

        // update number of choices state i and action a
        Q[i][a].k++;
    }
        
    // update parameters with actions 
    rhoe    = Q[0][a0].pVar;   
    p       = Q[1][a1].pVar;
    pm      = Q[2][a2].pVar;
    pe      = Q[3][a3].pVar;  
}

void UpdatePopulationSize()
{
    // *** define population size

    // proportional pruning 
    if (Pop.size() > p)
    {
        PopInter = Pop;

        // define new size of Pop
        int currentP = Pop.size();
        Pop.resize(p);

        // select the elite chromosomes
        #pragma omp parallel for num_threads(MAX_THREADS)
        for (int i=0; i<(int)(p*pe); i++){
            // copy p*pe best chromosomes
            Pop[i] = PopInter[i];
        }

        // select the non-elite chromosomes
        int pos = pe * currentP;
        #pragma omp parallel for num_threads(MAX_THREADS)
        for (int i=(int)(p*pe); i<p; i++){
            // copy the chromosome
            Pop[i] = PopInter[pos];
            pos++;
        }

        PopInter.clear();
        PopInter.resize(p);
    }
    
    // generate new chromosomes 
    else if (Pop.size() < p)
    {
        int currentP = Pop.size();
        TSol ind;
        for (int k = currentP; k < p; k++)
        {
            // mutant
            if (randomico(0,1) < pm)
            {
                ind = CreateInitialSolutions();
            }

            // crossover
            else
            {
                // Select an elite parent:
                int eliteParent = irandomico(0,(int)(currentP*pe) - 1);

                // Select a non-elite parent:
                int noneliteParent = irandomico((int)(currentP*pe), currentP-1);

                // Mate:  
                ind = Pop[noneliteParent];
                for(int j = 0; j < n+1; j++)
                {
                    //copy alelos of elite chromossom of the new generation
                    if (randomico(0,1) < rhoe)
                        ind.vec[j].rk = Pop[eliteParent].vec[j].rk;
                }

                // set the flag of local search as zero
                ind.flag = 0;
            }

            ind = Decoder(ind);
            Pop.push_back(ind);
        }
        sort(Pop.begin(), Pop.end(), sortByFitness);
        updateBestSolution(Pop[0]);
        PopInter.resize(p);
    }
}

void UpdateQLParameters(float currentTime)
{
    //initial and minimum epsilon 
    float initial_epsilon = 1.0;
    float minimum_epsilon = 0.01;

    // **** define parameter epsilon ****
    // exponential decay
    epsilon = initial_epsilon * pow(minimum_epsilon, (currentTime / MAXTIME));

    // *** define learning rate ***
    // initialy, a higher priority is given to the newly gained information (exploration mode)
    // then, we decrement lf and have a higher priority for the existing information in Q-Table (exploitation mode)
    lf = 1 - (0.9 * currentTime / MAXTIME);

    // *** define discount rate ***
    // we look for a higher, long-term reward
    df = 0.8;
}

void UpdateQTable()
{ 
    if (debug) printf("\n\nUpdate Q-table");

    for (int s=0; s<par; s++)
    {
        int a; 

        switch (s)
        {
            case 0:
                a = a0;
                break;
            
            case 1:
                a = a1;
                break;

            case 2:
                a = a2;
                break;

            case 3:
                a = a3;
                break;
        }
        
        qTotal -= Q[s][a].q;

        if (debug) printf("\ns: %d, a: %d, Q = %.3lf (R = %.2lf, Qmax = %.2lf, df = %.2lf, lf = %.2lf)", s, a, Q[s][a].q, R, Qmax, df, lf);

        //Q-Learning
        // Q(s,a) is incremented when the action leads to a state, in which there exists an action such that the best possible Q-value and
        // the reward R is greater than current value of Q(s,a).
        // i.e., the old value of Q(s,a) was too pessimistic 
        // df*Qmax is the target Q-value

        Q[s][a].q = Q[s][a].q + lf*(R + df*Qmax - Q[s][a].q ); 
       
        Q[s][a].kImp++;
        qTotal += Q[s][a].q;

        if (debug) printf(" => Q = %.3lf ", Q[s][a].q);
    }

    if (debug) printf("\n");
}

double CalculateStDev()
{
    // vector with fitness of the elite partition 
    std::vector <double> v;             

    // express the variability of the data in terms of gap from the best solution
    for (int i=0; i<(int)(p*pe); i++){
        v.push_back(100*((Pop[i].ofv - Pop[0].ofv)/Pop[0].ofv));}

    double sum = std::accumulate(std::begin(v), std::end(v), 0.0);
    double mean =  sum / v.size();

    double accum = 0.0;
    std::for_each (std::begin(v), std::end(v), [&](const double d) {
        accum += (d - mean) * (d - mean);
    });
    double stdev = sqrt(accum / (v.size()-1));

    // double sq_sum = std::inner_product(v.begin(), v.end(), v.begin(), 0.0);
    // double stdev = std::sqrt(sq_sum / v.size() - mean * mean);

    return stdev;
}

TSol CreateInitialSolutions()
{
	TSol s;
	TVecSol aux;

    s.vec.clear();

	// create a random-key for each allelo (consider decoder type in the n-th random-key)
	for (int j = 0; j < n+1; j++)
	{
		aux.rk  = randomico(0,1);  // random value between [0,1[
        s.vec.push_back(aux);
	}

    // flag to control the local search memory
    s.flag = 0;

	return s;
}

TSol ChaoticInd(TSol s)
{
    // generate a caotic individual
    for (int k=0; k<n+1; k++)
    {      
        if (randomico(0,1) > rhoe)
           s.vec[k].rk = randomico(0,1);
    }

    // set the flag of local search as zero
    s.flag = 0;
    
    return s;
}

TSol ParametricUniformCrossover()
{	
	TSol s;

	// create a new offspring
	s.vec.resize(n+1);

    // Select an elite parent:
    int eliteParent = irandomico(0,(int)(p*pe) - 1);

    // Select a non-elite parent:
    int noneliteParent = irandomico((int)(p*pe), p-1);

    // Mate:  // including decoder gene in the n-th rk 
    for(int j = 0; j < n+1; j++)
    {
        //copy alelos of top chromossom of the new generation
        if (randomico(0,1) < rhoe)
           s.vec[j].rk = Pop[eliteParent].vec[j].rk;
        else
           s.vec[j].rk = Pop[noneliteParent].vec[j].rk;
    }

    // set the flag of local search as zero
    s.flag = 0;

    return s;
}

double PearsonCorrelation(std::vector <TVecSol> X, std::vector <TVecSol> Y)
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

void writeLPGraph(std::vector<std::vector<std::pair<int, double> > > &listaArestas) 
{	
	// Set id in groups between 1 and n
	int i, j;
	int n = listaArestas.size();
	int newId = 1;
	std::vector<int> newIds(n, 0);
	for (i = 0; i < n; i++) {
		if (newIds[Pop[i].label] == 0) {
			newIds[Pop[i].label] = newId;
			newId++;
		}
	}
	for (i = 0; i < n; i++) {
		Pop[i].label = newIds[Pop[i].label];
	}

	// Name file .json (LP-<generation>.json)
    numLP++;
	std::string jsonfile = "LP-";
	jsonfile += std::to_string(numLP);
	jsonfile += ".json";

	// Create a graph file (.json)
	int totalArestas = 0;
	std::string json = "{\n  \"nodes\": [\n";
	for (i = 0; i < listaArestas.size(); i++) {			// Insert vertices
		totalArestas += listaArestas[i].size();
		if(i == listaArestas.size() - 1)
			json += "    {\"id\": \"" + std::to_string(i) + "\", \"group\": " + std::to_string(Pop[i].label) + "}\n";
		else
			json += "    {\"id\": \"" + std::to_string(i) + "\", \"group\": " + std::to_string(Pop[i].label) + "},\n";
	}
	totalArestas /= 2;
	json += "  ],\n";
	json += "  \"links\": [\n";							// Insert edges
	int totalArestasInseridas = 0;
	for (i = 0; i < listaArestas.size(); i++) {
		for (j = 0; j < listaArestas[i].size(); j++) {
			if (i < listaArestas[i][j].first) {
				
				// Create an output string stream
				std::ostringstream peso;
				// Set Fixed -Point Notation
				peso << std::fixed;
				// Set precision to 2 digits
				peso << std::setprecision(2);
				//Add double to stream
				peso << listaArestas[i][j].second;
				// Get string from output string stream
				std::string pesoString = peso.str();
				
				json += "    {\"source\": \"" + std::to_string(i) + "\", \"target\": \"" + std::to_string(listaArestas[i][j].first) + "\", \"value\": " + pesoString + "}";
				
				totalArestasInseridas++;
				if (totalArestasInseridas != totalArestas)
					json += ",\n";
				else
					json += "\n";
			}
		}
	}
	json += "  ]\n";
	json += "}";

	// Save .json file
	std::ofstream myfile;
	myfile.open("LP/"+jsonfile);
	myfile << json;
	myfile.close();

	// Name .json file (LP-<generation>.json)
	std::string htmlfile = "LP-";
	htmlfile += std::to_string(numLP);
	htmlfile += ".html";

	// Creat a html with ghaph library and the graph (.json)
	std::string html = "<head>\n";
	html += "\t<style> body{ margin : 0; } </style>\n";
	html += "\t<script src = \"//unpkg.com/three\"></script>\n";
	html += "\t<script src=\"//unpkg.com/three-spritetext\"></script>\n";
	html += "\t<script src = \"//unpkg.com/3d-force-graph\"></script>\n";
	html += "</head>\n";
	html += "<body>\n";
	html += "\t<div id=\"3d-graph\"></div>\n";
	html += "\t<script>\n";
	html += "\t\tconst Graph = ForceGraph3D()\n";
	html += "\t\t(document.getElementById('3d-graph'))\n";
	html += "\t\t.jsonUrl('" + jsonfile + "')\n";
	html += "\t\t.nodeLabel('id')\n";
	html += "\t\t.nodeAutoColorBy('group')\n";
	html += "\t\t.linkThreeObjectExtend(true)\n";
	html += "\t\t.linkThreeObject(link => {\n";
	html += "\t\t\tconst sprite = new SpriteText(`${link.value}`);\n";
	html += "\t\t\tsprite.color = 'lightgrey';\n";
	html += "\t\t\tsprite.textHeight = 1.5;\n";
	html += "\t\t\treturn sprite;\n";
	html += "\t\t})\n";
	html += "\t\t.linkPositionUpdate((sprite, { start, end }) => {\n";
	html += "\t\t\tconst middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({\n";
	html += "\t\t\t[c]: start[c] + (end[c] - start[c]) / 2 })));\n";
	html += "\t\t\tObject.assign(sprite.position, middlePos);\n";
	html += "\t\t});\n";
	html += "\t\tGraph.d3Force('charge').strength(-120);\n";
	html += "\t</script>\n";
	html += "</body>";
	
	// Save .html file
	myfile.open("LP/" + htmlfile);
	myfile << html;
	myfile.close();
}

void IC() 
{
    int Tpe = (int)p*pe;
    std::vector<std::vector<std::pair<int, double> > > listaArestas(Tpe, std::vector<std::pair<int, double> >());

	// create weighted (pearson correlation) graph
	int entrouAresta = 0;
	double pearson = 0.0;
	for (int i = 0; i < Tpe - 1; i++) {
		for (int j = i + 1; j < Tpe; j++)
		{
			pearson = PearsonCorrelation(Pop[i].vec, Pop[j].vec);
			if (pearson > 0.6) {
				entrouAresta++;
				listaArestas[i].push_back(std::make_pair(j, pearson));
				listaArestas[j].push_back(std::make_pair(i, pearson));
			}
		}
	}

	// apply clustering method
	LP(listaArestas);

    /*if (debug) {
		writeLPGraph(listaArestas);
	}*/

	PromisingLP();
    listaArestas.clear();
}

void LP(std::vector<std::vector<std::pair<int, double> > > listaArestas)
{
    int nk = listaArestas.size();

	// Create vector with visit order
	std::vector<int> ordemVisita(nk);
	iota(ordemVisita.begin(), ordemVisita.end(), 0);

	// initialize each node with its own label
	for (int i = 0; i < nk; i++)
		Pop[i].label = i;

	int iteracao = 1;
	int labelVizinho, melhorLabel;
	double melhorPeso;
	std::map<int, double> totalLabels;
	std::map<int, double>::iterator it;

	int movimentos = 1;
	while (movimentos) {
		movimentos = 0;
		random_shuffle(ordemVisita.begin(), ordemVisita.end());
		for (auto idVertice : ordemVisita) {

			// Calculate the weigth of the labels
			totalLabels.clear();
			for (auto idVizinho : listaArestas[idVertice]) {
				labelVizinho = Pop[idVizinho.first].label;
				it = totalLabels.find(labelVizinho);
				if (it != totalLabels.end()) {
					it->second += idVizinho.second;
				}
				else {
					totalLabels[labelVizinho] = idVizinho.second;
				}
			}

			// Best label is itself initially
			melhorLabel = Pop[idVertice].label;
			melhorPeso = std::numeric_limits<double>::min();
			for (auto totais : totalLabels) {
				if (totais.second > melhorPeso) {
					melhorLabel = totais.first;
					melhorPeso = totais.second;
				}
			}

			if (melhorLabel != Pop[idVertice].label) {
				Pop[idVertice].label = melhorLabel;
				movimentos = 1;
			}
		}
		iteracao++;
	}

    ordemVisita.clear();
}

void PromisingLP()
{
    int Tpe = (int)p*pe;
    std::vector <int> grupos;
	int tamanhoGrupos = 0;

	// initialize promisings solutions
	for (int i = 0; i < Tpe; i++)
		Pop[i].promising = 0;

	// save labels defined by LP in groups
	int achei;

    for (int i = 0; i < Tpe; i++)
	{
		achei = 0;
		for (unsigned int j = 0; j < grupos.size(); j++)
		{
			if (Pop[i].label == grupos[j])
				achei = 1;
		}
		if (achei == 0)
		{
			tamanhoGrupos++;
			grupos.push_back(Pop[i].label);
		}
	}

	// find the best solution in the group (with flag = 0)
	for (unsigned int j = 0; j < grupos.size(); j++)
	{
		double menorFO = INFINITY;
		int localMenor = -1;
		int local = -1;
		for (int i = 0; i < Tpe; i++)
		{
			if (Pop[i].label == grupos[j])
			{
				// find the best solution of the group
				if (local == -1)
					local = i;

				// we not apply local search in this solution yet
                if (Pop[i].ofv < menorFO && Pop[i].flag == 0) 
				{
					menorFO = Pop[i].ofv;
					localMenor = i;
				}
			}
		}

		if (localMenor == -1)
			localMenor = local;

		if (Pop[localMenor].label != -1)
			Pop[localMenor].promising = 1;
	}
}

TSol PathRelinking(TSol atual, TSol guia)
{
    TSol melhorCaminho = atual;     //melhor solucao obtida pelo PR
    TSol melhorIteracao = atual;    //melhor solucao em cada iteracao
    TSol sCorrente = atual;         //solucao corrente em cada iteracao
    TSol sViz = atual;              //solucao vizinha em cada iteracao

    //calcula a diferenca entre as solucoes
    int distance=0;
    std::vector<int> diferenca;
    diferenca.resize(n,0);

    for (int i=0; i<n; i++)
    {
    	if (atual.vec[i].rk != guia.vec[i].rk){
            diferenca[i] = 1;
            distance++;
        }
    }

    //inicializa o processo de busca do PR
    int melhorindice = -1;
    int limiteCaminho = 1; //(int)(distance*0.2); //pesquisar somente em 80% do caminho
    while(distance > limiteCaminho)
    {
        melhorindice = -1;
        melhorIteracao.ofv = INFINITY;

        //examinar todas as trocas possiveis em uma iteracao do PR
        for(int i=0; i<n; i++)
        {
            if(diferenca[i] == 1)
            {
                //gerar o vizinho da solucao corrente
                sViz = sCorrente;
                sViz.vec[i].rk = guia.vec[i].rk;
                sViz = Decoder(sViz);

                //verficar se eh a melhor solucao da iteracao
                if(sViz.ofv < melhorIteracao.ofv){
                    melhorIteracao = sViz;
                    melhorindice = i;
                }
            }
        }

        //verificar se eh a melhor solucao do caminho
        if (melhorIteracao.ofv < melhorCaminho.ofv)
        {
            melhorCaminho = melhorIteracao;
            if (debug)
              printf("\nmelhorou %.0lf - %.0lf >> %.0lf", atual.ofv, guia.ofv, melhorCaminho.ofv);
        }

        //continuar a busca a partir da melhor solucao da iteracao
        sCorrente = melhorIteracao;

        //apagar o indice do cliente trocado nesta iteracao
        diferenca[melhorindice] = 0;

        //diminuir o numero de movimentos possiveis
        distance--;
    }

    return melhorCaminho;
}

void FreeMemory()
{
    //methods
    Pop.clear();
    PopInter.clear();
    Q.clear();
}

double randomico(double min, double max)
{
	return ((double)(rand()%10000)/10000.0)*(max-min)+min;
    //return std::uniform_real_distribution<double>(min, max)(rng);
}

int irandomico(int min, int max)
{
	return (int)randomico(0,max-min+1.0) + min;
}
