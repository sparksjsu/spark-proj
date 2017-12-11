#!/bin/sh
pid=$(ps -ef | grep  -e "python run_spark_proj\.py" | awk  '{print $2}')
kill -9 $pid
exit 0
