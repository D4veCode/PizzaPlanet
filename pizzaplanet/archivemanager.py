# -*- coding: utf-8 -*-
import os
from pizzaplanet import database as db
class Archive:
    def __init__(self, fileName):
        self.fileName = '{}.pz'.format(fileName)

    def openFile(self):
        try:
            with open(self.fileName, 'r') as f:
                valido = True
                for line in f:
                    if line.strip() == 'COMIENZO_PEDIDO':
                        pedido = Pedido()
                    elif line.strip() == 'FIN_PEDIDO':
                        if valido == True:
                            self.guardarPedido(pedido)
                        del pedido
                        valido = True
                    elif valido == True:
                        linea = line.strip().split(';')
                        if len(linea[0]) != 0:
                            data = tuple(linea)
                            self.asignarData(data, pedido)
                        else:
                            print('Pedido invalido!')
                            valido = False
        except IOError as e:
            print('Ruta no valida o no existe archivo con ese nombre')
        except Exception as err:
            print('Error.', str(err))
                    
    def asignarData(self, data, ped):
        if data[0] not in ['personal', 'mediana', 'familiar']:
            ped.nombrecliente = data[0]
            ped.fecha = data[1]
        else:
            ped.pizzas.append(data)

    def guardarPedido(self, ped):
        conn = db.createConnection('pizzaplanet.db')
        client = db.ClienteController(conn)
        name = ped.nombrecliente.split(' ')
        idCliente = client.createCliente(name[0], name[1])
        pedido = db.PedidoController(conn)
        idPedido = pedido.createPedido(idCliente, ped.fecha)
        for pizza in ped.pizzas:
            pizzaController = db.PizzaController(conn)
            pizza = list(pizza)
            print(pizza)
            idBase = pizzaController.createPizza(idPedido, pizza[0])
            tam = pizza[0]
            pizza.pop(0)
            for item in pizza:
                print(item)
                pizzaController.addPizzaIngrediente(idBase, item, tam)

class Pedido:
    def __init__(self, nombrecliente='', fecha='', pizzas=[]):
        self.nombrecliente = nombrecliente
        self.fecha = fecha
        self.pizzas = pizzas
