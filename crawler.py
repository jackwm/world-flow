from methods import *

# format of index:
# index = [bucket,bucket,...]
# bucket = [entry,entry,...]
# entry = [keyword,links]
# links = [[url,count],[url,count],[url,count]...]
#     entry[0] = keyword    entry[1] = [[url,count],[url,count],...]
# entry = [keyword,[[url,count],[url,count]...]]

# format of index:
# {keyword1:{url1:count,url2,count},keyword:{url1:count,url2:count},...}}

def make_hashtable(n_buckets):
  table = []
  for i in range(0,n_buckets):
    table.append([])
  return table

def get_page(link):           
  try :
    return urllib2.urlopen(link).read()
  except :
    return ""

def get_next_target(page):
  start_link = page.find('<a href=')
  if start_link == -1:
    return None, 0
  else :
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote +1:end_quote]
    return url, end_quote

def print_all_links(page):
  while True:
    url, endpos = get_next_target(page)
    if url:
      print url
      page = page[endpos:]
    else :
      break

def get_all_links(page):
  links = []
  while True:
    url, endpos = get_next_target(page)
    if good_url(url) :
      links.append(url)
      page = page[endpos:]
    else :
      break
  return links

def get_docs(page):
  docs = tuple()
  s = save_links(page)
  i = 0
  while i < len(s):
    if s[i].find('.pdf') != -1:
      docs += (s[i],)
      i += 1
    else :
      i += 1
  return docs

def good_url(url):
  if (url[::-1])[0] == '#':
    print url, 'bad one'
    return False
  else :
    return True

def crawl_web(seed,max_pages,max_depth):
  tocrawl = [seed]
  crawled = []
  next_depth = []
  depth = 0
  index = {}
  graph = {}
  while tocrawl and depth <= max_depth:
    page = tocrawl.pop()
    if page not in crawled and len(crawled) < max_pages:
      content = get_page(page)
      add_page_to_index(index,page,content)
      outlinks = get_all_links(content)
      graph[page] = outlinks
      union(next_depth,outlinks)
      crawled.append(page)
    if not tocrawl:
      tocrawl, next_depth = next_depth, []
      depth += 1
  return index, graph

def record_user_click(index, keyword, url):
  urls = lookup(index, keyword)
  if urls:
    for entry in urls:
      if entry[0] == url:
        entry[1] = entry[1]+1

def add_to_index(index,keyword,url):
  if keyword in index:
    index[keyword].append(url)
  else :
    # not found, add new keyword to index
    index[keyword] = url

def add_page_to_index(index,url,content):
  words = content.split()
  for word in words:
    add_to_index(index,word,url)

def lookup(index,keyword):
  if keyword in index:
    return index[keyword]
  else :
    return None

# cache format {proc1:{proc1_in1:proc1_out1,proc1_in2:proc1_out2},proc2:{proc2_in1:proc2_out2},...}

def cached_execution(cache,proc,proc_input):
  if proc not in cache:
    cache[proc] = {}
    cache[proc][proc_input] = proc(proc_input)
    return cache[proc][proc_input]
  elif proc_input not in cache[proc]:
    cache[proc][proc_input] = proc(proc_input)
    return cache[proc][proc_input]
  else :
    return cache[proc][proc_input]


def compute_ranks(graph):
  d = 0.8 # damping factor
  numloops = 10
  ranks = {}
  npages = len(graph)
  for page in graph:
    ranks[page] = 1.0/npages
  for i in range(0,numloops):
    newranks = {}
    for page in graph:
      newrank = (1-d)/npages
      for node in graph:
        if page in graph[node]:
          newrank = newrank + d*(ranks[node]/len(graph[node]))
      newranks[page] = newrank
    ranks = newranks
  return ranks

def lucky_search(index,ranks,keyword):
  pages = lookup(index,keyword)
  if not pages:
    return None
  best_page = pages[0]
  for candidate in pages:
    if ranks[candidate] > ranks[best_page]:
      best_page = candidate
  return best_page

def ordered_search(index,ranks,keyword):
  pages = lookup(index,keyword)
  return quicksort_pages(pages,ranks)

def quicksort_pages(pages,ranks):
  if not pages or len(pages) <= 1:
    return pages
  else :
    pivot = ranks[pages[0]]
    worse = []
    better = []
    for page in pages[1:]:
      if ranks[page] <= pivot:
        worse.append(page)
      else :
        better.append(page)
    return quicksort_pages(better,ranks) + [pages[0]] + quicksort_pages(worse,ranks)

def fibo(n):
  if n ==1 or n ==0:
    return n
  else :
    return cached_execution(cache,fibo,n-1) + cached_execution(cache,fibo,n-2)

#print time_execution('lookup(index_time[0],"is")')
#words = get_page('http://www.gutenberg.org/cache/epub/1661/pg1661.txt').split()

#counts = test_hash_function(hash_string,words,52)
#print counts

