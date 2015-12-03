# -*- coding: utf-8 -*-
# script01.py
# 2014.10.26 K. Kuwata

import numpy as np
from math import *
from matplotlib import pyplot as plt
from datetime import datetime as dt
import csv

## 九九を表示 / Show 9 x 9
print "[Showing 9 x 9]"
A = np.array(range(1, 10))
for i in A:
    print A * i

print "~~~" * 10
print "\n"

# 素数を探す / Find prime number
print "Find Prime number"

def FindPrimeNumbers(N):
    counter = 0
    primes = []
    for n in range(2, N):
        isprime = True
        for i in range(2, n):
            counter += 1
            if n % i == 0:
                isprime = False
                break
        if isprime:
            primes.append(n)
    print primes, len(primes)
    print u'Times of division: %d' % counter


FindPrimeNumbers(2000)

print "~~~" * 10
print "\n"

print "Stock value of Yahoo! Japan in 2010"
data = np.loadtxt("../stocks.4869.txt")
print data

f = open('../stocks.4869.date.csv', 'rb')
dataReader = csv.reader(f)
a = [row for row in dataReader]
dates = [dt.strptime(row, '%Y-%m-%d %H:%M:%S') for row in a[0]]

plt.plot(dates, data, '-r')
plt.xticks(rotation=30)
plt.suptitle('Stock value of Yahoo! Japan in 2010', size='20')
plt.show()
