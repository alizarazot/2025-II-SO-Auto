# 2025-II-SO-Auto

## Downloading

To download precompiled binary use: https://github.com/alizarazot/2025-II-SO-Auto/releases/download/v0.1.0/os-auto.exe

## Building from source

First install Poetry, then to install dependencies use:

```
poetry install
```

To run the project:

```
poetry run python -m src
```

To generate an executable:

```
poetry run pyinstaller --onefile src/__main__.py --specpath build -n os-auto
```

Then check the `dist/` directory.
