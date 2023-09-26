## Usage

Initiate pipenv

```bash
pipenv install
pipenv shell
```

Options
```bash
Usage: main.py [OPTIONS]

Options:
  --output-file TEXT   Output file
  --profile TEXT       AWS Profile
  --initial-date TEXT  The initial date to gather the events (format %m/%d/%Y
                       %H:%M). e.g. 09/21/2023 00:00
  --help               Show this message and exit.
```

Executing
```bash
python main.py --profile "<aws-profile>" --initial-date "09/21/2023 00:00"
```