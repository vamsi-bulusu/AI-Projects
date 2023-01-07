#include <bits/stdc++.h>
using namespace std;

class DSU {
    public:
        vector<int> parent, rank, size;
        
        DSU(int n){
            for(int i = 0; i < n; i++){
                parent.push_back(i);
                rank.push_back(0);
                size.push_back(1);
            }
        }

        int find(int u){
            if(parent[u] == u) return u;
            return parent[u] = find(parent[u]);
        }

        void Union(int u, int v){
            int pu = find(u);
            int pv = find(v);

            if(pu != pv){
                if(size[pu] < size[pv]){
                    swap(pu, pv);
                }
                parent[pv] = pu;
                size[pu] += size[pv];
            }
        }

};

vector<int> getTheGroups(int n, vector<string> queryType, vector<int> students1, vector<int> students2){
    DSU dsu(n + 1);
    vector<int> result;
    for(int i = 0; i < queryType.size(); i++){
        if(queryType[i] == "Friend"){
            dsu.Union(students1[i], students2[i]);
        } else {
            int rks1 = dsu.size[dsu.parent[students1[i]]], rks2 = dsu.size[dsu.parent[students2[i]]];
            result.push_back(rks1 + rks2);
        }
    }
    cout << "parent array\n";
    for(int i : dsu.size){
        cout << i << " ";
    } 

    return result;
}


int solve(vector<pair<int, int>> nodes){
    DSU network(100000 + 1);
    int result = 0;
    for(int i = 0; i < nodes.size(); i++){
        network.Union(nodes[i].first, nodes[i].second);
        for(int i = 0; i < 100001; i++){
            result = max(result, network.size[i]);
        }
    }
    return result;
}

int main(){

    int T, M, X, Y;
    cin >> T;

    while(T--){
        cin >> M;
        vector<pair<int, int>> nodes;
        for(int i = 0; i < M; i++){
            cin >> X >> Y;
            nodes.push_back(make_pair(X, Y));
        }
        cout << solve(nodes) << "\n";
    }
    return 0;
}