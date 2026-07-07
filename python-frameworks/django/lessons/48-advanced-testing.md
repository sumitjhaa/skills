# 📘 Django Phase 05 — Lesson 08: Advanced Testing

> 🎯 **Goal**: Write robust tests with factories, mocking, TDD, and coverage analysis.

## 📖 Concepts

### Test Pyramid
```
     /\
    /  \        UI / E2E (few)
   /    \
  /______\      Integration (some)
 /________\    Unit tests (many — fast!)
```

### Factory Boy vs Fixtures

| Approach | Pros | Cons |
|----------|------|------|
| `fixtures.json` | Simple, portable | Brittle, hard to maintain |
| `Factory Boy` | Flexible, readable | More setup |

### Factory Example
```python
# factories.py
import factory
from .models import Post

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ('slug',)

    title = factory.Faker('sentence')
    slug = factory.Faker('slug')
    content = factory.Faker('paragraph')
    author = factory.SubFactory('users.factories.UserFactory')
```

### Mocking
Replace external services during testing:

```python
from unittest.mock import patch

@patch('myapp.tasks.send_email.delay')
def test_register_sends_email(mock_send_email):
    response = self.client.post('/register/', {'email': 'a@b.com'})
    assert mock_send_email.called_once_with('a@b.com')
```

### Client Test Patterns

| Pattern | Test | Code |
|---------|------|------|
| GET | Status + content | `self.client.get('/url/')` |
| POST | Create + redirect | `self.client.post('/url/', data)` |
| Auth | Login + test | `self.client.login(username='alice', password='x')` |
| Assert | Template used | `assertTemplateUsed(response, 'template.html')` |
| Assert | Contains | `assertContains(response, 'Hello')` |

### Coverage
```bash
coverage run --source='.' manage.py test myapp
coverage report
coverage html  # open htmlcov/index.html
```

### ADHD-Friendly Summary
```
Factory Boy → flexible test data
unittest.mock → patch external calls
self.client → Django test client simulates browser
coverage run → measure what's tested
TDD: red → green → refactor
```

## 🛠️ Code

```python
# tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .factories import PostFactory, UserFactory

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_post_list_shows_published(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    @patch('myapp.tasks.send_notification.delay')
    def test_create_post_triggers_notification(self, mock_task):
        self.client.force_login(self.user)
        response = self.client.post(reverse('post-create'), {
            'title': 'Test', 'content': 'Content'
        })
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(mock_task.called)
```

## 🧪 Practice

1. Create a `PostFactory` with Faker-generated title and content
2. Write a test for `LoginRequiredMixin` — unauthenticated user gets 302
3. Mock an external API call in a test
4. Use `self.client.login()` then test a POST view
5. Run coverage and find untested lines

## 🧠 Key Takeaways

- Factories are more flexible than fixtures for test data
- Mock external calls (email, API, payments) to keep tests fast
- `setUp()` runs before each test — use it to create common objects
- Test behavior, not implementation
- Aim for 80%+ coverage on business logic; 100% on critical paths
- TDD: write the test first, then the implementation
