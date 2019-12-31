# !/usr/bin/env python
# -*- coding:utf-8 -*-
principal = 10000
rate = 0.0275
numyears = 5
year = 1
while year <= numyears:
    principal = principal*(1+rate)
    print(year,principal)
    year += 1