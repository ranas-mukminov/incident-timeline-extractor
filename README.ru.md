# 🔍 incident-timeline-extractor

[![CI](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/ci.yml)
[![Security Audit](https://github.com/ranas-mukminov/incident-timeline-extractor/workflows/Security%20Audit/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/security.yml)
[![Code Quality](https://github.com/ranas-mukminov/incident-timeline-extractor/workflows/Code%20Quality/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/code-quality.yml)

Автоматизированное извлечение таймлайнов инцидентов и генерация постмортемов с помощью ИИ для SRE-команд.

**Production-ready** | **Множество источников** | **ИИ-помощник** | **Безопасность данных**

---

## Русский

`incident-timeline-extractor` — CLI-инструмент для агрегации логов из journald, Nginx, syslog, Zabbix и Prometheus/Alertmanager. Он нормализует события, строит единый хронологический таймлайн инцидента и экспортирует его в JSON, Markdown и ASCII. Дополнительный модуль `postmortem-generator-ai` генерирует SRE-постмортем на основе таймлайна и короткого описания инженера.

### Зачем это нужно

- Во время инцидентов информация разбросана по journald, логам веб-серверов, syslog, алертам и системам мониторинга
- Создание постмортемов требует чистого хронологического таймлайна и единой структуры
- Этот проект автоматизирует извлечение таймлайна, нормализацию и создание постмортемов, чтобы команда могла сосредоточиться на устранении проблем

### ✨ Возможности

- 📊 **Множество источников**: journald, Nginx, syslog, Zabbix, Prometheus/Alertmanager
- ⏱️ **Построение таймлайна**: Хронологически отсортированный JSON с экспортом в Markdown/ASCII
- 🤖 **ИИ-анализ**: Тегирование событий и кластеризация причин (подключаемые провайдеры)
- 📝 **Генерация постмортемов**: ИИ-генерация постмортемов без обвинений (Markdown + PDF)
- 🔒 **Безопасность данных**: Данные не покидают инфраструктуру по умолчанию
- 🛠️ **CLI интерфейс**: Построен на Typer - `collect`, `to-markdown`, `analyze`, `postmortem`
- 🌍 **Мультиязычность**: Шаблоны постмортемов на английском и русском
- 🔌 **Офлайн режим**: Работает с детерминированным мок-провайдером

### 🚀 Быстрый старт

**Требования:** Python 3.10+, доступ к вашим логам или экспортированным файлам.

**1. Установка:**
```bash
pip install -e .
```

**2. Конфигурация:**
Настройте `config.yaml` (см. `config.py` для схемы и `examples/config.yaml`).

**3. Сбор таймлайна:**
```bash
incident-timeline collect --incident-id INC-123 --config config.yaml --output timeline.json
```

**4. Конвертация в Markdown:**
```bash
incident-timeline to-markdown timeline.json > timeline.md
```

**5. Генерация постмортема (опционально):**
```bash
incident-timeline postmortem --timeline timeline.json --input "Краткое описание..." --lang ru --output postmortem.md
```

### 🔒 ИИ и конфиденциальность

- ✅ Данные логов не передаются, если не настроен внешний ИИ-провайдер
- ✅ Работает офлайн с детерминированным мок-провайдером
- ⚠️ При использовании ИИ убедитесь, что чувствительные данные редактированы/анонимизированы
- ⚠️ Изучите условия использования провайдера перед настройкой

### 👨‍💻 Профессиональные услуги – run-as-daemon.ru

**Профессиональные SRE и услуги управления инцидентами от [run-as-daemon.ru](https://run-as-daemon.ru)**

Проект поддерживается SRE / DevOps инженером с сайта run-as-daemon.ru.

#### 💼 Предлагаемые услуги:

- 🔍 **Реагирование на инциденты**: Внедрение культуры таймлайнов и постмортемов
- 🔌 **Интеграция**: Подключение к вашему стеку мониторинга (Zabbix, Prometheus и др.)
- 📊 **SRE процессы**: Настройка SLI/SLO и дежурств
- 🎓 **Обучение**: Воркшопы для команд по постмортемам без обвинений и управлению инцидентами
- 🛠️ **Кастомная разработка**: Расширение инструмента под ваши нужды

#### 📞 Контакты для консультаций:

**Веб-сайт:** [run-as-daemon.ru](https://run-as-daemon.ru)

*"Защита в дизайне. Скорость по умолчанию"* — Архитектура с упором на безопасность и оптимизацию производительности

---

### 🤝 Участие в разработке

Мы приветствуем вклад в проект! Пожалуйста, следуйте этим рекомендациям:

1. **Форкните репозиторий**
2. **Создайте ветку:** `git checkout -b feature/amazing-feature`
3. **Запустите линтер:** `scripts/lint.sh`
4. **Запустите тесты:** `pytest`
5. **Закоммитьте изменения:** `git commit -m 'feat: add amazing feature'`
6. **Запушьте в ветку:** `git push origin feature/amazing-feature`
7. **Откройте Pull Request**

#### Рекомендации по разработке:

- Запускайте `scripts/lint.sh` и `pytest` перед созданием PR
- Следуйте стилю кода, который обеспечивают ruff/black/isort
- Добавляйте тесты для новой функциональности
- Делайте CLI-сообщения понятными и безопасными по умолчанию
- Следуйте формату conventional commits

### 📄 Лицензия

Проект распространяется под лицензией Apache-2.0 - см. файл [LICENSE](LICENSE) для деталей.

---

## 📮 Поддержка

**Поддержка сообщества:**
- Откройте issue на [GitHub Issues](https://github.com/ranas-mukminov/incident-timeline-extractor/issues)
- Проверьте существующие issue для решений
- Читайте документацию в [docs/](./docs/)

**Профессиональная поддержка:**
- Помощь с продакшен-развертыванием
- Кастомные интеграции с системами мониторинга
- Консалтинг по SRE-процессам
- Обучение управлению инцидентами
- Пакеты поддержки 24/7

**Контакт:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Сделано с ❤️ для SRE команд**

**Профессиональная SRE & DevOps поддержка:** [run-as-daemon.ru](https://run-as-daemon.ru)
