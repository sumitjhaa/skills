# 🏋️ Django Practice — Phase 01

## 1. 🟢 Project Setup
Create a Django project called `blog_project` with a `posts` app. Verify the server starts with `python manage.py runserver`. List the files created.

## 2. 🟢 Movie Model
Define a `Movie` model with: `title` (CharField), `year` (IntegerField), `rating` (FloatField), `is_watched` (BooleanField). Create and apply migrations. Add `__str__` and `Meta.ordering`.

## 3. 🟡 Movie Admin
Register the `Movie` model in admin with `list_display = ['title', 'year', 'rating']`, `list_filter = ['year', 'is_watched']`, and `search_fields = ['title']`.

## 4. 🟡 Movie List View
Create a `MovieListView` that lists all movies with rating > 7. Use a function-based view and render to a template. Add a URL pattern.

## 5. 🟡 Template with Inheritance
Create a `base.html` with nav bar. Have `movie_list.html` extend it and display movies in a table with title, year, rating.

## 6. 🟡 Movie Form
Create a `MovieForm` (ModelForm) with fields: `title`, `year`, `rating`, `is_watched`. Add a `MovieCreateView` that saves the form and redirects.

## 7. 🔴 Class-Based Movie Views
Implement full CRUD for Movie using CBVs: `MovieListView`, `MovieDetailView`, `MovieCreateView`, `MovieUpdateView`, `MovieDeleteView`. All with proper URL patterns and templates.

## 8. 🟢 Static Files
Add a CSS file that styles the movie list as a grid. Add a JS file that highlights movies with rating > 9. Use `{% static %}` tag.

## 9. 🟡 URL Namespacing
Put all movie URLs under the `movies/` prefix with `app_name = 'movies'`. Use `{% url 'movies:list' %}` in templates. Verify `reverse('movies:detail', kwargs={'pk': movie.pk})` works.

## 10. 🔴 Complete Blog Integration
Build a mini blog with:
- `Post` model (title, content, category, is_published)
- `Category` model (name, slug) with `prepopulated_fields`
- `PostListView` with pagination (5 per page)
- `PostDetailView` with slug URL
- `PostCreateView` with `ModelForm`
- Admin with `date_hierarchy`, `actions`, `list_filter`
- Base template with nav, footer, and `{% block content %}`
