class lista_fav():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.err = False
        self.modified =False
        lista = self.session.get("fav")

        if not lista:
            lista = self.session["fav"] = []

        self.lista = lista    
    
    def agregar(self, pokemon):
        
        for pok in self.lista:
            if pokemon["id"] == pok["id"]:
               self.err = True
        if not self.err:
            self.lista.append(pokemon)

        self.guardar()   

    def eliminar(self, pokemon):
        print("hola " + str(self.lista))
        for pok in self.lista:
            if pokemon["id"] == pok["id"]:
               
               self.lista.remove(pok)
               
               break
        self.guardar()
    def guardar(self):
        self.session["fav"] = self.lista
        self.modified=True

