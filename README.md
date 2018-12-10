# Exemplu script get medic data

## Utilizare

```bash
python get_medic_data.py --api https://adresa_api --tip json --email user@domain.com
```

datele sunt exportate in folderul *./export*

datele se pot exporta in format:
- xlsx
- csv
- json

pentru modificarea campurilor exportate in format xlsx si csv se editeaza fisierul app/export.py

## Instalare

Instaleaza python venv

```bash
python3 -m venv venv
```

se activeaza venv
linux

```bash
source venv/bin/activate
```
windows
```bash
C:\> .\venv\Scripts\activate.bat
```

se instaleaza python libraries

```bash
pip install -r requirements.txt
```