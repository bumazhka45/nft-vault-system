# Address Diary

**Address Diary** — сохраняет историю транзакций Bitcoin-адреса в локальную базу данных (SQLite).

## Возможности

- Локальное сохранение истории адреса
- Позволяет быстро анализировать активность без повторного обращения к API
- Удобен для мониторинга кошельков, архивирования и аналитики

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python address_diary.py <bitcoin_address>
```

## Пример

```bash
python address_diary.py 1BoatSLRHtKNngkdXEeobR76b53LETtpyT
```

## Лицензия

MIT
