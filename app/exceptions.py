"""Пользовательские исключения для системы учета товаров."""

class InventoryError(Exception):
    """Базовый класс для всех исключений инвентаризации."""
    pass

class ItemNotFoundError(InventoryError):
    """Товар с указанным идентификатором не найден."""
    pass

class InsufficientStockError(InventoryError):
    """Недостаточное количество товара на складе."""
    pass

class InvalidItemDataError(InventoryError):
    """Некорректные данные товара (отрицательная цена, пустое имя и т.п.)."""
    pass

class InventoryStorageError(InventoryError):
    """Ошибка при работе с хранилищем (чтение/запись JSON)."""
    pass