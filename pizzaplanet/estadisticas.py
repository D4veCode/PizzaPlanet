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
            print("4)Ventas Totales")
            print("5)Pizzas e ingredientes vendidos por dia")
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
            self.csl(2)
            
        input("Gracias por su atencion hasta luego")


    def option_5(self):
        #self.dataTest()

        baseController = database.PizzaController(self.conn)
        pedidoController = database.PedidoController(self.conn)
        ingredienteController = database.IngredienteController(self.conn)

        days = pedidoController.getDays()

        for day in days:
            today = day[0]
            pizzas = baseController.getVentaPizzasTamañoByDay(today)
            ventaTotal = pedidoController.getVentaTotalByDay(today)
            ingredientes = ingredienteController.getVentaIngredientesByDay(today)

            self.cls(1)
            print("PEDIDO")
            print("Fecha: {}".format(today))
            print("Venta Total: {}".format(ventaTotal[0][0]))

            print("Ventas por pizza (sin incluir adicionales)")
            for row in pizzas:
                if (row[0] ==   "personal"):
                    price = 10
                elif (row[0] == "mediana"):
                    price = 15
                elif (row[0] == "familiar"):
                    price = 20
                total = row[1]*price
                print(row[0] + "  |  " + str(row[1]) + "  |  " + str(total))
            print("Ventas por Ingrediente:")
            for row in ingredientes:
                print(row[0] + "  |  " + str(row[1]) + "  |  " + str(row[2]))


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
        clienteController = database.ClienteController(self.conn)

        idc = clienteController.createCliente("Fernando", "Rodriguez")

        idp = pedidoController.createPedido(idc,"23/04/2020")
        baseController.createPizza(idp,"personal")
        baseController.createPizza(idp,"personal")
        baseController.createPizza(idp,"familiar")
        baseController.createPizza(idp,"mediana")
        baseController.createPizza(idp,"mediana")
        baseController.updatePedidoPrice(idp,110)

        idp = pedidoController.createPedido(idc,date.today().strftime("%d/%m/%Y"))
        baseController.createPizza(idp,"familiar")
        baseController.createPizza(idp,"familiar")
        baseController.createPizza(idp,"familiar")
        baseController.createPizza(idp,"mediana")
        baseController.createPizza(idp,"mediana")
        baseController.updatePedidoPrice(idp,90)

        idp = pedidoController.createPedido(idc,"23/04/2020")
        baseController.createPizza(idp,"personal")
        baseController.createPizza(idp,"personal")
        baseController.createPizza(idp,"familiar")
        baseController.createPizza(idp,"mediana")
        baseController.createPizza(idp,"mediana")
        baseController.updatePedidoPrice(idp,110)

