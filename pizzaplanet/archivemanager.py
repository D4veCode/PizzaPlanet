# -*- coding: utf-8 -*-
import os
from pizzaplanet import database as db
class Archive:
    conn = db.createConnection("pizzaplanet.db")
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
                        pedido.pizzas.clear()
                        valido = True
                    elif valido == True:
                        linea = line.strip().split(';')
                        if len(linea[0]) != 0:
                            data = tuple(linea)
                            self.asignarData(data, pedido)
                        else:
                            print('Pedido invalido!')
                            valido = False
            
            print('Archivo leído con éxito! ')
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
        client = db.ClienteController(self.conn)
        name = ped.nombrecliente.split(' ')
        idCliente = client.createCliente(name[0], name[1])
        self.conn.commit()
        pedido = db.PedidoController(self.conn)
        idPedido = pedido.createPedido(idCliente, ped.fecha)
        self.conn.commit()
        for pizza in ped.pizzas:
            pizzaController = db.PizzaController(self.conn)
            pizza = list(pizza)
            idBase = pizzaController.createPizza(idPedido, pizza[0])
            self.conn.commit()
            tam = pizza[0]
            pizza.pop(0)
            for item in pizza:
                pizzaController.addPizzaIngrediente(idBase, item, tam)
                self.conn.commit()
            
class Pedido:
    def __init__(self, nombrecliente='', fecha='', pizzas=[]):
        self.nombrecliente = nombrecliente
        self.fecha = fecha
        self.pizzas = pizzas
