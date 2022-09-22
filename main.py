import os
import re
import urllib.request
from pathlib import Path
from time import sleep

from bs4 import BeautifulSoup


def open_file_and_return_urls(filename: str="list.txt") -> list:
  """
    Opens the file listing the urls to be downloaded.
  """
  try:
    with open(os.path.join(os.path.dirname(__file__), filename), 'rb') as f:
      return f.read().splitlines()
  except:
    print('An error occurred while opening the file.\n')
  
def access_url_and_return_content(url: str):
  """
    Access the url given and retrieve the content
  """
  with urllib.request.urlopen(url) as f:
    html_content = f.read().decode("utf8")
  
  return html_content

def get_link(content: str) -> str:
  """
    Get the link from the html content extracted
  """
  soup = BeautifulSoup(content, 'html.parser')
  link = soup.find("a", id="dlbutton").parent.script.text.strip().split('\n')[0].split('=')[1]
  link_split_brackets = re.split("\(|\)|\[|\]", link)
  eval_from_link = str(eval(link_split_brackets[1]))
  string_with_eval = eval_from_link.join(link_split_brackets[::2])
  remove_plus_operator = "".join(re.split("\+", string_with_eval))
  extracted_link = "".join(re.split('\"', remove_plus_operator)).replace(' ', '')[:-1]

  return "https://www62.zippyshare.com" + extracted_link

def download_anime(url: str, to: str, filename: str) -> None:
  """
    Download anime from the url
  """
  Path(to).mkdir(parents=True, exist_ok=True)
  urllib.request.urlretrieve(url, os.path.join(to, filename))

def main():
  for url in open_file_and_return_urls():
    html_content = access_url_and_return_content(url.decode('utf8'))
    link = get_link(html_content)
    print("Downloading link: " + link)
    download_anime(link, os.path.join(os.path.dirname(__file__), 'videos'), link.split("/")[-1])
    print("Download complete!")
    sleep(10)

if __name__ == '__main__':
  main()
