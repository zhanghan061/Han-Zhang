
# coding: utf-8

# In[ ]:

def flow_with_demands(graph):
    """Computes a flow with demands over the given graph.
    
    Args:
        graph: A directed graph with nodes annotated with 'demand' properties and edges annotated with 'capacity' 
            properties.
        
    Returns:
        A dict of dicts containing the flow on each edge. For instance, flow[s1][s2] should provide the flow along
        edge (s1, s2).
        
    Raises:
        NetworkXUnfeasible: An error is thrown if there is no flow satisfying the demands.
    """

    #I implement Ford_Fulkerson Algorithm by myself
    
    #First check the necessary condition
    
    
    sum_demand=0
    sum_supply=0
    for node in graph.nodes():
        if graph.node[node]['demand']>0:
            sum_demand+=graph.node[node]['demand']
        elif graph.node[node]['demand']<0:
            sum_supply+=graph.node[node]['demand']
            
    if sum_demand!=(-sum_supply):
        raise nx.NetworkXUnfeasible
        
            
            
            
    #Do reduction on graph
    graph_local = graph.to_directed()#make a local copy of graph
    graph_local.add_node('s1',demand=0)
    graph_local.add_node('t1',demand=0)
    for node in graph_local.nodes():
        if graph_local.node[node]['demand']<0:
            graph_local.add_edge('s1',node,capacity=-graph_local.node[node]['demand'])
        elif graph_local.node[node]['demand']>0:
            graph_local.add_edge(node,'t1',capacity=graph_local.node[node]['demand'])
            
    
    
    
    def construct_Gf (graph,f):
        Gf=nx.DiGraph()
        Gf.add_nodes_from(graph.nodes())
        for (u,v) in graph.edges():
            if f[u][v]<graph.edge[u][v]['capacity']:
                Gf.add_edge(u,v,capacity=graph.edge[u][v]['capacity']-f[u][v],direction=1)
            if f[u][v]>0:
                Gf.add_edge(v,u,capacity=f[u][v],direction=0)
        return Gf



    def Augment(f,Gf,P):
        #get the list of edges of a path
        G_temp=nx.DiGraph()
        G_temp.add_path(P)
        #get the list of residual capacity of all edges in P and compute minimum C(P)
        residual_capacity=[]
        for (u,v) in G_temp.edges():
            residual_capacity.append(Gf.edge[u][v]['capacity'])
    
        C_P=min(residual_capacity)
    
        for (u,v) in G_temp.edges():
            if Gf.edge[u][v]['direction']==1:
                f[u][v]=f[u][v]+C_P
            else:
                f[v][u]=f[v][u]-C_P
    
        return f

    def Ford_Fulkerson(graph,s,t):
    
        f={}   #function flow (dictionary)
        #set all flows to zero
        for node in graph.nodes():
            neighbors={}
            neighbor=[]
            f[node]=neighbors
            neighbor=graph.neighbors(node)
            for n in neighbor:
                neighbors[n]=0
    
    
        
        Gf=construct_Gf(graph,f)
        path=find_a_simple_path(Gf,s,t)#find a simple path in Gf using BFS
    
    
        while path!=[]:
        
        
            f=Augment(f,Gf,path)
            Gf=construct_Gf(graph,f)
            path=find_a_simple_path(Gf,s,t)
    
        return f


    
    
    def find_a_simple_path(graph,s,t):
        path_temp=[]
        predecessors=nx.bfs_predecessors(graph,s)
        if t not in predecessors:
            return path_temp
        else:
            path_temp.append(t)
            pre=predecessors[t]
            path_temp.append(pre)
            while pre!=s:
                pre=predecessors[pre]
                path_temp.append(pre)
            path=[]
            for i in range(0,len(path_temp)):
                path.append(path_temp[len(path_temp)-1-i])
            return path


    f=Ford_Fulkerson(graph_local,'s1','t1')
    
    max_flow=0
    for node in f['s1']:
        max_flow+=f['s1'][node]
    
    sum_demand=0
    for node in graph.nodes():
        if graph.node[node]['demand']>0:
            sum_demand+=graph.node[node]['demand']
     
    if max_flow!=sum_demand:
        raise nx.NetworkXUnfeasible
        
    
    #remove the supplementary 's1','t1'nodes and their flows from the flows
    del f['s1']
    del f['t1']
    for node in f:
        if 't1' in f[node]:
            del f[node]['t1']
    
    
    return f



def divergence(flow):
    """Computes the total flow into each node according to the given flow dict.
    
    Args:
        flow: the flow dict recording flow between nodes.
        
    Returns:
        A dict of the net flow into each node.
    """
    
    flow_in={}
    for node in flow:
        flow_in[node]=0
   
    for node in flow:
        for neighbor in flow[node]:
            flow_in[neighbor]+=flow[node][neighbor]
            flow_in[node]-=flow[node][neighbor]
    
    return flow_in

