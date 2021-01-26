#!/usr/bin/env python

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

import logging
import os
import sys
import subprocess
import time
import uuid

from argparse import ArgumentParser


def print_red(text):
    print('\033[31m' + text + '\033[0m')


REPAIR_API_LIB = ""
REPAIR_MODULE_PATH = ""
REPAIR_TESTDATA = ""

LOGGER = logging.getLogger()


def run_individual_python_test(target_dir, test_name):
    env = dict(os.environ)
    env.update({
        'PYTHONPATH': REPAIR_MODULE_PATH,
        'REPAIR_API_LIB': REPAIR_API_LIB,
        'REPAIR_TESTDATA': REPAIR_TESTDATA,
        'SPARK_TESTING': '1'
    })

    # Creates an unique temp directory under 'target/' for each test
    tmp_dir = os.path.join(target_dir, "{}-{}".format(test_name, str(uuid.uuid4())))
    while os.path.isdir(tmp_dir):
        tmp_dir = os.path.join(target_dir, "{}-{}".format(test_name, str(uuid.uuid4())))
    os.mkdir(tmp_dir)

    LOGGER.info("Starts running test: %s", test_name)
    start_time = time.time()
    try:
        per_test_output = "{}/output-{}".format(tmp_dir, str(uuid.uuid4()))
        with open(per_test_output, 'w') as f:
            retcode = subprocess.Popen(
                ["python", "{}/tests/{}.py".format(os.path.dirname(__file__), test_name)],
                stderr=f, stdout=f, env=env).wait()
    except:
        LOGGER.exception("Got exception while running test: %s", test_name)
        # Here, we use os._exit() instead of sys.exit() in order to force Python to exit even if
        # this code is invoked from a thread other than the main thread.
        os._exit(1)

    duration = time.time() - start_time

    if retcode != 0:
        try:
            with open(per_test_output, 'r') as f:
                for line in f:
                    print(line, end='')
        except:
            LOGGER.exception("Got an exception while trying to print failed test output")
        finally:
            print_red(f"\nHad test failures in {test_name}; see logs")
            # Here, we use os._exit() instead of sys.exit() in order to force Python to exit even if
            # this code is invoked from a thread other than the main thread.
            os._exit(-1)
    else:
        LOGGER.info("Passed (%is)", duration)


# TODO: Brush up this test runner by referring to the PySpark code:
#  - https://github.com/apache/spark/blob/master/python/run-tests.py
if __name__ == "__main__":

    # Parses command-line arguments
    parser = ArgumentParser()
    parser.add_argument('--package', dest='package', type=str, required=True)
    parser.add_argument('--mod', dest='module', type=str, required=True)
    parser.add_argument('--data', dest='data', type=str, required=True)
    args = parser.parse_args()

    # Sets enveironmental variables for tests
    REPAIR_API_LIB = args.package
    REPAIR_MODULE_PATH = args.module
    REPAIR_TESTDATA = args.data

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    LOGGER.info("Running Python tests...")

    # Create the target directory before starting tests
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'target'))
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    run_individual_python_test(target_dir, "test_model")
    run_individual_python_test(target_dir, "test_detectors")
    run_individual_python_test(target_dir, "test_distances")
    run_individual_python_test(target_dir, "test_misc")
