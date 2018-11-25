import unittest
import app

class TestingTest(unittest.TestCase):
    def test_root(self):
        self.app = app.app.test_client()
        out = self.app.get('/')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_home(self):
        self.app = app.app.test_client()
        out = self.app.get('/home')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_get_beat(self):
        self.app = app.app.test_client()
        out = self.app.get('/home/<string:name>/<string:beat>')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_genre(self):
        self.app = app.app.test_client()
        out = self.app.get('/genre')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_get_genre(self):
        self.app = app.app.test_client()
        out = self.app.get('/genre/<string:name>')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_get_beat_for_genre(self):
        self.app = app.app.test_client()
        out = self.app.get('/genre/<string:genre>/<string:beat>')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_beatmaker(self):
        self.app = app.app.test_client()
        out = self.app.get('/beatmaker')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_get_beatmaker(self):
        self.app = app.app.test_client()
        out = self.app.get('/beatmaker/<string:name')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_get_beat_for_beatmaker(self):
        self.app = app.app.test_client()
        out = self.app.get('/beatmaker/<string:name>/<string:beat>')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

    def test_contact(self):
        self.app = app.app.test_client()
        out = self.app.get('/contact')
        assert '200 OK' or '302 FOUND' in out.status
        assert 'charset=utf-8' in out.content_type
        assert 'text/html' in out.content_type

if __name__ == "__main__":
    unittest.main ()
