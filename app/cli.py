"""
Консольный интерфейс для управления складом.
"""
from app.repository import InventoryRepository
from app.service import InventoryService
from app.exceptions import InventoryError

def main():
    repo = InventoryRepository()
    service = InventoryService(repo)

    while True:
        print("\nСкладской учет")
        print("1. Показать все товары")
        print("2. Найти товар по id")
        print("3. Принять товар")
        print("4. Отгрузить товар")
        print("5. Поиск по категории")
        print("6. Поиск по названию")
        print("7. Товары с низким остатком")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            items = service.get_all_items()
            for item in items:
                print(f"{item.id}: {item.name} ({item.category}) - {item.quantity} шт по {item.price} руб")

        elif choice == "2":
            item_id = input("Введите id: ")
            try:
                item = service.get_item_by_id(item_id)
                print(f"Найден: {item.name}, {item.quantity} шт")
            except InventoryError as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            item_id = input("id: ")
            name = input("Название: ")
            category = input("Категория: ")
            price = float(input("Цена: "))
            quantity = int(input("Количество: "))
            try:
                item = service.receive(item_id, name, category, price, quantity)
                print(f"Товар принят. Теперь на складе: {item.quantity} шт")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "4":
            item_id = input("id товара: ")
            quantity = int(input("Количество для отгрузки: "))
            try:
                item = service.ship(item_id, quantity)
                print(f"Отгружено. Осталось: {item.quantity} шт")
            except InventoryError as e:
                print(f"Ошибка: {e}")

        elif choice == "5":
            cat = input("Категория: ")
            found = list(service.find_by_category(cat))
            if found:
                for item in found:
                    print(f"{item.id}: {item.name} - {item.quantity} шт")
            else:
                print("Ничего не найдено")

        elif choice == "6":
            keyword = input("Ключевое слово: ")
            found = list(service.find_by_name(keyword))
            if found:
                for item in found:
                    print(f"{item.id}: {item.name} - {item.quantity} шт")
            else:
                print("Ничего не найдено")

        elif choice == "7":
            found = list(service.find_low_stock())
            if found:
                for item in found:
                    print(f"{item.id}: {item.name} - {item.quantity} шт")
            else:
                print("Все товары в достатке")

        elif choice == "0":
            print("Выход")
            break

        else:
            print("Неверный ввод. Попробуйте снова")

if __name__ == "__main__":
    main()