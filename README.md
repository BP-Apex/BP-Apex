# Bpex

## Environment

Bpex is tested on the following operating systems:

- Ubuntu 16.04

Bpex is tested on the following Python versions:

- python 3.7

## Dependencies

Running example and benchmark:

- numpy

Development or run other programs:

- clang-3.7

## Examples

The `examples/` directory contains an example program:

- c.c is one of the correct example from the benchmark
- w.c is one of the correct example from the benchmark
- input is the testcase
- mark is the marked alignments
- c_symb and w_symb are complied traces from c.c and w.c

## Feedback

To generate feedback, use:

```bash
python3 bp_apex feedback examples/1/input examples/1/w.c examples/1/c.c --mark examples/1/mark -symb --sw examples/1/w_symb --sc examples/1/c_symb --verbose 1
```

## Align

To perform alignment, use:

```bash
python3 bp_apex align examples/1/input examples/1/w.c examples/1/c.c --mark examples/1/mark -symb --sw examples/1/w_symb --sc examples/1/c_symb --verbose 1
```

## Experiment

To reproduce the experiment, use:

```bash
python3 run.py -option all
```

## Options

To run the benchmark in different options (rq2 and rq3), use:

```bash
python3 run.py -option [bpapex/fcd/.../iter_2]
```
