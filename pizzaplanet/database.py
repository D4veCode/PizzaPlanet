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

    cursor = conn.cursor()
    for sql in sqls:
        cursor.execute(sql)
    cursor.close()


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
        self.__cursor.execute(sql, ( lowName, price, lowTamano))
        return self.__cursor.lastrowid


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


class PizzaController:
    
    def __init__(self, connection, basePrice = 0, pedidoPrice = 0):
        self.__cursor = connection.cursor()
        self.basePrice = basePrice
        self.pedidoPrice = pedidoPrice

    def __del__(self):
        self.__cursor.close()

    def createPizza(self, fk_Pedido, tamano):
        lowTamano = tamano.lower()
        sql = """INSERT INTO Base (fk_Pedido, tamano, price)
             VALUES(?, ?, ?);"""
        self.__cursor.execute(sql, (fk_Pedido, lowTamano, 0))
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
        sql = """SELECT i.price, i.id_Ingrediente FROM Ingrediente as i
             WHERE i.name = ? AND i.tamano = ?;"""
        self.__cursor.execute(sql, (lowName, lowTamano))
        return self.__cursor.fetchall()

    def addPizzaIngrediente(self, fk_Base, name, tamano):
        ingrediente = self.getIngredienteByTamano(name,tamano)
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
        

def main():
    database = "pizzaplanet.db"
    conn = createConnection(database)
    with conn:
        pedidoc = PizzaController(conn)
        idPedido = pedidoc.addPizzaIngrediente(1,'cebolla', 'personal')
        idPedido = pedidoc.addPizzaIngrediente(1,'tocineta', 'personal')
        idPedido = pedidoc.addPizzaIngrediente(1,'tomate', 'personal')
        print(idPedido)
        del pedidoc

if __name__ == "__main__":
    main()
