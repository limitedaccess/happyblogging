from __future__ import unicode_literals

# Create your models here.
from google.appengine.ext import ndb

class Blog(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    posted = ndb.DateTimeProperty(auto_now_add=True)

