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

def require_minimum_pandas_version():
    """ Raise ImportError if minimum version of Pandas is not installed
    """
    # TODO: Relocate and deduplicate the version specification.
    minimum_pandas_version = "0.23.2"

    from distutils.version import LooseVersion
    try:
        import pandas
        have_pandas = True
    except ImportError:
        have_pandas = False
    if not have_pandas:
        raise ImportError("Pandas >= {} must be installed; however, "
                          "it was not found.".format(minimum_pandas_version))
    if LooseVersion(pandas.__version__) < LooseVersion(minimum_pandas_version):
        raise ImportError("Pandas >= {} must be installed; however, "
                          "your version was {}.".format(minimum_pandas_version, pandas.__version__))


pandas_requirement_message = None
try:
    require_minimum_pandas_version()  # type: ignore
    have_pandas = True
except ImportError as e:
    # If pandas version requirement is not satisfied, skip related tests.
    have_pandas = False


def require_minimum_pyarrow_version():
    """ Raise ImportError if minimum version of pyarrow is not installed
    """
    # TODO: Relocate and deduplicate the version specification.
    minimum_pyarrow_version = "0.17.1"

    from distutils.version import LooseVersion
    try:
        import pyarrow
        have_arrow = True
    except ImportError:
        have_arrow = False
    if not have_arrow:
        raise ImportError("PyArrow >= {} must be installed; however, "
                          "it was not found.".format(minimum_pyarrow_version))
    if LooseVersion(pyarrow.__version__) < LooseVersion(minimum_pyarrow_version):
        raise ImportError("PyArrow >= {} must be installed; however, your version was {}.".format(
            minimum_pyarrow_version, pyarrow.__version__))


pyarrow_requirement_message = None
try:
    require_minimum_pyarrow_version()  # type: ignore
    have_pyarrow = True
except ImportError as e:
    # If Arrow version requirement is not satisfied, skip related tests.
    have_pyarrow = False