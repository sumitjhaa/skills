# 🏋️ Django Practice — Phase 05 (Advanced Patterns)

## 1. 🟢 Celery
Create a `send_welcome_email` task that accepts a user email. Call it with `.delay()` from a registration view. Add a `process_report` task with `max_retries=3` and `countdown=60`.

## 2. 🟡 Caching
Set up Redis as the cache backend. Cache a slow DB query with `cache.get_or_set()`. Add `@cache_page(60)` to a view. Bust the cache via `post_save` signal.

## 3. 🟡 Signals
Connect `post_save` on `Post` to auto-invalidate the post list cache. Create a custom `post_viewed` signal. Connect it to increment a view counter. Create an `AuditLog` entry on every post save.

## 4. 🟡 Middleware
Create `TimingMiddleware` that logs request duration. Create `AdminOnlyMiddleware` that restricts `/admin/` paths. Create `SecurityHeadersMiddleware` that adds `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.

## 5. 🟡 Management Commands
Create a `generate_sample_data` command with `--users=N --posts=M --flush` flags. Create a `cleanup_temp_files` command with `--days=N --dry-run`.

## 6. 🟡 Template Tags
Create a `star_rating` filter: `{{ rating|star_rating }}` → "★★★★☆". Create a `time_ago` filter: `{{ date|time_ago }}` → "3 hours ago". Create an inclusion tag `show_popular_posts(count=5)`.

## 7. 🟡 File Handling
Add an `ImageField` to your Post model. Generate a thumbnail on save using Pillow. Configure S3 storage with `django-storages`. Validate that uploaded files are < 5MB and are images only.

## 8. 🔴 Advanced Testing
Create a `PostFactory` using factory_boy with Faker. Write tests for: login-required views redirect anon, post creation triggers email task, post list returns 200. Mock the Celery task. Run coverage and report.

## 9. 🟡 Performance
Install `django-debug-toolbar`. Add `select_related('author')` and `prefetch_related('comments')` to a view. Verify query count dropped. Add `db_index` to frequently filtered fields. Replace `len(qs)` with `.count()`.

## 10. 🔴 Full Production Blog
Combine everything:
- Celery: send notification on new post
- Caching: cache post list 15 min, bust on create
- Signals: audit log + view counter
- Middleware: timing + security headers
- Management: `publish_scheduled_posts` command
- Storage: S3 for images + thumbnails
- Testing: factory-based, mock Celery
- Performance: verify with debug-toolbar
