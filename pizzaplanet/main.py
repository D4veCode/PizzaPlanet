from pizzaplanet import estadisticas

class Main:
    def menu(self):
        while True:
            print("Bienvenido al PizzaPlanet, esperamos su orden")
            print("1)Registrar pedido.")
            print("2)Realizar un reporte")
            print("3)Cargar Archivos")
            print("0)Exit")

            option = self.Validate_Entry()

            if(option == 1):
                break
            elif(option == 2):
                self.cls(25)
                e = estadisticas.Estadisticas()
                e.main()
                break
            elif(option == 3):
                break
            elif(option == 0):
                break
        input("Gracias por su atencion hasta luego")


    def Validate_Entry(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry <= 0) or (entry > 3):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")


    def cls(self, num): 
        print ("\n" * num)