import os
from readme import gen_readme
from index import gen_index

gen_readme()
gen_index()
os.system('git add . > /dev/null 2>&1 && git commit -m commit > /dev/null 2>&1 && git push -u -f > /dev/null 2>&1')



