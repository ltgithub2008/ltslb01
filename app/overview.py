#!/usr/bin/env python3
import funct, sql
import create_db
import os, http.cookies
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('ovw.html')
	
print('Content-type: text/html\n')
if create_db.check_db():
	if create_db.create_table():	
		create_db.update_all()
create_db.update_all_silent()
funct.check_login()

try:
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_id = cookie.get('uuid')
	user = sql.get_user_name_by_uuid(user_id.value)
	users = sql.select_users()
	groups = sql.select_groups()
	token = sql.get_token(user_id.value)
	cmd = "ps ax |grep checker_mas |grep -v grep |wc -l"
	checker_master, stderr = funct.subprocess_execute(cmd)
	cmd = "ps ax |grep checker_worker |grep -v grep |wc -l"
	checker_worker, stderr = funct.subprocess_execute(cmd)
	cmd = "ps ax |grep metrics_master |grep -v grep |wc -l"
	metrics_master, stderr = funct.subprocess_execute(cmd)
	cmd = "ps ax |grep -e 'metrics_worker\|metrics_waf_worker.py' |grep -v grep |wc -l"
	metrics_worker, stderr = funct.subprocess_execute(cmd)
except:
	pass

template = template.render(h2 = 1,
							autorefresh = 1,
							title = "&#27010;&#36848;&#20449;&#24687;",
							role = sql.get_user_role_by_uuid(user_id.value),
							user = user,
							users = users,
							groups = groups,
							metrics_master = ''.join(metrics_master),
							metrics_worker = ''.join(metrics_worker),
							checker_master = ''.join(checker_master),
							checker_worker = ''.join(checker_worker),
							error = stderr,
							token = token)
print(template)											
