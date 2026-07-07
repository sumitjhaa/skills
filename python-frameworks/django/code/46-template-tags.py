"""Custom template tags & filters: simple_tag, inclusion_tag, filters."""
from typing import Any, Optional
from datetime import datetime, timedelta
import random


# ======================== Template & Context Simulation ========================

class Context(dict):
    """Simulates Django template Context."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autoescape = True
        self.use_l10n = False


class Template:
    """Simple template renderer for testing tags."""
    def __init__(self, template_string: str):
        self.template_string = template_string

    def render(self, context: Context) -> str:
        return self.template_string


# ======================== Template Tag Library ========================

class Library:
    """Simulates Django's template.Library for registering tags/filters."""
    def __init__(self):
        self.tags: dict[str, Any] = {}
        self.filters: dict[str, Any] = {}

    def simple_tag(self, func=None, *, name: str = None):
        """Register a simple template tag (returns a string)."""
        def decorator(f):
            tag_name = name or f.__name__.replace("_", "-")
            self.tags[tag_name] = f
            return f
        return decorator(func) if func else decorator

    def inclusion_tag(self, template_name: str):
        """Register an inclusion tag (renders a partial template)."""
        def decorator(f):
            self.tags[f.__name__.replace("_", "-")] = {
                "fn": f,
                "template": template_name,
                "type": "inclusion",
            }
            return f
        return decorator

    def filter(self, func=None, *, name: str = None, is_safe: bool = False):
        """Register a template filter."""
        def decorator(f):
            filter_name = name or f.__name__
            self.filters[filter_name] = {"fn": f, "is_safe": is_safe}
            return f
        return decorator(func) if func else decorator


register = Library()


# ======================== Custom Filters ========================

@register.filter
def pluralize(value, variants: str = "s"):
    """Returns plural suffix if value != 1. Usage: {{ count|pluralize:'ies' }}"""
    if value != 1:
        return variants
    return ""


@register.filter(name="truncate_words", is_safe=True)
def truncate_words(value: str, max_words: int = 10) -> str:
    """Truncate text to N words."""
    words = value.split()
    if len(words) <= max_words:
        return value
    return " ".join(words[:max_words]) + "..."


@register.filter
def time_ago(value: datetime) -> str:
    """Humanize a datetime: '3 hours ago', 'just now'."""
    delta = datetime.now() - value
    seconds = delta.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        mins = int(seconds // 60)
        return f"{mins} minute{'s' if mins != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


@register.filter
def star_rating(value: float, max_stars: int = 5) -> str:
    """Convert numeric rating to star HTML."""
    full = int(value)
    half = 1 if value - full >= 0.5 else 0
    empty = max_stars - full - half
    return "★" * full + "½" * half + "☆" * empty


# ======================== Custom Simple Tags ========================

@register.simple_tag
def current_year() -> str:
    """Returns the current year. Usage: {% current_year %}"""
    return str(datetime.now().year)


@register.simple_tag(name="random_quote")
def random_quote() -> str:
    """Returns a random quote. Usage: {% random_quote %}"""
    quotes = [
        "The only way to do great work is to love what you do.",
        "Innovation distinguishes between a leader and a follower.",
        "Stay hungry, stay foolish.",
        "Think different.",
    ]
    return random.choice(quotes)


@register.simple_tag
def url_replace(request, field: str, value: str) -> str:
    """Replace a query param in current URL. Usage: {% url_replace request 'page' 2 %}"""
    params = dict(request.get("GET", {}))
    params[field] = value
    return "&".join(f"{k}={v}" for k, v in params.items())


# ======================== Inclusion Tag ========================

@register.inclusion_tag("recent_posts.html")
def show_recent_posts(count: int = 5):
    """Renders a list of recent posts. Usage: {% show_recent_posts 3 %}"""
    posts = [
        {"title": "Hello Django", "date": datetime.now() - timedelta(hours=2)},
        {"title": "DRF Guide", "date": datetime.now() - timedelta(days=1)},
        {"title": "Python Tips", "date": datetime.now() - timedelta(days=3)},
        {"title": "Advanced ORM", "date": datetime.now() - timedelta(weeks=1)},
    ]
    return {"recent_posts": posts[:count]}


# ======================== Demo ========================
print("=== Custom Template Tags & Filters Demo ===\n")

# --- Filter demos ---
print("1. Filters:")
print(f"   pluralize(1, 's'): '{pluralize(1, 's')}'")
print(f"   pluralize(3, 's'): '{pluralize(3, 's')}'")
print(f"   pluralize(1, 'ies'): '{pluralize(1, 'ies')}'")
print(f"   pluralize(3, 'ies'): '{pluralize(3, 'ies')}'")

text = "This is a very long article about Django framework and its many features"
print(f"   truncate_words('{text}', 4): '{truncate_words(text, 4)}'")

dt = datetime.now() - timedelta(hours=3)
print(f"   time_ago(3 hours ago): '{time_ago(dt)}'")
print(f"   star_rating(4.5): '{star_rating(4.5)}'")
print(f"   star_rating(3.0): '{star_rating(3.0)}'")

# --- Simple tag demos ---
print(f"\n2. Simple tags:")
print(f"   current_year: {current_year()}")
print(f"   random_quote: \"{random_quote()}\"")

request = {"GET": {"page": "1", "sort": "title"}}
print(f"   url_replace (page=3): {url_replace(request, 'page', '3')}")

# --- Inclusion tag ---
print(f"\n3. Inclusion tag (show_recent_posts 3):")
result = show_recent_posts(3)
print(f"   Template: {result['template'] if isinstance(register.tags['show-recent-posts'], dict) and 'template' in register.tags['show-recent-posts'] else 'recent_posts.html'}")
print(f"   Posts: {len(result['recent_posts'])}")
for post in result['recent_posts']:
    print(f"     - {post['title']} ({time_ago(post['date'])})")

# --- Registered tags & filters ---
print(f"\n4. Registered custom tags: {list(register.tags.keys())}")
print(f"   Registered custom filters: {list(register.filters.keys())}")
