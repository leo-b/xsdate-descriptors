#!/usr/bin/python3

# xsdata-ext.py generate test-schema.xsd --package test_xsdata_descr.test_xsdata_descr --structure-style single-package --output ext

from xsdata_ext.generator import ExtGenerator
from xsdata.__main__ import main
import sys

from xsdata.codegen.writer import CodeWriter
CodeWriter.register_generator("ext", ExtGenerator)

if __name__ == '__main__':
    sys.exit(main())
