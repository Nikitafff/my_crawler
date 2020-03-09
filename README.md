# Scraper

### Overview
Scraper - простой, синхронный веб-краулер и веб-скрейпер.
Собирает данные о топовых игроках в Fortnite.
### Install
Устанавливаем зависимости
```shell script
pip install -r requirements/dev.txt
```

### Commands
Запуск краулера
```shell script
python -m scraper crawl [options]
```
&nbsp;&nbsp;&nbsp;&nbsp;Supported options:
  - ```--outfile=FILE``` or ```-o FILE```: файл, в который будут сохранены собранные данные
  - ```--format=FORMAT``` or ```-f FORMAT```: формат файла с собранными данными {csv, jl}
  - ```--pages=PAGE_NUMBER``` or ```-p PAGE_NUMBER```: сколько страниц будет парсить, по умолчанию = 10 {int}