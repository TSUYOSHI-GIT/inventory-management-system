"""Модели данных для товара"""
from dataclasses import dataclass
from app.exceptions import InvalidItemDataError

@dataclass
class Item:
    """Товар на складе"""
    id: str
    name: str
    category: str
    price: float
    quantity: int

    def __post_init__(self) -> None:
        """Валидация данных после инициализации"""
        self.name = self.name.strip()
        if not self.name:
            raise InvalidItemDataError("Название товара не может быть пустым")
        if self.price < 0:
            raise InvalidItemDataError(
                f"Цена товара '{self.name}' не может быть отрицательной: {self.price}"
            )
        if self.quantity < 0:
            raise InvalidItemDataError(
                f"Количество товара '{self.name}' не может быть отрицательным: {self.quantity}"
            )

    @property
    def total_value(self) -> float:
        """Общая стоимость позиции на складе"""
        return self.price * self.quantity