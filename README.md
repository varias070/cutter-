## Инструкция для запуска:

1. Клонировать репозиторий из гит

      ```bash
       git@github.com:varias070/cutter-.git
     ```
2. настроить файл .env

3. Выполнить 

   ```bash
    docker-compose pull
    docker-compose build 
    docker-compose up db
    docker-compose up app
   ```

## Логика работы

1. клиент присылает изображение
2. клиенту выдается название файла
3. изображение сжимается по заданным парамтрам
4. сохраняется в бд

## Точки входа

1. /save_image POST запрос с изображением и парметрами width и height в теле запроса
2. '/get_image' GET запрос для взятие с сервера сжатого изображение