#!/usr/bin/env python3
import os
import sql
import http.cookies
import funct
import sql
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('metrics.html')

print('Content-type: text/html\n')
funct.check_login()

try:
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_id = cookie.get('uuid')
	user = sql.get_user_name_by_uuid(user_id.value)
	token = sql.get_token(user_id.value)
except:
	pass

template = template.render(h2 = 1, title = "&#24230;&#37327;",
							autorefresh = 1,
							role = sql.get_user_role_by_uuid(user_id.value),
							user = user,
							onclick = "metricsShow()",
							table_stat = sql.select_table_metrics(user_id.value),
							token = token)											
print(template)