# ledger-app-west

# Introduction 🔐

This is a Ledger devices wallet app for Waves Enterprise.

Special thanks to Jean Passot, Cédric Mesnil, and Oto from the Ledger team, Jake Bordens from the Ledger/Birst community for their support and advices. Thanks to the Waves community for trusting the tokens on this application.

For app APDU protocol and an integration manual please take a look at [this](https://github.com/wavesplatform/ledger-app-waves/wiki/Integration-manual). 

# Building 👷

Clone and build ledger-app-builder image as described [here](https://developers.ledger.com/docs/nano-app/build/)

In the root folder of the application:
```
docker run --rm -ti -v "$(realpath .):/app" ledger-app-builder:latest
```

Then run following command inside docker container:

```
root@656be163fe84:/app# BOLOS_SDK=$NANOS_SDK make
```


## Tests & Continuous Integration

The flow processed in [GitHub Actions](https://github.com/features/actions) is the following:

- Code formatting with [clang-format](http://clang.llvm.org/docs/ClangFormat.html)
- Compilation of the application for Ledger Nano S/X in [ledger-app-builder](https://github.com/LedgerHQ/ledger-app-builder)
- Unit tests of C functions with [cmocka](https://cmocka.org/) (see [unit-tests/](unit-tests/))
- End-to-end tests with [Speculos](https://github.com/LedgerHQ/speculos) emulator (see [tests/](tests/))
- Code coverage with [gcov](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html)/[lcov](http://ltp.sourceforge.net/coverage/lcov.php) and upload to [codecov.io](https://about.codecov.io)

It outputs 4 artifacts:

- `boilerplate-app-debug` within output files of the compilation process in debug mode
- `speculos-log` within APDU command/response when executing end-to-end tests
- `code-coverage` within HTML details of code coverage
- `documentation` within HTML auto-generated documentation
