CCC = g++ -std=c++11 
FLAGS = -c -O3 -m64 -fopenmp -g

bnt: $(CVRPSEP) scenario.o paramreader.o individual.o population.o bayesiannetwork.o boa.o main.o
	g++ scenario.o paramreader.o individual.o population.o bayesiannetwork.o boa.o main.o -o bnt.out

scenario.o: scenario.cpp
	$(CCC) $(FLAGS) scenario.cpp -o scenario.o

paramreader.o: paramreader.cpp
	$(CCC) $(FLAGS) paramreader.cpp -o paramreader.o

individual.o: individual.cpp
	$(CCC) $(FLAGS) individual.cpp -o individual.o

population.o: population.cpp
	$(CCC) $(FLAGS) population.cpp -o population.o

bayesiannetwork.o: bayesiannetwork.cpp
	$(CCC) $(FLAGS) bayesiannetwork.cpp -o bayesiannetwork.o

boa.o: boa.cpp
	$(CCC) $(FLAGS) boa.cpp -o boa.o

main.o: main.cpp
	$(CCC) $(FLAGS) main.cpp -o main.o

clean: 
	rm -rf *.o *~
