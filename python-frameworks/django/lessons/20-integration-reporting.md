# 📘 Django Phase 02 — Lesson 10: Integration — Advanced Querying & Reporting

> 🎯 **Goal**: Build a complete reporting system combining everything from Phase 02: QuerySets, field lookups, aggregation, F/Q, relationships, and custom managers.

## 📖 Concepts

### What We're Building
A **Dashboard Report** that computes:
- Published/draft counts
- Top posts by engagement
- Author productivity summaries
- Monthly activity
- Category breakdown
- Custom business metrics

### Design Pattern: Manager + QuerySet + Reports

```
Data (models) → Custom Managers (scoping) → QuerySet Methods (chaining) → Reports (aggregation)
```

### The Reporter Class Pattern
```python
class ReportManager(models.Manager):
    def summary_by_author(self):
        """Aggregates per-author stats."""
        return self.values('author').annotate(
            total_posts=Count('id'),
            total_likes=Sum('likes'),
            avg_likes=Avg('likes'),
        ).order_by('-total_likes')

    def monthly_report(self, year):
        """Posts per month for a given year."""
        return self.filter(
            published_date__year=year
        ).dates('published_date', 'month')
```

### Metrics to Track
```
Engagement Ratio = likes / views × 100
Author Output = total_posts, total_likes, avg_likes
Content Health = published vs draft ratio
Category Distribution = posts, likes, views per category
Period Activity = posts per month
```

### ADHD-Friendly Summary
```
Custom Manager + QuerySet → reusable query building blocks
Report methods → aggregate data for dashboards
All Phase 02 concepts combine here:
  filter, exclude, F(), Q()
  aggregate, annotate
  select_related, prefetch_related
  values(), order_by()
```

## 🛠️ Code (Integration)

The full integration (`20-integration-reporting.py`) demonstrates:

```python
class ReportManager(Manager):
    def summary_by_author(self) -> list[dict]:
        return self.values('author').annotate(
            total_posts=Count('id'),
            total_likes=Sum('likes'),
            avg_likes=Avg('likes'),
        ).order_by('-total_likes')

    def monthly_report(self, year: int) -> list:
        return self.filter(
            published_date__startswith=str(year)
        ).dates('published_date', 'month')

# Dashboard
report = ReportManager(POSTS)

published_count = PublishedManager(POSTS).all().count()
draft_count = qs.filter(is_published=False).count()

top_posts = qs.filter(is_published=True).order_by('-likes')[:5]

author_summary = report.summary_by_author()
monthly = report.monthly_report(2024)
```

### Reports Generated

1. **Published/Draft Count** — content health overview
2. **Top Posts by Likes** — most engaging content
3. **Author Summary** — who's producing what
4. **Monthly Activity** — publishing cadence
5. **Engagement Ratio** — likes/views as percentage
6. **Comments per Post** — community interaction
7. **Category Breakdown** — content distribution
8. **Popular Drafts** — Q expression to find unpublished gems
9. **Author Role Report** — editors vs writers output
10. **Annotated Titles** — computed column example

## 🧪 Practice

Models: `Author`, `Post`, `Comment`, `Category`

1. Build a `DashboardManager` with `.author_report()`, `.category_report()`, `.trending(threshold)`
2. Create a report showing: author name, total posts, total likes, last post date
3. Find posts with high likes but low views (potential hidden gems)
4. Build a rolling 30-day publishing streak report
5. Create an "author score" = (likes × 2 + views × 0.1) / post_count

## 🧠 Key Takeaways

- All ORM techniques compose: filter + annotate + order_by + values = powerful reports
- Custom managers keep report logic reusable and testable
- `values()` + `annotate()` replaces SQL GROUP BY for aggregations
- Q expressions unlock complex filtering (hidden gems, popular drafts)
- Annotations add computed columns without raw SQL
- Prefetch related data in reports to avoid N+1 in templates
