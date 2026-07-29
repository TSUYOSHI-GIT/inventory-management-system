"""
Тесты для модели Item.
"""
import pytest
from app.models import Item
from app.exceptions import InvalidItemDataError


#Тест на создание товара
def test_create_item():
    """Проверяет, что товар создаётся с правильными полями."""
    item = Item(id="1", name="Клавиатура", category="Электроника", price=5000.0, quantity=10)
    assert item.id == "1"
    assert item.name == "Клавиатура"
    assert item.category == "Электроника"
    assert item.price == 5000.0
    assert item.quantity == 10


#Тест на вычисление общей стоимости
def test_total_value():
    """Проверяет расчет общей стоимости позиции."""
    item = Item(id="2", name="Мышь", category="Аксессуары", price=1500.0, quantity=5)
    assert item.total_value == 7500.0  # 1500 * 5


#Тесты на валидацию данных
def test_negative_price_raises_error():
    """Проверяет, что отрицательная цена вызывает исключение."""
    with pytest.raises(InvalidItemDataError):
        Item(id="3", name="Товар", category="Разное", price=-100.0, quantity=1)


def test_negative_quantity_raises_error():
    """Проверяет, что отрицательное количество вызывает исключение."""
    with pytest.raises(InvalidItemDataError):
        Item(id="4", name="Товар", category="Разное", price=100.0, quantity=-5)


def test_empty_name_raises_error():
    """Проверяет, что пустое название вызывает исключение."""
    with pytest.raises(InvalidItemDataError):
        Item(id="5", name="", category="Разное", price=100.0, quantity=1)


#Тест на создание товара с нулевой ценой
def test_zero_price_is_allowed():
    """Товар с нулевой ценой должен создаваться без ошибок."""
    item = Item(id="6", name="Пробник", category="Разное", price=0.0, quantity=1)
    assert item.price == 0.0