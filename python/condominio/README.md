## Extract and calc the value of FUNDO DE RESERVA from PDFs

### How to use

#### Install packages
```bash
pipenv install
pipenv shell
```

#### Decrypt PDFs
```bash
python decrypt_pdfs.py <folder> <master_password>
```

#### Extract value from each pdf and calc
```bash
python extract_value.py <folder>
```

### Testing
```bash
pytest -x -vv
```