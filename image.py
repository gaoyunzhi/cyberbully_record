import yaml
import cached_url
from bs4 import BeautifulSoup

def get_images_from_telegram_url(url):
	url = url.replace('t.me/', 't.me/s/')
	relative_url = url.strip('/').split('/')
	relative_url = relative_url[-2] + '/' + relative_url[-1]
	soup = BeautifulSoup(cached_url.get(url), 'html.parser')
	for post in soup.find_all('div', class_='tgme_widget_message'):
		if post['data-post'] != relative_url:
			continue
		for item in post.find_all('a', class_='tgme_widget_message_photo_wrap'):
			yield item['style'].split("background-image:url('")[1].split("')")[0]

def get_images(filename):
	with open(filename) as f:
		meta = yaml.load(f, Loader=yaml.FullLoader)
	if meta.get('images'):
		return meta.get('images')
	if 't.me' not in meta['detail_link']:
		return []
	images = list(get_images_from_telegram_url(meta['detail_link']))
	meta['images'] = images
	with open(filename, 'w') as f:
		f.write(yaml.dump(meta, sort_keys=True, indent=2, allow_unicode=True))


