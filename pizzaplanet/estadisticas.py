from pizzaplanet import database
from datetime import date

class Estadisticas:

    conn = database.createConnection("pizzaplanet.db")

    def main(self):
        while True:
            print("Que reporte desea visualizar?")
            print("1)Ingredientes mas utilizados.")
            print("2)Ingredientes con mas ventas")
            print("3)Historial de ventas")
            print("4)Usuarios con mas compras")
            print("5)Pizzas mas vendidas por tamaño")
            print("0)Exit")

            option = self.validate_Entry()

            if(option == 1):
                break
            elif(option == 2):
                break
            elif(option == 3):
                break
            elif(option == 4):
                break
            elif(option == 5):
                self.option_5()
            elif(option == 0):
                break
            
        input("Gracias por su atencion hasta luego")


    def validate_Entry(self):
        entry = input("Por favor ingrese la opcion: ")
        try:
            entry = int(entry)
            if (entry <= 0) or (entry > 5):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")


    def cls(self, num): 
        print ("\n" * num)
    
    def dataTest(self):
        baseController = database.PizzaController(self.conn)
        pedidoController = database.PedidoController(self.conn)

        pedidoController.createPedido(1,date.today().strftime("%d/%m/%Y"))

        baseController.createPizza(2,"familiar")
        baseController.createPizza(2,"familiar")
        baseController.createPizza(2,"familiar")
        baseController.createPizza(2,"mediana")
        baseController.createPizza(2,"mediana")

        baseController.updatePedidoPrice(2,90)



    def option_5(self):
        baseController = database.PizzaController(self.conn)
        pedidoController = database.PedidoController(self.conn)
        ingredienteController = database.IngredienteController(self.conn)

        self.dataTest()

        today = date.today().strftime("%d/%m/%Y")
        pizzas = baseController.getVentaPizzasTamaño()
        ventaTotal = pedidoController.getVentaTotal()
        ingredientes = ingredienteController.getVentaIngredientes()

        self.cls(25)
        print("Fecha: {}".format(today))
        print("Venta Total: {}".format(ventaTotal[0][0]))

        print("Ventas por pizza (sin incluir adicionales)")
        for row in pizzas:
            if (row[0] ==   "personal"):
                n = 10
            elif (row[0] == "mediana"):
                n = 15
            elif (row[0] == "familiar"):
                n = 20
            total = row[1]*n
            print(row[0] + "  |  " + str(row[1]) + "  |  " + str(total))

        print("Ventas por Ingrediente:")
        for row in ingredientes:
            print(row[0] + "  |  " + str(row[1]) + "  |  " + str(row[2]))


