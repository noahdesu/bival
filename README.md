# bival

A sandbox for modeling ceph using either Dedalus or C4 Overlog. Provenance graph generation only supports Dedalus programs at the moment.

# INSTALLATION
```
python setup.py
```

# EXAMPLES
Dedalus example :
```
$ cd examples/delayProblem/
$ bash run.sh cmd
```

C4 Overlog example :
```
$ cd examples/eqnSupport/
$ bash run_working.sh
```

# building with cmake

```
git submodule update --init --recursive
dnf install -y cmake gcc apr-devel apr-util-devel flex bison sqlite-devel sympy
cd lib/PyC4
cmake . && make
cd ../../lib/orik
cmake . && make
cd ../../
```
