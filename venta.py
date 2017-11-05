class Item(object):
    def __init__(self, cliente, producto, cantidad, precio):        
        self.producto = producto
        self.cliente = cliente
        self.cantidad = cantidad
        self.precio = precio