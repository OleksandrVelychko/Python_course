from datetime import datetime

# Задача4
# Необходимо создать модели работы со складскими запасами товаров и процесса оформления заказа этих товаров.
# Список требований:
# 1) Создайте товар с такими свойствами, как имя(name), подробные сведения(description or details),
# количество на складе(quantity), доступность(availability), цена(price).
# 2) Добавить товар на склад
# 3) Удалить товар со склада
# 4) Распечатать остаток товара по его имени
# 5) Распечатать остаток всех товаров
# 6) Товар может принадлежать к категории
# 7) Распечатать список товаров с заданной категорией
# 8) Корзина для покупок, в которой может быть много товаров с общей ценой.
# 9) Добавить товары в корзину (вы не можете добавлять товары, если их нет в наличии)
# 10) Распечатать элементы корзины покупок с ценой и общей суммой
# 11) Оформить заказ и распечатать детали заказа по его номеру
# 12) Позиция заказа, созданная после оформления заказа пользователем.
# Он будет иметь идентификатор заказа(order_id), дату покупки(date_purchased), товары(items), количество(quantity)
# 13) После оформления заказа количество товара уменьшается на количество товаров из заказа.

# Добавить к этой задаче дескриптор для аттрибута цена.
# При назначении цены товара будет автоматически добавлен НДС 20%
# При получении цены товара, цена возврщается уже с учетом НДС


class Order:
    orders = {}
    processed_orders = {}

    def __init__(self, shop_cart):
        self.order_id = 'Order_ID_'+str(id(self))
        self.order_date = datetime.today().strftime('%Y-%m-%d')
        self.items = shop_cart.items_to_buy
        self.status = 'New'
        self.position = None
        print(f'\nOrder created with id {self.order_id} and date {self.order_date}')
        print(f'Order contains:\n{self.items}')
        Order.orders[self.order_id] = {'Date: ': self.order_date, 'Status': self.status, 'Position': self.position,
                                       'Items: ': self.items}
        print(Order.orders)

    def process_order_and_print_details(self):
        for k, v in self.items.items():
            if Warehouse.wgoods.get(k)['Quantity'] < v:
                raise ValueError(
                    f"Order {self.order_id}: Requested quantity {v} is not available for {k}")

        for k, v in self.items.items():
            Warehouse.wgoods.get(k)['Quantity'] -= v

        if not Order.processed_orders:
            self.position = 1
        else:
            self.position = len(Order.processed_orders) + 1
        Order.processed_orders[self.order_id] = self.position
        self.status = 'Processed'
        for k, v in Order.orders.items():
            if k == self.order_id:
                v['Position'] = self.position
        return print(f'\nOrder {self.order_id} was processed. Details:\n{Order.orders[self.order_id]}')


class ShoppingCart:
    def __init__(self, g_name, g_quantity):
        if not Warehouse.is_available(self, g_name):
            raise ValueError(f"No more {g_name} available")
        self.items_to_buy = {g_name: g_quantity}
        self.id = 'ShopCart_ID_'+str(id(self))

    def add_goods_to_cart(self, item, r_quant):
        stock = Warehouse.wgoods.get(item)['Quantity']
        print('\nAdding  to cart: ', item, r_quant)
        if not Warehouse.is_available(self, item):
            raise ValueError(f"No more {item} available")
        elif stock < r_quant:
            raise ValueError(
                f"Requested quantity not available: {r_quant} requested while {stock} only available")
        else:
            # Warehouse.wgoods.get(item)['Quantity'] -= r_quant # removing this part to order processing
            if item in self.items_to_buy.keys():
                self.items_to_buy[item] += r_quant
            else:
                self.items_to_buy[item] = r_quant

    def print_goods_from_cart(self):
        self.total_price = 0
        for item in self.items_to_buy.keys():
            self.total_price += Warehouse.wgoods[item].get('Price')*self.items_to_buy[item]
        return print(f'Shopping cart {self.id} contains: {self.items_to_buy} with total price: {self.total_price:.2f}')


class InvalidPriceException(Exception):
    pass


class PriceDescriptor:
    def __get__(self, instance, owner):
        return self.price

    def __set__(self, instance, value):
        VAT = 20  # tax specified in %
        if value >= 0:
            self.price = value * (1 + VAT / 100)
        else:
            raise InvalidPriceException(f'Specified price is not valid: {value}')


class Goods:
    price = PriceDescriptor()

    def __init__(self, name, category, description, quantity, price):
        self.name = name
        self.category = category
        self.descr = description
        self.quantity = quantity
        self.price = price
        Warehouse.add_goods_to_warehouse(self)

    def __repr__(self):
        return f'Name: {self.name} \ncategory: {self.category} \nquantity: {self.quantity}' \
               f'\ndescription: {self.descr} \nprice: {self.price:.2f} (including VAT)'


class Warehouse:
    wgoods = {}

    def is_available(self, item):
        self.item = Warehouse.wgoods.get(item)
        return self.item['Quantity'] > 0

    def add_goods_to_warehouse(self):
        Warehouse.wgoods[self.name] = {'Category': self.category, 'Descr': self.descr, 'Quantity': self.quantity,
                                       'Price': self.price}

    @staticmethod
    def remove_goods_from_warehouse(name):
        print(f'\nDeleting {name} from warehouse')
        try:
            del Warehouse.wgoods[name]
        except KeyError:
            print(f'Trying to remove non-existent item from the warehouse: {name}')

    @staticmethod
    def print_remaining_goods_by_name(name):
        print(f'\nItems by name {name}:')
        for k, v in Warehouse.wgoods.items():
            if k == name:
                print(k, v)

    @staticmethod
    def print_all_remaining_goods():
        print(Warehouse.wgoods)

    @staticmethod
    def print_goods_by_category(cat):
        print(f'\nItems in category {cat}:')
        for k, v in Warehouse.wgoods.items():
            if v['Category'] == cat:
                print(k, v)


item_1 = Goods('Huawei', 'Phones', 'some new model', 5, 500)
print(f'\nItem 1:\n{item_1}')
item_2 = Goods('IPhone', 'Phones', '12 Pro', 4, 1300)
print(f'\nItem 1:\n{item_2}')
item_3 = Goods('Bread', 'Food', 'Gluten free', 10, 1.4)
print(f'\nItem 1:\n{item_3}')
item_4 = Goods('Orange juice', 'Food', 'Fresh juice', 15, 2)
print(f'\nItem 1:\n{item_4}')

#print(f'\nWarehouse contains:\n{Warehouse.wgoods}\n')
#print(f'\n\nPrint __phones__:\n{Warehouse.print_goods_by_category("Phones")}')

sc1 = ShoppingCart('Huawei', 3)
sc2 = ShoppingCart('Huawei', 1)
sc1.add_goods_to_cart('IPhone', 1)
sc1.add_goods_to_cart('IPhone', 1)
sc1.add_goods_to_cart('IPhone', 1)
sc2.add_goods_to_cart('Bread', 2)
sc1.print_goods_from_cart()
sc2.print_goods_from_cart()

#Warehouse.print_goods_by_category("Phones")
#Warehouse.print_all_remaining_goods()
#Warehouse.remove_goods_from_warehouse('Orange juice')
Warehouse.print_all_remaining_goods()
#Warehouse.print_remaining_goods_by_name('IPhone')
order_1 = Order(sc1)
order_2 = Order(sc2)
order_1.process_order_and_print_details()
Warehouse.print_all_remaining_goods()
sc2.add_goods_to_cart('IPhone', 1)
sc3 = ShoppingCart('IPhone', 1)
order_3 = Order(sc3)
order_3.process_order_and_print_details()
# to see exception raised as stock is depleted after processing previous orders:
#order_2.process_order_and_print_details()