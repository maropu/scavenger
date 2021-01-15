#!/usr/bin/env python3

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from abc import ABCMeta
from typing import Any, Optional

from pyspark.sql import SparkSession


class ApiBase(metaclass=ABCMeta):

    output: Optional[str] = None
    db_name: str = ""

    def __init__(self) -> None:
        # For Spark/JVM interactions
        self.spark = SparkSession.builder.getOrCreate()
        self.jvm = self.spark.sparkContext._active_spark_context._jvm

    def setOutput(self, output: str) -> Any:
        self.output = output
        return self

    def setDbName(self, db_name: str) -> Any:
        self.db_name = db_name
        return self

    def outputToConsole(self, msg: str) -> None:
        print(msg)


class ResultBase():

    output: Optional[str] = None

    # TODO: Prohibit instantiation directly
    def __init__(self, output: str) -> None:
        self.output = output

    def show(self) -> None:
        assert self.output is not None
        import webbrowser
        webbrowser.open("file://%s/index.html" % self.output)

