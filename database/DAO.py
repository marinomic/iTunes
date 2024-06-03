from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAllALbums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*, sum(t.Milliseconds) as totDurata
                    from album a , track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId
                    having totDurata/60000 > %s"""

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        """
        Due album a1 e a2 sono collegati tra loro se almeno una canzone (tabella track) di a1 e una canzone di a2
        sono state inserite da un utente all’interno di una stessa playlist (tabella PlaylistTrack).
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinctrow t.AlbumId as a1, t2.AlbumId as a2
        from playlisttrack p , track t , playlisttrack p2 , track t2 
        where t.AlbumId <> t2.AlbumId 
        and t.TrackId = p.TrackId 
        and t2.TrackId = p2.TrackId
        and p2.PlaylistId = p.PlaylistId
        """

        cursor.execute(query)

        for row in cursor:
            # aggiungo solo se i nodi gia' esistono, cioè se gli album hanno la durata maggiore di quella inserita
            if row['a1'] in idMap and row['a2'] in idMap:
                result.append((idMap[row['a1']], idMap[row['a2']]))

        cursor.close()
        conn.close()
        return result
