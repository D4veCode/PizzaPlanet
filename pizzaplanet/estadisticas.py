from pizzaplanet import database
from datetime import date

class Estadisticas:

    conn = database.createConnection("pizzaplanet.db")

    def main(self):
        while True:
            print("Que reporte desea visualizar?")
            print("1)Ingredientes mas populares.")
            print("2)Historial de ventas")
            print("3)Ventas por producto")
            print("4)Ventas por producto filtrado por dia")
            print("0)Exit")

            option = self.validate_Entry()

            if(option == 1):
                self.option_1()
            elif(option == 2):
                self.option_2()
            elif(option == 3):
                self.option_3()
            elif(option == 4):
                self.option_4()
            elif(option == 0):
                break
            self.cls(2)
            

    def option_1(self):
        ingredienteController = database.IngredienteController(self.conn)
        ingredientes = ingredienteController.getPopularIngredientes()
        self.cls(1)
        print("Los 5 ingredientes mas populares y numero de usos :")
        cont = 1
        for row in ingredientes:
            if cont < 6:
                print(row[0] + "  |  " + str(row[1]))
            else:
                break
    
    def option_2(self):
        pedidoController = database.PedidoController(self.conn)
        pedidos = pedidoController.getAllPedidos()
        for pedido in pedidos:
            self.cls(0)
            print("PEDIDO:")
            print("Fecha de pedido: {}".format(pedido[0]))
            print("Nombre cliente:  {} {}".format(pedido[1],pedido[2]))
            print("Numero de pizzas ordenadas: {}".format(pedido[3]))
            print("Monto de factura: {}".format(pedido[4]))
            



    def option_3(self):
        baseController = database.PizzaController(self.conn)
        pedidoController = database.PedidoController(self.conn)
        ingredienteController = database.IngredienteController(self.conn)

        today = date.today().strftime("%d/%m/%Y")
        pizzas = baseController.getVentaPizzasTamaño()
        ventaTotal = pedidoController.getVentaTotal()
        ingredientes = ingredienteController.getVentaIngredientes()

        self.cls(1)
        print("Hasta la fecha de hoy: {}".format(today))
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

    def option_4(self):
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
            if (entry < 0) or (entry > 5):
                self.cls(25)
                print("Opcion invalida!! Ingrese una opcion valida")
            else:
                return entry
        except ValueError:
            self.cls(25)
            print("Opcion invalida!! Ingrese una opcion valida")


    def cls(self, num): 
        print ("\n" * num)


