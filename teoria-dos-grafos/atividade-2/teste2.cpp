#include <bits/stdc++.h>
using namespace std;
 
class Graph {
public:
    int tamanho;
    map<int, list<int> > adj;
    void adicionarAresta(int v, int w);
};
 
void Graph::adicionarAresta(int v, int w){
    if(v == tamanho - 1){
        adj[v].push_back(w);
    } else if(w == tamanho - 1){
        adj[w].push_back(v);
    } else {
        adj[w].push_back(v);
        adj[v].push_back(w);
    }
}
 
int main()
{
 
    Graph g;
    int n, m, u, v, i;
 
    scanf("%d", &n);
    scanf("%d", &m);
    g.tamanho = n;
 
    for(i = 0; i < m; i++){
        scanf("%d", &u);
        scanf("%d", &v);
        g.adicionarAresta(u, v);
    }
 
    return 0;
}