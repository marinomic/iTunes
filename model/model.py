import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def creaGrafo(self, durata):
        self._grafo.clear()
        allNodes = DAO.getAllALbums(durata)
        self._grafo.add_nodes_from(allNodes)
        self._idMap = {a.AlbumId: a for a in allNodes}
        edges = DAO.getEdges(self._idMap)
        # edges è una lista di tuple, ogni tupla contiene due album collegati tra loro e il metodo add_edges_from
        # vuole proprio una lista di tuple come parametro
        self._grafo.add_edges_from(edges)

    def getGraphDetails(self):
        return f"Numero di nodi: {self._grafo.number_of_nodes()}\nNumero di archi: {self._grafo.number_of_edges()}"

    def getNodes(self):
        return list(self._grafo.nodes())

    def getEdges(self):
        return len(self._grafo.edges())

    def analisiComponente(self, album):
        # Componente connessa a cui appartiene l'album selezionato
        cc = nx.node_connected_component(self._grafo, album)
        # Dimensione della componente connessa
        dim = len(cc)
        # Durata complessiva degli album nella componente connessa
        durata = sum([a.totDurata for a in cc])/60000
        return dim, durata

