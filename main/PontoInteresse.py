#Classe Objeto Ponto de Interesse

class PontoInteresse:
    def __init__(self, nmPontoInteresse, lat, longitude):
        self.nmPontoInteresse = nmPontoInteresse
        self.latitude = lat
        self.longitude = longitude

    def setNome(self, nmPontoInteresse):
        self.nmPontoInteresse = nmPontoInteresse

    def setLatitude(self, lat):
        self.lat = lat

    def setLongitude(self, lng):
        self.lng = lng

    def getNmPontoInteresse(self):
        return self.nmPontoInteresse

    def getLatitude(self):
        return self.lat

    def getLongitude(self):
        return self.lng


