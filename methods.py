import urllib2
import os
import time
import re

# non-crawler based methods

def bigger(a,b):
  if a > b:
    return a
  else :
    return b

def biggest(a,b,c):
  return bigger(a,bigger(b,c))

def median(a,b,c):
  big = biggest(a,b,c)
  if big == a:
    return bigger(b,c)
  if big ==b:
    return bigger(a,c)
  else :
    return bigger(a,b)

def say(h,m,s):
    h_s = ' hour, '
    m_s = ' minute, '
    s_s = ' second'
    if h != 1:
        h_s = ' hours, '
    if m != 1:    
        m_s = ' minutes, '
    if s != 1:
        s_s = ' seconds'
    h,m,s = str(h),str(m),str(s)
    return h+h_s+m+m_s+s+s_s

def convert_seconds(secs):
    h = int(secs/3600)
    secs -= h*3600
    m = int(secs/60)
    secs -= m*60
    return say(h,m,secs)

def download_time(fs,fs_mult,b,b_mult):
    sizes = [['kb',2**10],['kB',2**10*8],['Mb',2**20],['MB',2**20*8],['Gb',2**30],['GB',2**30*8],['Tb',2**40],['TB',2**40*8]]
    for entry in sizes:
        if entry[0] == fs_mult:
            dist = entry[1]*fs*1.0
        if entry[0] == b_mult:
            speed = entry[1]*b*1.0
    time = dist/speed
    return convert_seconds(time)

def clean_string(string):
  string = re.findall(r'\w+',string)
  return string

def split_string(source,splitlist):
  output = []
  atsplit = True
  for char in splitlist:
    if char in splitlist:
      atsplit = True
    else :
      if atsplit:
        output.append(char)
        atsplit = False
      else :
        output[-1] = output[-1] + char
  return output

def time_execution(code):
  start = time.clock()
  result = eval(code)
  run_time = time.clock() - start
  return result, run_time

def calc_mean(list):
  sum = 0.0
  for item in list:
    sum += item
  return sum/len(list)  

def calc_sd(list):
  mean = calc_mean(list)
  sum = 0.0
  for item in list:
    sum += (item - mean)**2
  return (sum/len(list))**(0.5)

def spin_loop(n):
  i = 0
  while i < n:
    i += 1

def union(p,q):
  for e in q:
    if e not in p:
      p.append(e)

def hashtable_lookup(htable,key):
  for entry in hashtable_get_bucket(htable,key):
    if entry[0] == key:
      return entry[1]
  return None

def hashtable_get_bucket(htable,keyword):
  return htable[hash_string(keyword,len(htable))]

def hashtable_add(htable,key,value):
  hashtable_get_bucket(htable,key).append([key,value])

def hashtable_update(htable,key,value):
  bucket = hashtable_get_bucket(htable,key)
  for entry in bucket:
    if entry[0] == key:
      entry[1] = value
      return
  bucket.append([key,value])
  
def test_hash_function(func,keys,size):
  results = [0]*size
  keys_used = []
  for w in keys:
    if w not in keys_used:
      hv = func(w,size)
      results[hv] += 1
      keys_used.append(w)
  return results

def hash_string(keyword,buckets):
  h = 0
  for c in keyword:
    h = (h+ord(c))%buckets
  return h
