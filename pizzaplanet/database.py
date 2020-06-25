import sqlite3
import string
from sqlite3 import Error


def createConnection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return conn


def createTables(conn):
    sqls = list()

    sql1 = """CREATE TABLE IF NOT EXISTS Cliente (
                    id_Cliente INTEGER PRIMARY KEY ,
                    name TEXT NOT NULL,
                    last_Name TEXT NOT NULL,
                    cedula TEXT);"""
    sqls.append(sql1)

    sql2 = """CREATE TABLE IF NOT EXISTS Ingrediente (
                    id_Ingrediente INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    tamano TEXT NOT NULL);"""
    sqls.append(sql2)

    sql3 = """CREATE TABLE IF NOT EXISTS Pedido(
                    id_Pedido INTEGER PRIMARY KEY,
                    fk_Cliente INTEGER NOT NULL,
                    pedido_Date TEXT NOT NULL,
                    total_Price INTEGER NOT NULL,
                    FOREIGN KEY (fk_Cliente)
                        REFERENCES Cliente(id_Cliente));"""
    sqls.append(sql3)

    sql4 = """CREATE TABLE IF NOT EXISTS Base(
                    id_Base INTEGER PRIMARY KEY,
                    fk_Pedido INTEGER NOT NULL,
                    tamano TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    FOREIGN KEY (fk_Pedido)
                        REFERENCES Pedido(id_Pedido));"""
    sqls.append(sql4)

    sql5 = """CREATE TABLE IF NOT EXISTS Pizza (
                    id_Pizza INTEGER PRIMARY KEY,
                    fk_Ingrediente INTEGER NOT NULL,
                    fk_Base INTEGER NOT NULL,
                    FOREIGN KEY (fk_Ingrediente)
                        REFERENCES Ingrediente(id_Ingrediente),
                    FOREIGN KEY (fk_Base)
                        REFERENCES Base(id_Base));"""
    sqls.append(sql5)

    sql6 = """CREATE TABLE IF NOT EXISTS Combo (
                    id_Combo INTEGER PRIMARY KEY,
                    dia TEXT NOT NULL,
                    fk_Ingrediente INTEGER NOT NULL,
                    tamano TEXT NOT NULL,
                    precio_base INTEGER NOT NULL,
                    descuento INTEGER NOT NULL,
                    FOREIGN KEY (fk_Ingrediente)
                        REFERENCES Ingrediente(id_Ingrediente));"""
    sqls.append(sql6)

    cursor = conn.cursor()
    for sql in sqls:
        cursor.execute(sql)
    cursor.close()


def insertIngredients(conn):
    sql = """SELECT name from Ingrediente;"""

    cursor = conn.cursor()
    cursor.execute(sql)
    response = cursor.fetchall()
    cursor.close()
    filled = len(response)
    if (filled):
        pass
    else:
        ingredienteC = IngredienteController(conn)
        ingredienteC.createIngrediente('jamon', 1.5, 'personal')
        ingredienteC.createIngrediente('jamon', 1.75, 'mediana')
        ingredienteC.createIngrediente('jamon', 2, 'familiar')
        ingredienteC.createIngrediente('champinones', 1.75, 'personal')
        ingredienteC.createIngrediente('champinones', 2.05, 'mediana')
        ingredienteC.createIngrediente('champinones', 2.5, 'familiar')
        ingredienteC.createIngrediente('pimenton', 1.5, 'personal')
        ingredienteC.createIngrediente('pimenton', 1.75, 'mediana')
        ingredienteC.createIngrediente('pimenton', 2, 'familiar')
        ingredienteC.createIngrediente('doble queso', 0.8, 'personal')
        ingredienteC.createIngrediente('doble queso', 1.3, 'mediana')
        ingredienteC.createIngrediente('doble queso', 1.7, 'familiar')
        ingredienteC.createIngrediente('aceitunas', 1.8, 'personal')
        ingredienteC.createIngrediente('aceitunas', 2.15, 'mediana')
        ingredienteC.createIngrediente('aceitunas', 2.6, 'familiar')
        ingredienteC.createIngrediente('pepperoni', 1.25, 'personal')
        ingredienteC.createIngrediente('pepperoni', 1.7, 'mediana')
        ingredienteC.createIngrediente('pepperoni', 1.9, 'familiar')
        ingredienteC.createIngrediente('salchichon', 1.6, 'personal')
        ingredienteC.createIngrediente('salchichon', 1.85, 'mediana')
        ingredienteC.createIngrediente('salchichon', 2.1, 'familiar')
        conn.commit()

        del ingredienteC


class ClienteController:

    def __init__(self, connection):
        self.__cursor = connection.cursor()

    def __del__(self):
        self.__cursor.close()

    def createCliente(self, name, lastName):
        sql = """INSERT INTO Cliente (name, last_Name)
             VALUES(?, ?);"""
        lowName = name.lower()
        lowLastName = lastName.lower()
        self.__cursor.execute(sql, (lowName, lowLastName))
        return self.__cursor.lastrowid


class IngredienteController:

    def __init__(self, connection):
        self.__cursor = connection.cursor()

    def __del__(self):
        self.__cursor.close()

    def createIngrediente(self, name, price, tamano):
        sql = """INSERT INTO Ingrediente (name, price, tamano)
             VALUES(?, ?, ?);"""
        lowName = name.lower()
        lowTamano = tamano.lower()
        self.__cursor.execute(sql, (lowName, price, lowTamano))
        return self.__cursor.lastrowid

    def getVentaIngredientes(self):
        sql = """SELECT i.name, COUNT(i.name), SUM(i.price) 
        FROM Ingrediente as i, Pizza as p WHERE p.fk_Ingrediente = i.id_Ingrediente GROUP BY i.name;"""
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows

    def getVentaIngredientesByDay(self, date):
        sql = """SELECT i.name, COUNT(i.name), SUM(i.price) 
        FROM Ingrediente as i, Pizza as p, Base as b, Pedido as a
        WHERE p.fk_Ingrediente = i.id_Ingrediente and p.fk_Base = b.id_Base and b.fk_Pedido = a.id_Pedido 
        and a.pedido_Date = ?
        GROUP BY i.name;"""
        self.__cursor.execute(sql, (date,))
        rows = self.__cursor.fetchall()
        return rows

    def getPopularIngredientes(self):
        sql = """SELECT i.name, COUNT(i.name), SUM(i.price) 
        FROM Ingrediente as i, Pizza as p WHERE p.fk_Ingrediente = i.id_Ingrediente GROUP BY i.name ORDER BY COUNT(i.name) DESC;"""
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows
    
    def getIngredienteIdByTamano(self, name, tamano):
        sql = """SELECT id_Ingrediente from Ingrediente where name = ? and tamano = ?;"""
        self.__cursor.execute(sql, (name,tamano))
        row = self.__cursor.fetchall()
        return row

    def getIngredienteById(self, id_ingrediente):
        sql = """SELECT name from Ingrediente where id_Ingrediente = ?;"""
        self.__cursor.execute(sql, (id_ingrediente))
        row = self.__cursor.fetchall()
        return row

class PedidoController:

    def __init__(self, connection):
        self.__cursor = connection.cursor()

    def __del__(self):
        self.__cursor.close()

    def createPedido(self, fk_Cliente, pedido_Date):
        sql = """INSERT INTO Pedido (fk_Cliente, pedido_Date, total_price)
             VALUES(?, ?, ?);"""
        self.__cursor.execute(sql, (fk_Cliente, pedido_Date, 0))
        return self.__cursor.lastrowid
    
    def getVentaTotal(self):
        sql = """SELECT SUM(total_price) FROM Pedido;"""
        self.__cursor.execute(sql)
        row = self.__cursor.fetchall()
        return row

    def getVentaTotalByDay(self, date):
        sql = """SELECT SUM(total_price) FROM Pedido WHERE pedido_Date = ?;"""
        self.__cursor.execute(sql, (date,))
        row = self.__cursor.fetchall()
        return row

    def getDays(self):
        sql = """SELECT DISTINCT pedido_Date FROM Pedido ORDER BY pedido_Date ASC;"""
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows

    def getAllPedidos(self):
        sql = """SELECT p.pedido_Date, c.name, c.last_name, COUNT(b.fk_Pedido), p.total_Price
        FROM Pedido as p, Cliente as c, Base as b
        WHERE c.id_Cliente = p.fk_Cliente and p.id_Pedido = b.fk_Pedido
        GROUP BY b.fk_Pedido
        ORDER BY pedido_Date ASC, c.name ASC;"""
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows   


class PizzaController:

    def __init__(self, connection, basePrice=0, pedidoPrice=0):
        self.__cursor = connection.cursor()
        self.basePrice = basePrice
        self.pedidoPrice = pedidoPrice

    def __del__(self):
        self.__cursor.close()

    def createPizza(self, fk_Pedido, tamano):
        lowTamano = tamano.lower()
        if('personal' in lowTamano):
            price = 10
        elif (lowTamano in lowTamano):
            price = 15
        else:
            price = 20
        sql = """INSERT INTO Base (fk_Pedido, tamano, price)
             VALUES(?, ?, ?);"""
        self.__cursor.execute(sql, (fk_Pedido, lowTamano, price))
        self.basePrice = price
        self.pedidoPrice = price
        return self.__cursor.lastrowid

    def getPedidoIdFromBase(self, id_Base):
        sql = """SELECT b.fk_Pedido FROM Base as b
             WHERE b.id_Base = ?;"""
        self.__cursor.execute(sql, (id_Base,))
        return self.__cursor.fetchall()

    def updatePedidoPrice(self, id_Pedido, precio):
        sql = """UPDATE Pedido SET total_price = ?
             WHERE id_Pedido = ?;"""
        self.__cursor.execute(sql, (precio, id_Pedido))
        return True

    def updateBasePrice(self, id_Base, precio):
        sql = """UPDATE Base SET price = ?
             WHERE id_Base = ?;"""
        self.__cursor.execute(sql, (precio, id_Base))
        return True

    def getIngredienteByTamano(self, name, tamano):
        lowName = name.lower()
        lowTamano = tamano.lower()

        if lowName in ['champiñón', 'champiñon', 'champiñones']:
            lowName = 'champinones'
        if lowName in ['pimentón', 'pimentones']:
            lowName = 'pimenton'
        if lowName in ['salchichón', 'salchichones']:
            lowName = 'salchichon'
        if lowName in ['jamón', 'jamones']:
            lowName = 'jamon'

        sql = """SELECT i.price, i.id_Ingrediente FROM Ingrediente as i
             WHERE i.name = ? AND i.tamano = ?;"""
        self.__cursor.execute(sql, (lowName, lowTamano,))
        return self.__cursor.fetchall()

    def addPizzaIngrediente(self, fk_Base, name, tamano):
        ingrediente = self.getIngredienteByTamano(name, tamano)
        ingredientePrice = ingrediente[0][0]
        idIngrediente = ingrediente[0][1]
        sql = """INSERT INTO Pizza (fk_Ingrediente, fk_Base)
             VALUES(?, ?);"""
        self.__cursor.execute(sql, (idIngrediente, fk_Base))
        id_Pedido = self.getPedidoIdFromBase(fk_Base)
        self.basePrice += ingredientePrice
        self.pedidoPrice += self.basePrice
        self.updateBasePrice(fk_Base, self.basePrice)
        self.updatePedidoPrice(id_Pedido[0][0], self.pedidoPrice)
        return True

    def getVentaPizzasTamaño(self):
        sql = """SELECT tamano, COUNT(tamano) FROM Base GROUP BY tamano;"""
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()
        return rows

    def getVentaPizzasTamañoByDay(self, date):
        sql = """SELECT b.tamano, COUNT(b.tamano) FROM Base as b, Pedido as p WHERE b.fk_Pedido = p.id_Pedido and p.pedido_Date = ? GROUP BY tamano;"""
        self.__cursor.execute(sql, (date,))
        rows = self.__cursor.fetchall()
        return rows

class ComboController:
    def __init__(self, connection):
        self.__cursor = connection.cursor()

    def __del__(self):
        self.__cursor.close()
    
    def createCombo(self, dia, fk_ingrediente, tamano, precio_base, descuento):
        print("Dia: ",dia)
        print("FK: ",fk_ingrediente)
        print("Tamano: ", tamano)
        print("Precio base: ",precio_base)
        print("descuento: ", descuento)
        sql = """INSERT INTO Combo (dia, fk_Ingrediente, tamano, precio_base, descuento)
             VALUES(?, ?, ?, ?, ?);"""
        self.__cursor.execute(sql, (dia, fk_ingrediente, tamano, precio_base, descuento))
        
    def getCombo(self, dia):
        lowDia = dia.lower()
        sql = """SELECT DISTINCT c.dia, c.tamano, c.precio_base, c.descuento, i.name, i.price FROM Combo as c, Base as b, Ingrediente as i
             WHERE c.dia = ? and c.fk_Ingrediente = i.id_Ingrediente ORDER BY c.id_Combo desc;"""
        self.__cursor.execute(sql, (lowDia,))
        rows = self.__cursor.fetchall()
        return rows

def main():
    database = "pizzaplanet.db"
    conn = createConnection(database)
    with conn:
        createTables(conn)
        insertIngredients(conn)
