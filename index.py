import os
import yaml
from image import get_images, get_image_html_table
from bs4 import BeautifulSoup

def gen_articles():
	with open('articles/meta.yaml') as f:
		articles = yaml.load(f, Loader=yaml.FullLoader)
	output = ['<ul>']
	for article in articles:
		output.append('<li><a href="%s">%s</a></li>' % (article['link'], article['name']))
	output.append('</ul>')
	return BeautifulSoup('\n'.join(output), 'html.parser').find('ul')

def gen_records():
	output = ['<div class="record_show">']
	for dirname in os.listdir('records'):
		if not os.path.isdir('records/%s' % dirname):
			continue
		filename = 'records/%s/meta.yaml' % dirname
		with open(filename) as f:
			meta = yaml.load(f, Loader=yaml.FullLoader)
		output.append('<div>')
		output.append(get_image_html_table(get_images(filename)))
		output.append('<ul>')
		output.append('<li>罪犯: %s</li>' % meta['offender'])
		# TODO: support other social accounts
		output.append('<li>微信号: %s</li>' % meta['wechat_id'])
		output.append('<li>标签: %s</li>' % ' '.join(meta['tags']))
		output.append('<li><a href="%s">详细信息</a></li>' % meta['detail_link'])
		output.append('</ul>')
		output.append('</div>')
		output.append('<hr>')
	output.append('</div>')
	return BeautifulSoup('\n'.join(output), 'html.parser').find('div')
	
def gen_index():
	with open('index.html') as f:
		soup = BeautifulSoup(f.read(), 'html.parser')

	articles = soup.find('ul')
	articles.replace_with(gen_articles())

	records = soup.find('div', class_='record_show')
	records.replace_with(gen_records())

	with open('index.html', 'w') as f:
		f.write(str(soup))