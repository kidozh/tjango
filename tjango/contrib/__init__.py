# for template output
import tornado.template
import os
template_path = os.path.join(os.path.dirname(__file__), "templates")
template_loader = tornado.template.Loader(template_path)

# init configuration then get connect key
from tjango.db import connectHandler

connect = connectHandler()