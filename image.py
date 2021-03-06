import yaml
import cached_url
from bs4 import BeautifulSoup
import math
import os

def get_single_image(image):
	return '<img width="300" src="' + image + '" style="max-width:100%;" align="top">'

def get_image_line(images, width):
	result = ['|' + get_single_image(x) for x in images]
	result.append(('|  ' * (width + 1 - len(images))).strip())
	return ''.join(result)

def get_single_html_image(image):
	return '<a href="' + image + '"><img width="150" src="' + image + \
		'" style="max-width:100%;margin-right:10px;margin-top:10px;margin-bottom:10px" align="top"></a>'

def get_image_html_table(images):
	return ''.join([get_single_html_image(image) for image in images])

def get_image_table(images):
	size = len(images)
	width = min(3, size)
	if size == 4:
		width = 2
	result = [get_image_line(images[:width], width)]
	result.append('|-------------' * width + '|')
	for line_number in range(1, math.ceil(1.0 * size / width)):
		result.append(get_image_line(
			images[line_number * width : (line_number + 1) * width], width))
	return '\n'.join(result)

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

def save_to_local(images):
	for image in images:
		cached_url.get(image, force_cache=True, mode='b')
		ext = os.path.splitext(image)[1] or '.html'
		fn = cached_url.getFileName(image) + ext
		os.system('cp tmp/%s index_files/' % fn)
		yield 'index_files/' + fn

def get_images(filename):
	with open(filename) as f:
		meta = yaml.load(f, Loader=yaml.FullLoader)
	# if meta.get('images'):
	# 	return meta.get('images')
	if 't.me' not in meta['detail_link']:
		return []
	images = get_images_from_telegram_url(meta['detail_link'])
	meta['images'] = list(save_to_local(images))
	with open(filename, 'w') as f:
		f.write(yaml.dump(meta, sort_keys=True, indent=2, allow_unicode=True))
	return meta.get('images')


