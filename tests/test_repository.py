"""
Тесты для InventoryRepository.
"""
import os
import pytest
from app.models import Item
from app.repository import InventoryRepository
from app.exceptions import ItemNotFoundError


# Фикстура, которая создаёт временный JSON-файл и возвращает путь к нему
@pytest.fixture
def temp_file_path(tmp_path):
    """Создает путь к временному файлу внутри временной папки."""
    return os.path.join(tmp_path, "test_inventory.json")


# Фикстура, которая возвращает репозиторий, работающий с временным файлом
@pytest.fixture
def repo(temp_file_path):
    """Возвращает экземпляр InventoryRepository с временным файлом."""
    return InventoryRepository(file_path=temp_file_path)


# Тест на добавление товара
def test_add_item(repo):
    """Проверяет, что товар добавляется и сохраняется."""
    item = Item(id="1", name="Тест", category="Кат", price=100.0, quantity=10)
    repo.add(item)

    items = repo.get_all()
    assert len(items) == 1
    assert items[0].id == "1"


# Тест на получение товара по id
def test_get_by_id(repo):
    """Проверяет поиск существующего товара."""
    item = Item(id="2", name="Поиск", category="Разное", price=50.0, quantity=3)
    repo.add(item)

    found = repo.get_by_id("2")
    assert found.name == "Поиск"


# Тест на исключение при поиске несуществующего id
def test_get_by_id_not_found(repo):
    """Проверяет, что выбрасывается ItemNotFoundError."""
    with pytest.raises(ItemNotFoundError):
        repo.get_by_id("nonexistent")


# Тест на обновление товара
def test_update_item(repo):
    """Проверяет обновление существующего товара."""
    item = Item(id="3", name="Старое", category="X", price=10.0, quantity=2)
    repo.add(item)

    updated = Item(id="3", name="Новое", category="Y", price=20.0, quantity=5)
    repo.update(updated)

    item_after = repo.get_by_id("3")
    assert item_after.name == "Новое"
    assert item_after.quantity == 5


# Тест на исключение при обновлении несуществующего
def test_update_not_found(repo):
    """Проверяет, что выбрасывается ItemNotFoundError при обновлении."""
    item = Item(id="999", name="Нет", category="Нет", price=1.0, quantity=1)
    with pytest.raises(ItemNotFoundError):
        repo.update(item)


# Тест на удаление товара
def test_delete_item(repo):
    """Проверяет удаление существующего товара."""
    item = Item(id="4", name="Удалить", category="Z", price=5.0, quantity=1)
    repo.add(item)
    repo.delete("4")

    assert len(repo.get_all()) == 0


# Тест на исключение при удалении несуществующего
def test_delete_not_found(repo):
    """Проверяет, что выбрасывается ItemNotFoundError при удалении."""
    with pytest.raises(ItemNotFoundError):
        repo.delete("nonexistent")


# Тест на ошибка при дублировании id
def test_add_duplicate_id(repo):
    """Проверяет, что добавление товара с существующим id вызывает ValueError."""
    item1 = Item(id="5", name="Первый", category="A", price=1.0, quantity=1)
    repo.add(item1)
    item2 = Item(id="5", name="Второй", category="B", price=2.0, quantity=2)
    with pytest.raises(ValueError):
        repo.add(item2)