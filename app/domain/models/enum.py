from enum import Enum

class UserRol(str, Enum):
    CUSTOMER="customer"
    ADMIN="admin"
    
class OrderStatus(str, Enum):
    PENDING="pending"
    PAID="paid"
    SHIPPED="shipped"
    DELIVERED="delivered"
    CANCELED="canceled"