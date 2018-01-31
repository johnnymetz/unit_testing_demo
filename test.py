from flask_testing import TestCase
from app import app, db, Todo
import unittest


class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Todo(title='Walk the dog', description='Bring treats'))
        db.session.add(Todo(title='YouTube video', description='Flask-Testing demo'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_loads(self):
        """Ensure index page loads correctly."""
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')
        self.assertIn(b'Walk the dog', response.data)
        self.assertEqual(len(self.get_context_variable('todos')), 2)

    def test_add_todo(self):
        """Ensure add item route works correctly."""
        response = self.client.post(
            '/add_todo',
            data=dict(title='Do Laundry', description='Socks in bedroom'),
            follow_redirects=True
        )
        self.assert200(response)
        self.assertMessageFlashed('Todo successfully added!', 'success')
        self.assertIn(b'Do Laundry', response.data)
        self.assertEqual(len(self.get_context_variable('todos')), 3)

    def test_delete_todo(self):
        """Ensure delete item route works correctly."""
        response = self.client.post('/delete_todo/1', follow_redirects=True)
        self.assert200(response)
        self.assertMessageFlashed('Todo successfully deleted!', 'warning')
        self.assertEqual(len(self.get_context_variable('todos')), 1)

    def test_no_todos(self):
        """Ensure index works when there are no todos."""
        Todo.query.delete()
        response = self.client.get('/', follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'You have no Todos.', response.data)
        self.assertEqual(len(self.get_context_variable('todos')), 0)


if __name__ == '__main__':
    unittest.main()
