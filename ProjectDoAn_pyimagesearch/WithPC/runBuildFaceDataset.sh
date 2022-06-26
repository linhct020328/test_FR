#!/bin/bash

mkdir dataset/${@}
python getDatasetPC.py  --output dataset/${@}
