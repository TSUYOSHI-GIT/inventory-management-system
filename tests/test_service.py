"""
Тесты для InventoryService.
"""
import os
import pytest
from app.models import Item
from app.repository import InventoryRepository
from app.service import InventoryService
from app.exceptions import ItemNotFoundError, InsufficientStockError


#Фикстура временного репозитория
@pytest.fixture
def temp_file_path(tmp_path):
    return os.path.join(tmp_path, "test_service.json")

@pytest.fixture
def repo(temp_file_path):
    return InventoryRepository(file_path=temp_file_path)

@pytest.fixture
def service(repo):
    """Сервис, подключенный к временному репозиторию."""
    return InventoryService(repo)


#Тест на получение всех товаров (пустой склад)
def test_get_all_empty(service):
    assert service.get_all_items() == []

#Тест на получение товара по id
def test_get_item_by_id(service):
    # Добавим товар через репозиторий напрямую
    item = Item("1", "Товар", "Кат", 10.0, 5)
    service.repo.add(item)
    result = service.get_item_by_id("1")
    assert result.name == "Товар"

#Тест на приемку нового товара
def test_receive_new_item(service):
    item = service.receive("2", "Новый", "Разное", 50.0, 10)
    assert item.id == "2"
    assert item.quantity == 10
    assert len(service.get_all_items()) == 1

#Тест на приемку существующего товара (увеличение количества)
def test_receive_existing_item(service):
    #Сначала добавим через receive
    service.receive("3", "Базовый", "Осн", 100.0, 7)
    #Примем ещё 3 штуки
    updated = service.receive("3", "Базовый", "Осн", 100.0, 3)
    assert updated.quantity == 10

#Тест на успешную отгрузку
def test_ship_success(service):
    service.receive("4", "Отгруз", "Тест", 30.0, 20)
    result = service.ship("4", 5)
    assert result.quantity == 15

#Тест на ошибку при нехватке товара
def test_ship_insufficient_stock(service):
    service.receive("5", "Дефицит", "Тест", 10.0, 2)
    with pytest.raises(InsufficientStockError):
        service.ship("5", 10)

#Тест на поиск по категории
def test_find_by_category(service):
    service.receive("6", "Клава", "Электроника", 500.0, 5)
    service.receive("7", "Мышь", "Электроника", 200.0, 3)
    service.receive("8", "Стол", "Мебель", 1500.0, 1)
    electronics = list(service.find_by_category("Электроника"))
    assert len(electronics) == 2

#Тест на поиск по названию
def test_find_by_name(service):
    service.receive("9", "Монитор LG", "Электроника", 10000.0, 4)
    service.receive("10", "LG Телевизор", "Электроника", 20000.0, 2)
    result = list(service.find_by_name("LG"))
    assert len(result) == 2

#Тест на поиск с низким остатком
def test_find_low_stock(service):
    service.receive("11", "Много", "Раз", 1.0, 100)
    service.receive("12", "Мало", "Два", 2.0, 2)
    low = list(service.find_low_stock(threshold=5))
    assert len(low) == 1
    assert low[0].id == "12"