# 📘 Django Phase 05 — Lesson 06: Custom Template Tags & Filters

> 🎯 **Goal**: Extend Django templates with custom tags and filters for reusable presentation logic.

## 📖 Concepts

### Why Custom Tags?
Template tags keep logic out of templates. When `{{ post.created_at|time_ago }}` is cleaner than formatting dates in every view.

### Tag Types

| Type | Register | Returns | Use Case |
|------|----------|---------|----------|
| **Filter** | `@register.filter` | Modified value | `{{ value|filter:arg }}` |
| **Simple tag** | `@register.simple_tag` | String | `{% current_year %}` |
| **Inclusion tag** | `@register.inclusion_tag` | Context dict | `{% show_posts 5 %}` |
| **Assignment tag** | `@register.simple_tag` (with `as`) | Set variable | `{% get_posts as posts %}` |

### Template Filter Rules
```python
@register.filter
def pluralize(value, variants="s"):
    """{{ count|pluralize:'ies' }} → 3 comments, 1 comment"""
    if value != 1:
        return variants
    return ""

@register.filter(is_safe=True)
def truncate_words(value, max_words=10):
    """Safe = won't escape HTML output"""
```

### Inclusion Tag
```python
@register.inclusion_tag('blog/recent_posts.html')
def show_recent_posts(count=5):
    posts = Post.objects.all()[:count]
    return {'recent_posts': posts}
```
The template `blog/recent_posts.html` renders using the returned context.

### Loading Custom Tags
```html
{% load blog_tags %}
{% show_recent_posts 3 %}
{{ post.title|truncate_words:5 }}
```

### ADHD-Friendly Summary
```
@register.filter → value|filter:arg
@register.simple_tag → {% tag arg %}
@register.inclusion_tag → {% tag arg %} (renders partial)
Create templatetags/ directory in your app
```

## 🛠️ Code

```python
# myapp/templatetags/blog_tags.py
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime

register = template.Library()

@register.filter
def time_ago(value):
    delta = datetime.now() - value
    if delta.days > 0:
        return f"{delta.days}d ago"
    return f"{delta.seconds // 3600}h ago"

@register.simple_tag
def current_year():
    return str(datetime.now().year)

@register.inclusion_tag('blog/recent_posts.html')
def show_recent_posts(count=5):
    return {'posts': Post.objects.all()[:count]}

# Usage in template:
{% load blog_tags %}
{% show_recent_posts 3 %}
<p>Copyright {% current_year %}</p>
<p>Posted {{ post.created_at|time_ago }}</p>
```

## 🧪 Practice

1. Create a `star_rating` filter that converts 3.5 → "★★★½☆"
2. Create a `url_replace` simple tag for pagination links
3. Create an inclusion tag `show_comment_count` that displays "3 comments"
4. Create an assignment tag `{% get_popular_posts as popular %}`
5. Add `is_safe=True` to filters that return HTML

## 🧠 Key Takeaways

- Tags live in `myapp/templatetags/` (must have `__init__.py`)
- Load with `{% load module_name %}` (module name = Python file)
- Filters are for value transformation; tags are for logic/output
- `is_safe=True` marks output as safe from auto-escaping
- Use `mark_safe()` when returning HTML from tags
