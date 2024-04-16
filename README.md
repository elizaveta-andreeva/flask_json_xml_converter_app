# Сервис конвертации
## Инструкция по запуску
1. Склонировать репозиторий
2. Установить все зависимости из `requirements.txt`
    ```
    $ pip install -r tasks/requirements.txt
    ```
3. Запустить сервер с помощью команды
    ```
    $ flask run
    ```
    Приложение доступно по адресу http://127.0.0.1:5000
4. Можно открыть в браузере страницу http://127.0.0.1:5000 и воспользоваться интерфейсом.

## Конвертировать JSON в XML
Без валидации xml по схеме xsd:
http://127.0.0.1:5000/convert/json_to_xml

С валидацией:
http://127.0.0.1:5000/convert/json_to_xml/true

## Конвертировать XML в JSON
Без валидации xml по схеме xsd:
http://127.0.0.1:5000/convert/xml_to_json

С валидацией:
http://127.0.0.1:5000/convert/xml_to_json/true

## Формат входных данных
Примеры выходных данных можно найти в папке examples.
### JSON to XML
В исходном файле App_info.json не содержится следующих необходимых данных (опираясь на схему xsd):
- `document_type_id` - id документа, данные которого подаются на вход, это значение должно быть взято из `dict_document_type_cls.json`
- `is_registration` - является ли адрес регистрацией

В исходном файле App_info.json в неверном формате содержатся следующие данные:
- `kladr_1` - в соответствии со схемой необходимо, чтобы это значение было числом
- `passport_begda` - неверный формат даты (нужно `yyyy-mm-dd`)
- `birthday` - неверный формат даты (нужно `yyyy-mm-dd`)
- `address_txt3` - (город) не должно быть null

## Формат выходных данных
### XML to JSON
При конвертации xml в json имена некоторых тэгов не сопоставлялись с ключами из файла `App_info.json`, а формировались в процессе. 
Все ключи, которые можно получить при конвертации имеют информативные названия.
