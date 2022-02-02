# End-to-end tests

These tests are implemented in Python and can be executed either using the [Speculos](https://github.com/LedgerHQ/speculos) emulator or a Ledger Nano S/X.
Python dependencies are listed in [requirements.txt](requirements.txt), install them using [pip](https://pypi.org/project/pip/)

```
pip install -r requirements.txt
```

### Launch with Speculos

First start your application with Speculos
```
docker pull ghcr.io/ledgerhq/speculos
docker image tag ghcr.io/ledgerhq/speculos speculos
docker run --rm -it -v $(pwd)/bin:/speculos/apps --publish 9999:9999 --publish 5001:5000 --publish 9998:9998  speculos --display headless --button-port 9998 apps/app.elf
```

then in the `tests` folder run

```
pytest --headless
```

### Launch with your Nano S/X



Be sure to have you device connected through USB (without any other software interacting with it) and run

```
pytest --hid
```
