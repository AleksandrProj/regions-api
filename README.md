# Правила пользования API регионов
Чтобы начать пользоваться API необходимо зарегистрировать аккаунт и получить для него токен. После можно будет уже работать с API.

    Рабочая API: https://region-app.herokuapp.com/
    * - Обязательные параметры

## Регистрация аккаунта

    URL: /api/users/register [POST]    
    Authorization: No
    Parametrs JSON:    
        *username [String]
        *password [String]

## Получение токена

    URL: /api/users/token [GET]
    Authorization: Yes
    Parametrs JSON: No

## Работа с модулями API

### Регионы

#### Вывод регионов

    URL: /api/regions [GET]    
    Authorization: Yes    
    Parametrs JSON: No

#### Добавление регионов

    URL: /api/regions/add [POST]    
    Authorization: Yes    
    Parametrs JSON:
        *name_region [String]
        *region_id [Int]

#### Изменение регионов
    
    URL: /api/regions/edit [PUT]    
    Authorization: Yes    
    Parametrs JSON:
        *new_name_region [String]
        *region_id [Int]

#### Удаление регионов

    URL: /api/regions/delete [DELETE]    
    Authorization: Yes    
    Parametrs JSON:
        *region_id [Int]

### Города

#### Вывод городов

    URL: /api/cities [GET]    
    Authorization: Yes    
    Parametrs JSON:
        region_id [Int]

#### Добавление города

    URL: /api/cities/add [POST]    
    Authorization: Yes    
    Parametrs JSON:
        *name_city [String]
        *region_id [Int]

#### Изменение города
    
    URL: /api/cities/edit [PUT]    
    Authorization: Yes    
    Parametrs JSON:
        *name_city [String]
        *new_name_city [String]

#### Удаление города

    URL: /api/cities/delete [DELETE]    
    Authorization: Yes    
    Parametrs JSON:
        *name_city [String]
