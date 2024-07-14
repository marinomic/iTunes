import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._album = None

    def handleCreaGrafo(self, e):
        nMinDurata = self._view._txtInDurata.value
        try:
            durata = int(nMinDurata)
        except ValueError:
            warnings.warn_explicit(message="Durata non è un intero",
                                   category=TypeError,
                                   filename="controller.py",
                                   lineno=15)
            return
        self._model.creaGrafo(durata)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato:"))
        self._view._txt_result.controls.append(ft.Text(self._model.getGraphDetails()))
        albums = self._model.getNodes()
        albums.sort(key=lambda x: x.Title)
        # Metodo 1
        # for a in albums:
        #     self._view._ddAlbum.options.append(ft.dropdown.Option(data=a,
        #                                                           text=a.Title,
        #                                                           on_click=self.getSelectedAlbum))
        listDD = map(lambda x: ft.dropdown.Option(data=x,
                                                  text=x.Title,
                                                  on_click=self.getSelectedAlbum), albums)
        self._view._ddAlbum.options.extend(listDD)
        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._album = None
        else:
            self._album = e.control.data
        print(f"getSelectedAlbum called --> {self._album}")

    def handleAnalisiComp(self, e):
        if self._album is None:
            warnings.warn("Nessun album selezionato")
            return
        dim, totalD = self._model.analisiComponente(self._album)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Analisi della componente connessa dell'album {self._album}:"))
        self._view._txt_result.controls.append(ft.Text(f"Dimensione: {dim}"))
        self._view._txt_result.controls.append(ft.Text(f"Durata complessiva: {totalD}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        dTOTtxt = self._view._txtInSoglia.value
        try:
            dTOT = int(dTOTtxt)
        except ValueError:
            warnings.warn("Soglia not integer.")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Soglia inserita non valida. Inserire un intero"))
            self._view.update_page()
            return
        if self._album is None:
            warnings.warn("Nessun album selezionato")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Nessun album selezionato"))
            self._view.update_page()
            return
        path, totCost = self._model.getSetAlbum(self._album, dTOT)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Set di album con durata totale di {totCost} minuti:"))
        for a in path:
            self._view._txt_result.controls.append(ft.Text(a))
        self._view.update_page()
