"""
Слой доступа к данным - чтение и запись в JSON-файл.
"""
import json
import os
from typing import List
from app.models import Item
from app.exceptions import ItemNotFoundError, InventoryStorageError

class InventoryRepository:
    """Реализует CRUD-операции над товарами, хранящимися в JSON."""

    def __init__(self, file_path: str = "data/inventory.json") -> None:
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создать файл с пустым списком, если его еще нет."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self._write_data([])

    def _read_data(self) -> List[dict]:
        """Прочитать сырые данные из JSON."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise InventoryStorageError(f"Повреждённый JSON-файл: {e}") from e
        except OSError as e:
            raise InventoryStorageError(f"Ошибка чтения файла: {e}") from e

    def _write_data(self, data: List[dict]) -> None:
        """Записать данные в JSON (полная перезапись)."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            raise InventoryStorageError(f"Не удалось записать файл: {e}") from e

    def get_all(self) -> List[Item]:
        """Получить все товары."""
        raw_items = self._read_data()
        return [Item(**raw) for raw in raw_items]

    def get_by_id(self, item_id: str) -> Item:
        """Найти товар по id или выбросить исключение."""
        raw_items = self._read_data()
        for raw in raw_items:
            if raw["id"] == item_id:
                return Item(**raw)
        raise ItemNotFoundError(f"Товар с id '{item_id}' не найден")

    def add(self, item: Item) -> None:
        """Добавить новый товар. Если id уже существует - ошибка."""
        raw_items = self._read_data()
        for raw in raw_items:
            if raw["id"] == item.id:
                raise ValueError(f"Товар с id '{item.id}' уже существует")
        raw_items.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "quantity": item.quantity,
        })
        self._write_data(raw_items)

    def update(self, item: Item) -> None:
        """Обновить существующий товар. Если не найден - исключение."""
        raw_items = self._read_data()
        updated = False
        for i, raw in enumerate(raw_items):
            if raw["id"] == item.id:
                raw_items[i] = {
                    "id": item.id,
                    "name": item.name,
                    "category": item.category,
                    "price": item.price,
                    "quantity": item.quantity,
                }
                updated = True
                break
        if not updated:
            raise ItemNotFoundError(f"Товар с id '{item.id}' для обновления не найден")
        self._write_data(raw_items)

    def delete(self, item_id: str) -> None:
        """Удалить товар по id. Если не найден -исключение."""
        raw_items = self._read_data()
        initial_length = len(raw_items)
        raw_items = [raw for raw in raw_items if raw["id"] != item_id]
        if len(raw_items) == initial_length:
            raise ItemNotFoundError(f"Товар с id '{item_id}' для удаления не найден")
        self._write_data(raw_items)