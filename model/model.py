import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._solBest = None
        self._totCosto = 0

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
        # Durata complessiva degli album nella componente connessa (durata di ogni album in minuti)
        durata = sum([a.totDurata for a in cc]) / 60000
        return dim, durata

    def getSetAlbum(self, a1, soglia):
        self._solBest = None
        self._totCosto = 0
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale = set([a1])
        connessa.remove(a1)

        self._ricorsione(parziale, connessa, soglia)

        return self._solBest, self.calcolaPeso(self._solBest)

    def _ricorsione(self, parziale, connessa, soglia):
        """
        Utilizzare un algoritmo ricorsivo per estrarre un set di album dal grafo che abbia le seguenti caratteristiche:
            • includa a1;
            • includa solo album appartenenti alla stessa componente connessa di a1;
            • includa il maggior numero possibile di album;
            • abbia una durata complessiva, definita come la somma della durata degli album in esso contenuti, non superiore dTOT.
        """
        # CASO TERMINALE
        # 1) Verificare che parziale sia una soluzione ammissibile
        # Questo controllo devo farlo prima di salvare la soluzione ottima, altrimenti rischio di
        # salvare una soluzione non ammissibile
        if self.calcolaPeso(parziale) > soglia:
            return
        # 2) Verificare se la soluzione trovata è migliore di quella attuale
        if len(parziale) > self._totCosto:
            self._solBest = copy.deepcopy(parziale)
            self._totCosto = len(parziale)

        # 3) CASO RICORSIVO
        # Posso ancora aggiungere nodi
        # 4) Prendo i vicini dell'ultimo nodo e provo ad aggiungerli
        for nodo in connessa:
            # Tipicamente qua inserisco dei vincoli, per esempio questo:
            if nodo not in parziale:
                parziale.add(nodo)
                # Per accorciare i cicli dentro la ricorsione posso fare una copia di connessa e rimuovere il nodo
                # che ho appena aggiunto a parziale, in modo da non ripassare su di esso
                # rimanenti = copy.deepcopy(connessa)
                # rimanenti.remove(nodo)
                self._ricorsione(parziale, connessa, soglia)
                parziale.remove(nodo)

    def calcolaPeso(self, listOfNodes):
        dtot = 0
        for a in listOfNodes:
            dtot += a.totDurata
        # oppure
        # return sum([a.totDurata for a in listOfNodes]) / 60000
        return dtot / 60000
