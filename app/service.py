"""
Сервисный слой - бизнес-логика складского учета.
"""
from typing import List, Generator
from app.models import Item
from app.repository import InventoryRepository
from app.exceptions import ItemNotFoundError, InsufficientStockError

class InventoryService:
    """Сервис для работы с товарами."""

    def __init__(self, repository: InventoryRepository) -> None:
        self._repo = repository 

    def get_all_items(self) -> List[Item]:
        """Возвращает все товары."""
        return self._repo.get_all()

    def get_item_by_id(self, item_id: str) -> Item:
        """Возвращает товар по id."""
        return self._repo.get_by_id(item_id)

    def receive(self, item_id: str, name: str, category: str,
                price: float, quantity: int) -> Item:
        """Принимает товар на склад."""
        try:
            existing = self._repo.get_by_id(item_id)
            #Если товар уже есть - увеличиваем количество
            updated = Item(
                id=existing.id,
                name=name.strip() or existing.name,
                category=category.strip() or existing.category,
                price=price if price > 0 else existing.price,
                quantity=existing.quantity + quantity
            )
            self._repo.update(updated)
            return updated
        except ItemNotFoundError:
            #Если товара нет - создаем новый
            new_item = Item(
                id=item_id,
                name=name,
                category=category,
                price=price,
                quantity=quantity
            )
            self._repo.add(new_item)
            return new_item

    def ship(self, item_id: str, quantity: int) -> Item:
        """Отгружает товар со склада."""
        item = self._repo.get_by_id(item_id)
        if item.quantity < quantity:
            raise InsufficientStockError(
                f"Недостаточно товара '{item.name}': запрошено {quantity}, в наличии {item.quantity}"
            )
        updated = Item(
            id=item.id,
            name=item.name,
            category=item.category,
            price=item.price,
            quantity=item.quantity - quantity
        )
        self._repo.update(updated)
        return updated

    #Поиск генераторами

    def find_by_category(self, category: str) -> Generator[Item, None, None]:
        """Ищет товары по категории."""
        cat_lower = category.lower()
        for item in self._repo.get_all():
            if item.category.lower() == cat_lower:
                yield item

    def find_by_name(self, keyword: str) -> Generator[Item, None, None]:
        """Ищет товары по названию."""
        if not keyword:
            return
        kw_lower = keyword.lower()
        for item in self._repo.get_all():
            if kw_lower in item.name.lower():
                yield item

    def find_low_stock(self, threshold: int = 5) -> Generator[Item, None, None]:
        """Ищет товары с количеством меньше порога."""
        for item in self._repo.get_all():
            if item.quantity < threshold:
                yield item