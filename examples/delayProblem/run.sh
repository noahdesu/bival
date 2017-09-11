#!/usr/bin/env bash

cmd="time python ../../src/drivers/biv.py -c 0 -n str --EOT 2 -f ./delayProblem.ded --evaluator c4"
opt_cmd="cmd"

rm ./IR.db
rm ./tmp.txt

if [ "$1" = "$opt_cmd" ]
then
  # run command an do not hide stdout
  $cmd
  rm ./IR.db
else
  # run the test and hide stdout
  $cmd > tmp.txt

  # check if test passed (TODO: make more sophisticated)
  if grep -Fxq "PROGRAM EXITED SUCCESSFULLY" tmp.txt
  then
    echo "TEST PASSED"
    rm tmp.txt
  fi
fi
