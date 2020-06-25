# -*- coding: utf-8 -*-
import os
from .database import * 
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
        except Exception as e:
            print('Ruta no valida')
                    
    def asignarData(self, data, ped):
        if data[0] not in ['personal', 'mediana', 'familiar']:
            ped.nombrecliente = data[0]
            ped.fecha = data[1]
        else:
            ped.pizzas.append(data)

    def guardarPedido(self, ped):
        db = createConnection('database.db')
        client = ClienteController(db)
        name = ped.nombrecliente.split(' ')
        idCliente = client.createCliente(name[0], name[1])
        pedido = PedidoController(db)
        idPedido = pedido.createPedido(idCliente, ped.fecha)
        for pizza in ped.pizzas:
            pizzaController = PizzaController(db)
            pizza = list(pizza)
            idBase = pizzaController.createPizza(idPedido, pizza[0])
            tam = pizza[0]
            pizza.pop(0)
            for item in pizza:
                pizzaBase.addPizzaIngrediente(idBase, item, tam)

class Pedido:
    def __init__(self, nombrecliente='', fecha='', pizzas=[])
        self.nombrecliente = nombrecliente
        self.fecha = fecha
        self.pizzas = pizzas
