# HYPFS

The implementation of a Decentralized keywords Search Engine based on a hypercube structure and integrated with IPFS using Python.

<center><img src="sys_arch.png" width="75%" align="center"></center>

## Install

##### Requirements

- Python 3
- IPFS -> [install IPFS](https://docs.ipfs.io/install/command-line/)

##### Commands

```
git clone
cd hypfs
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

##### Other requirements

- [windows-curses](https://pypi.org/project/windows-curses/) (_only_ for Windows OS): `pip install windows-curses`
- [openpyxl](https://pypi.org/project/openpyxl/) (_only_ for benchmarking): : `pip install openpyxl`

## Usage

1. **Config**
   use the `src/config.py` file to configure:
   - **HYPERCUBE_SIZE**: defines the hypercube data structure dimension, i.e. the number of network's nodes.
   - **SUPERSET_THRESHOLD**: limits the number of objects returned by superset search.
2. **IPFS Daemon**
   Start an IPFS Daemon in a new console:
   `ipfs daemon`
3. **Boot network nodes**
   `python start_servers.py`
4. **Start client cli-app**
   `python menu.py /ip4/127.0.0.1/tcp/5001 50000`
   - the first parameter is your IPFS node API address
   - the second parameter is the OS port of one Hypercube node

## Folders

- **src**: contains all the scripts of the hypercube and node implementation.
- **results**: contains the results of tests carried out with the _bench.py_ script.
- **objects**: contains the objects downloaded from IPFS.
- **test_files**: used for generating random files.

## Executables

- **menu.py**: script that provides a user-friendly command line UI.
- **start_daemons.py**: script useful for starting two IPFS processes.
- **start_servers.py**: script useful for starting 2^HYPERCUBE_SIZE servers processes, and the hop_counter.
- **bench.py**: script used for testing.

## References

- Zichichi M., Serena L., Ferretti S., D'Angelo G., [Governing Decentralized Complex Queries Through a DAO](https://mirkozichichi.me/assets/papers/14governing.pdf), in Proc. of the Conference on Information Technology for Social Good (GoodIT). 9-11 September 2021
- Zichichi M., Serena L., Ferretti S., D'Angelo G., [Towards Decentralized Complex Queries over Distributed Ledgers: a Data Marketplace Use-case](https://mirkozichichi.me/assets/papers/12towards.pdf) , in Proc. of the 30th IEEE International Conference on Computer Communications and Networks (ICCCN). 3rd International Workshop on Social (Media) Sensing. 19-22 July 2021

## License

[Apache License 2.0](./LICENSE)
