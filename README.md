# PyRakNet
SWIG bindings for RakNet(4.081) library

## Notes
pyraknet.i is located in fork of RakNet library.

## Installation
> macOS isn't tested but theoratically should be supported
> 
> Windows is supported by RakNet, so the PyRakNet should on run it.
### Linux
#### Compile SWIG files
```
git clone https://github.com/MlsDmitry/PyRakNet --recursive
cd PyRakNet/RakNet/Source
swig -c++ -python -builtin pyraknet.i
```
#### Compile RakNet and link with python shared module
```
Do this from root(PyRakNet) folder!

mkdir build && cd build
cmake ..
make -j2
```
## Use
File **pyraknet.py and _pyraknet.so should be in same directory as your code**
```
mkdir test_project && cd test_project
cp ./RakNet/Source/pyraknet.py .
cp ./build/_pyraknet.so .
python3 -c "import pyraknet"
```
## Run examples
```
cp ./RakNet/Source/pyraknet.py ./examples
cp ./build/_pyraknet.so ./examples
cd examples
python3 test_server.py          in 1st terminal
python3 test_client.py          in 2nd terminal
```