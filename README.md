# ansible_dynamic_inventory_for_vagrant

Dynamic training inventory for working with ansible

## Динамический инвентарь

На случай если хосты располагаются в облаке, то вся информация о них хранится в облаке и доступна через API
Таким образом вместо копирования данных из интерфейса облака можно применить скрипт который подготовит данные.
Ansible поддерживает функцию динамическго инвентори, для этого файл который подаётся в ansible должен быть исполняемым.

## Интерфейс Сценария динамического инвентори

Сценарий должен поддерживать два параметар командной строки:

1. **--list** вывод информации о группах
1. **--host=hostname** вывод информации о хостах

### Вывод информации о хосте

Чтобы получить данные о конкретном хосте, ansible вызывает сценарий динамического инвентори командой ./inventory_vagrant.py --host=host01
Вывод сценария должен содержать переменные для заданного хоста, включая поведенческие параметры, например:

```yaml
{
  "ansible_ssh_host": "127.0.0.1",
  "ansible_ssh_port": "2200",
  "ansible_ssh_user": "vagrant"
}
```

### Вывод списка членов групп

Сценари динамического инвентори должен уметь выводить списки членов всех групп, а также данные об отдельных хостах. Ansible вызовет командой /inventory_vagrant.py --list
Результат ожидается в виде единого объекта JSON, имена свойств в котором соответствуют именам групп, а заначения - это массивы с именами хостов.
