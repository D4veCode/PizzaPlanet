from pizzaplanet import estadisticas
from pizzaplanet import combo
from pizzaplanet import archivemanager
from pizzaplanet import database


class Main:
    def menu(self):
        database.main()
        while True:
            self.cls(25)
            print("Bienvenido al PizzaPlanet, esperamos su orden")
            print("1)Ver Combo del dia.")
            print("2)Realizar un reporte")
            print("3)Cargar Archivos")
            print("0)Exit")

            option = self.Validate_Entry()

            if(option == 1):
                self.cls(25)
                c = combo.Combo()
                c.main()

            elif(option == 2):
                self.cls(25)
                e = estadisticas.Estadisticas()
                e.main()

            elif(option == 3):
                self.cls(25)
                fileName = input("Introduzca ruta o nombre de archivo \n (si el archivo esta en la mismo directorio, coloque solo el nombre. \n Si el archivo esta en otra ruta coloque la ruta con el nombre del archivo Ej: /path/to/dir/nombrearchivo):\n ")
                arch = archivemanager.Archive(fileName)
                arch.openFile()

            elif(option == 0):
                break

        print("Gracias por su atencion hasta luego")

    def Validate_Entry(self):
        """Validate files inputs """
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry < 0) or (entry > 3):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")

    def cls(self, num):
        print ("\n" * num)
