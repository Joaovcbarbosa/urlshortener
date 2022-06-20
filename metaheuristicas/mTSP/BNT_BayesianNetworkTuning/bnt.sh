g++ -c -O3 scenario.cpp -o scenario.o -fopenmp
g++ -c -O3 paramreader.cpp -o paramreader.o -fopenmp
g++ -c -O3 individual.cpp -o individual.o -fopenmp
g++ -c -O3 population.cpp -o population.o -fopenmp
g++ -c -O3 bayesiannetwork.cpp -o bayesiannetwork.o -fopenmp
g++ -c -O3 boa.cpp -o boa.o -fopenmp
g++ -c -O3 main.cpp -o main.o -fopenmp

g++ *.o -o bnt.out -fopenmp -lpthread
