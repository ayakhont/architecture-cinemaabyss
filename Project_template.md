## Изучите [README.md](.\README.md) файл и структуру проекта.

# Задание 1

[диаграмма контейнеров С4](docs/containers_C4.puml)


# Задание 2

### 1. Proxy
- Proxy сервис реализован src/microservices/proxy/
- postman тесты прогнаны успешно
- постепенный переход, при изменении переменной окружения 
MOVIES_MIGRATION_PERCENT в файле docker-compose.yml, отрабатывает корректно

### 2. Kafka
- Events service c соответствующим API и sconsumer'ами и producer'ами kafka реализован в src/microservices/events/
- Необходимые тесты для проверки API tests/postman прогнаны успешно [отчёт](docs/test_results.png)
- состояния топиков Kafka из UI: [movie-events](docs/movie-events.png), [user-events](docs/user-events.png), [payment-events](docs/payment-events.png) 

# Задание 3
CI/CD: https://github.com/ayakhont/architecture-cinemaabyss/actions

скриншоты логов event-service обработки событий при запуске 
`npm run test:kubernetes`
- [скриншот 1](docs/event-service_1.png)
- [скриншот 2](docs/event-service_2.png)
- [скриншот 3](docs/event-service_3.png)

скриншот вывода при вызове https://cinemaabyss.example.com/api/movies
- [скриншот](docs/cinemaabyss.example.com.png)


# Задание 4

Я доделал helm конфиги и разворачивание в k8s кластер прошло успешно. Конфиги helm такие же, как и в предыдущем задании.
Но 4ое задание мне пришлось делать на другом ноуте, и далее на новом инвайронменте начали происходить чудеса с 
разрешением DNS имён внутри кластера. Несколько вечеров я провозился с этой проблемой, но так и не смог её решить. 
Судя по всему, сам coredns работает хорошо (я проверил все сценарии 
https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/) и проблемы именно с kube-proxy 
и форваридингом по IP table запросов на нужные pod'ы.

[скриншот c состоянием подов](docs/unresolved_hosts_on_new_laptop.png)

Как можно видеть из скриншота 3 сервиса не могут нормально стартовать: kafka из-за невозможности достучаться до zookeeper,
а остальные два: monolith и movie-service из-за невозможности достучаться до postgres.

Я не вижу проблем в самих helm чарте. На предыдущем ноуте на аналогичных k8s конфигах без helm из 3его задания 
всё разворачивалось и работало. Через 4 дня у меня будет доступ к тому ноуту, и я смогу проверить там свои helm чарты.
