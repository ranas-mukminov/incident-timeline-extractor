# 🔍 incident-timeline-extractor

[![CI](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/ci.yml)
[![Security Audit](https://github.com/ranas-mukminov/incident-timeline-extractor/workflows/Security%20Audit/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/security.yml)
[![Code Quality](https://github.com/ranas-mukminov/incident-timeline-extractor/workflows/Code%20Quality/badge.svg)](https://github.com/ranas-mukminov/incident-timeline-extractor/actions/workflows/code-quality.yml)

Automated incident timeline extraction and AI-assisted postmortem generation for SRE teams.

**Production-ready** | **Multi-source** | **AI-powered** | **Privacy-first**

---

## English

`incident-timeline-extractor` aggregates logs from journald, Nginx, syslog, Zabbix and Prometheus/Alertmanager, normalizes them into a unified incident timeline, and exports JSON/Markdown/ASCII formats. The companion `postmortem-generator-ai` consumes the timeline plus a short operator note to draft a blameless SRE-style postmortem, with optional PDF export.

### Why this exists
- During incidents, evidence is scattered across journald, web server logs, syslog, alerts, and monitoring systems.
- Creating postmortems demands a clean, chronologically correct timeline and consistent structure.
- This project automates timeline extraction, normalization, and postmortem drafting so responders can focus on impact and remediation.

### ✨ Features

- 📊 **Multi-Source Collection**: journald, Nginx, syslog, Zabbix, Prometheus/Alertmanager
- ⏱️ **Timeline Building**: Chronologically sorted JSON with Markdown/ASCII export
- 🤖 **AI-Assisted Analysis**: Event tagging and cause clustering (pluggable providers)
- 📝 **Postmortem Generation**: AI-generated blameless postmortems (Markdown + PDF)
- 🔒 **Privacy-First**: No data leaves your infrastructure by default
- 🛠️ **CLI Interface**: Built with Typer - `collect`, `to-markdown`, `analyze`, `postmortem`
- 🌍 **Multi-Language**: English/Russian postmortem templates
- 🔌 **Offline Mode**: Works with deterministic mock provider

### 🚀 Quick start

**Prerequisites:** Python 3.10+, access to your logs or exported files.

**1. Install:**
```bash
pip install -e .
```

**2. Configure:**
Configure `config.yaml` (see `config.py` for schema and `examples/config.yaml`).

**3. Collect timeline:**
```bash
incident-timeline collect --incident-id INC-123 --config config.yaml --output timeline.json
```

**4. Convert to Markdown:**
```bash
incident-timeline to-markdown timeline.json > timeline.md
```

**5. Generate postmortem (Optional):**
```bash
incident-timeline postmortem --timeline timeline.json --input "Short summary..." --lang en --output postmortem.md
```

### 🔒 AI and privacy

- ✅ No log data is transmitted unless an external AI provider is configured
- ✅ Works offline with deterministic mock provider
- ⚠️ When using AI, ensure sensitive data is redacted/anonymized per your policies
- ⚠️ Review provider's terms of service before configuration

### 👨‍💻 Professional services – run-as-daemon.ru

**Professional SRE & incident management services by [run-as-daemon.ru](https://run-as-daemon.ru)**

This project is maintained by the SRE / DevOps engineer behind run-as-daemon.ru.

#### 💼 Services Offered:

- 🔍 **Incident Response**: Implementing incident timelines and postmortem culture
- 🔌 **Integration**: Connecting with your monitoring stack (Zabbix, Prometheus, etc.)
- 📊 **SRE Processes**: Setting up SLIs/SLOs and on-call routines
- 🎓 **Training**: Team workshops on blameless postmortems and incident management
- 🛠️ **Custom Development**: Extending the tool for your specific needs

#### 📞 Contact for Consulting:

**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

*"Defense by design. Speed by default"* — Security-first architecture with performance optimization

---

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Run linting:** `scripts/lint.sh`
4. **Run tests:** `pytest`
5. **Commit changes:** `git commit -m 'feat: add amazing feature'`
6. **Push to branch:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

#### Development Guidelines:

- Run `scripts/lint.sh` and `pytest` before opening a PR
- Follow the coding style enforced by ruff/black/isort
- Add tests for new functionality
- Keep user-facing CLI messages clear and safe by default
- Follow conventional commits format

### 📄 License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

---

## Русский (кратко)

`incident-timeline-extractor` собирает события из journald, Nginx, syslog, Zabbix и Prometheus/Alertmanager, нормализует их и строит единый таймлайн инцидента в формате JSON/Markdown/ASCII. Модуль `postmortem-generator-ai` берет таймлайн и короткое описание инженера, чтобы сгенерировать SRE-постмортем (Markdown, опционально PDF).

### ✨ Возможности:

- 📊 Объединяет логи и алерты, сортирует по времени
- 🤖 ИИ-тегирование подозрительных событий и кластеризация причин
- 📝 Постмортемы по шаблону SRE (EN/RU), можно использовать без ИИ
- 🔒 Данные не покидают вашу инфраструктуру по умолчанию
- 🛠️ Подходит для внедрения SRE-культуры и практик постмортемов

### 💼 Профессиональные услуги:

**[run-as-daemon.ru](https://run-as-daemon.ru)** — помощь с:
- Внедрением культуры постмортемов и таймлайнов инцидентов
- Интеграцией с системами мониторинга (Zabbix, Prometheus)
- Настройкой SRE-процессов и on-call дежурств
- Обучением команды методам управления инцидентами

---

## 📮 Support

**Community Support:**
- Open an issue on [GitHub Issues](https://github.com/ranas-mukminov/incident-timeline-extractor/issues)
- Check existing issues for solutions
- Read documentation in [docs/](./docs/)

**Professional Support:**
- Production deployment assistance
- Custom integrations with monitoring systems
- SRE process consulting
- Incident management training
- 24/7 support packages

**Contact:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Made with ❤️ for SRE teams**

**Professional SRE & DevOps Support:** [run-as-daemon.ru](https://run-as-daemon.ru)
