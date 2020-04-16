import yaml
import cached_url
from bs4 import BeautifulSoup

def get_images(filename):
	with open(filename) as f:
		meta = yaml.load(f, Loader=yaml.FullLoader)
	if meta.get('images'):
		return meta.get('images')
	if 't.me' not in meta['detail_link']:
		return []
	BeautifulSoup(cached_url.get(meta['detail_link']), 'html.parser')

