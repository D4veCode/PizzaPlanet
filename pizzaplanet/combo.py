from pizzaplanet import database

class Combo:

    conn = database.createConnection("pizzaplanet.db")

    def main(self):
        while True:
            print("Seleccione el día")
            print("1. Lunes")
            print("2. Martes")
            print("3. Miércoles")
            print("4. Jueves")
            print("5. Viernes")
            print("6. Sábado")
            print("7. Domingo")
            print("8. Crear un nuevo combo del día")
            print("0. Volver")

            opcion = self.validate_Entry()

            if (opcion == 1):
                self.mostrar_combo("lunes")
            
            elif (opcion == 2):
                self.mostrar_combo("martes")
            
            elif (opcion == 3):
                self.mostrar_combo("miercoles")

            elif (opcion == 4):
                self.mostrar_combo("jueves")
            
            elif (opcion == 5):
                self.mostrar_combo("viernes")
            
            elif (opcion == 6):
                self.mostrar_combo("sabado")
            
            elif (opcion == 7):
                self.mostrar_combo("domingo")

            elif (opcion == 8):
                self.menu_crear_combo()

            elif(opcion == 0):
                break

    def mostrar_combo(self, dia):
        comboController = database.ComboController(self.conn)
        combo = comboController.getCombo(dia)
        self.cls(0)
        for comb in combo:
            self.cls(0)
            precio = comb[2]+comb[5]
            print("Combo del día {}".format(comb[0]))
            print("Pizza tamaño {}".format(comb[1]), "con {}".format(comb[4]))
            print("Valor original: ", precio, " UMs")
            print("Precio con ", comb[3]," por ciento de descuento: ", precio-precio*comb[3]/100, "UMs")
            break

    def menu_crear_combo(self):
        while True:
            print("\t\t---- Creando combo del día 1/4 ----")
            print("Seleccione el día para crear el descuento")
            print("1. Lunes")
            print("2. Martes")
            print("3. Miércoles")
            print("4. Jueves")
            print("5. Viernes")
            print("6. Sábado")
            print("7. Domingo")
            print("0. Volver")

            opcion = self.validate_Entry()

            if (opcion == 1):
                self.menu_crear_combo2("lunes")
            
            elif (opcion == 2):
                self.menu_crear_combo2("martes")
            
            elif (opcion == 3):
                self.menu_crear_combo2("miercoles")

            elif (opcion == 4):
                self.menu_crear_combo2("jueves")
            
            elif (opcion == 5):
                self.menu_crear_combo2("viernes")
            
            elif (opcion == 6):
                self.menu_crear_combo2("sabado")
            
            elif (opcion == 7):
                self.menu_crear_combo2("domingo")

            elif(opcion == 0):
                break
            
            break

        
    def menu_crear_combo2(self, dia):
        while True:
            print("\t\t---- Creando combo del día 2/4 ----")
            print("Seleccione el tamaño de la pizza a ofertar el día ", dia)
            print("1. Personal")
            print("2. Mediana")
            print("3. Familiar")

            opcion = self.validate_Entry2()

            if (opcion == 1):
                self.menu_crear_combo3(dia, "personal", 10)
            
            elif (opcion == 2):
                self.menu_crear_combo3(dia, "mediana", 15)
            
            elif (opcion == 3):
                self.menu_crear_combo3(dia, "familiar", 20)
            
            break

    def menu_crear_combo3(self, dia, tamano, precio_base):
        while True:
            print("\t\t---- Creando combo del día 3/4 ----")
            print("Seleccione el ingrediente de la pizza ", tamano, " a ofertar el día ", dia)
            print("1. Jamón")
            print("2. Champiñones")
            print("3. Pimentón")
            print("4. Doble queso")
            print("5. Aceitunas")
            print("6. Pepperoni")
            print("7. Salchichón")

            opcion = self.validate_Entry3()
            ingredienteController = database.IngredienteController(self.conn)

            if (opcion == 1):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('jamon',tamano))
            
            elif (opcion == 2):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('champiñones',tamano))
            
            elif (opcion == 3):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('pimenton',tamano))
            
            elif (opcion == 4):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('doble queso',tamano))
            
            elif (opcion == 5):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('aceitunas',tamano))
            
            elif (opcion == 6):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('pepperoni',tamano))
            
            elif (opcion == 7):
                self.menu_crear_combo4(dia, tamano, precio_base, ingredienteController.getIngredienteIdByTamano('salchichon',tamano))
            
            break
    
    def menu_crear_combo4(self, dia, tamano, precio_base, fk_ingrediente):
        ingredienteController = database.IngredienteController(self.conn)
        ingrediente = ingredienteController.getIngredienteById(fk_ingrediente[0])
        print("ID DEL INGREDIENTE2: ",fk_ingrediente[0][0])
        while True:
            print("\t\t---- Creando combo del día 4/4 ----")
            print("Seleccione el descuento (número entero) de la pizza ", tamano, "con ", ingrediente[0][0], " a ofertar el día ", dia)
            print("Debe estar entre 10 y 90")

            descuento = self.validate_Entry4()

            comboController = database.ComboController(self.conn)
            comboController.createCombo(dia, fk_ingrediente[0][0], tamano, precio_base, descuento)
            break

    def validate_Entry(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry < 0) or (entry > 8):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")
    
    def validate_Entry2(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry < 1) or (entry > 3):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")

    def validate_Entry3(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry < 1) or (entry > 7):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")
    
    def validate_Entry4(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry < 10) or (entry > 90):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")

    def cls(self, num): 
        print ("\n" * num)
