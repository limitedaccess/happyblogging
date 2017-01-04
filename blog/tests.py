#from django.test import TestCase
import unittest
from webtest import TestApp

# 
# uncomment to run unit test by 'python blog/tests.py'
# otherwise use runner file to run the unit test
#
# [Start Path fix]
import dev_appserver
dev_appserver.fix_sys_path()
# [End Path fix]

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from happyblogging.wsgi import application
from blog.models import Blog

class BlogViewTestCase(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(application)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.setupUser()

        ndb.get_context().clear_cache()

    def setupUser(self, email="test@test.com", user_id="123", is_admin=False):
        self.testbed.setup_env(
                user_email=email,
                user_id=user_id,
                user_is_admin='1' if is_admin else '0',
                overwrite=True)

    def tearDown(self):
        self.testbed.deactivate()
    
    def testBlogModel(self):
        blog = Blog(author="test@test.com", title="test", slug="test-slug", content="testContent")
        blog.put()
        self.assertEqual(1, len(Blog.query().fetch(2)))

    def testIndexView(self):
        result = self.testapp.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertNotIn("test-title", result.body)
        blog = Blog(author="test@test.com", title="test-title", slug="test-slug", content="testContent")
        blog.put()
        result = self.testapp.get('/')
        self.assertIn("test-title", result.body)

    def testCreateBlog(self):
        result = self.testapp.get('/blog/create')
        form = result.form
        form['title'] = 'test-title'
        form['slug'] = 'test-slug'
        form['content'] = 'test-content'
        form.submit()
        self.assertEqual(1, len(Blog.query().fetch(2)))
        result = self.testapp.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn("test-title", result.body)

    def testBlogDetail(self):
        blog = Blog(author="test@test.com", title="test-title2", slug="test-slug", content="testContent")
        blog.put()
        result = self.testapp.get('/blog/' + str(blog.key.id()) +'/')
        self.assertIn("test-title2", result.body)


if __name__ == '__main__':
	unittest.main()
        
    
