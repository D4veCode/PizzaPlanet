# -*- coding: utf-8 -*-
import os
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
                            print(linea)
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
            print(ped.nombrecliente)
            print(ped.fecha)
        else:
            ped.pizzas.append(data)
            print(data)

    def guardarPedido(self, ped):
        pass

class Pedido:
    pizzas = []
    nombrecliente = ''
    fecha = ''


