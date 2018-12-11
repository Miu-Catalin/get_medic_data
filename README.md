# Exemplu script export date medici

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

exemplu pentru listarea specialitatilor

```python
for index, medic in enumerate(lista_date_medici):
    specialitate = ""
    studii_complementare = ""
    for item in medic.preg_postuniv:
        if item.active is True:
            if item.tip.id in [1, 7]:
                if specialitate != "":
                    specialitate += ", "
                specialitate += item.ppu.nume + " (Rezident)"
            if item.tip.id == 2 and item.active is True:
                if specialitate != "":
                    specialitate += ", "
                specialitate += item.ppu.nume + " (" + item.grad.nume + ")"
            if item.tip.id in [3, 4, 5, 6] and item.active is True:
                if studii_complementare != "":
                    studii_complementare += ", "
                studii_complementare += item.ppu.nume

    row = (
        index + 1,
        medic.nume,
        medic.prenume,
        medic.cuim,
        medic.cnp,
        medic.cod_parafa,
        medic.status.nume,
        specialitate,
        studii_complementare,
        medic.email,
        medic.telefon,
    )

    sheet.append(row)
    index += 1

book.save(out)
out.seek(0)
```

## Instalare

```bash
git clone https://github.com/Miu-Catalin/get_medic_data.git
cd get_medic_data
```

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