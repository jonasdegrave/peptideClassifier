import requests

from clint.textui import progress

url = 'http://do1.dr-chuck.com/pythonlearn/EN_us/pythonlearn.pdf'

r = requests.get(url, stream=True)

with open("LearnPython.pdf", "wb") as Pypdf:

    total_length = int(r.headers.get('content-length'))

    for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):

        if ch:

            Pypdf.write(ch)