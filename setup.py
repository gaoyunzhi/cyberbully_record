import os
import yaml
from image import get_images, get_image_table

output = ['# 网络暴力图鉴\n\n### 文章']

with open('articles/meta.yaml') as f:
	articles = yaml.load(f, Loader=yaml.FullLoader)
for article in articles:
	output.append('* [%s](%s)' % (article['name'], article['link']))

output.append('\n\n### 网络暴力公示')

for dirname in os.listdir('records'):
	if not os.path.isdir('records/%s' % dirname):
		continue
	filename = 'records/%s/meta.yaml' % dirname
	with open(filename) as f:
		meta = yaml.load(f, Loader=yaml.FullLoader)
	output.append(get_image_table(get_images(filename)))
	output.append('* 罪犯: ' + meta['offender'])
	# TODO: support other social accounts
	output.append('* 微信号: ' + meta['wechat_id'])
	output.append('* 标签: ' + ' '.join(meta['tags']))
	output.append('* [详细信息](%s)' % meta['detail_link'])
	output.append('\n\n')

with open('README.md', 'w') as f:
	f.write('\n'.join(output))

os.system('git add . > /dev/null 2>&1 && git commit -m commit > /dev/null 2>&1 && git push -u -f > /dev/null 2>&1')



