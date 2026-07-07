# 🏋️ Django Practice — Phase 02: ORM Deep

## 1. 🟢 QuerySet Basics
Given the `Post` model, write:
- A query that returns all published posts
- A query that returns the first draft
- A query that safely gets a post by ID or handles not-found

## 2. 🟡 Field Lookups
Write filters for:
- Posts with "python" in the title (case-insensitive)
- Posts created in January 2024
- Posts with likes between 5 and 20
- Posts where the author field is empty

## 3. 🟡 QuerySet Methods
- Get the 3 most recent posts (title + date only)
- Get unique authors from published posts
- Get all post titles as a flat list
- Get monthly creation dates for 2024

## 4. 🟡 Aggregation
- Get total, average, max, and min likes for published posts
- Annotate each post with the uppercase version of its title
- Get total likes grouped by author
- Get the number of posts per category

## 5. 🔴 F & Q Expressions
- Find posts where likes exceed views
- Increment likes by 2 for all posts by "alice"
- Find posts by "bob" OR posts with 10+ likes (using Q)
- Find posts that are NOT drafts AND have > 0 likes (using Q + ~)
- Build a dynamic query from a list of author names using Q.OR

## 6. 🔴 Relationships
- Fetch all posts with their author in 1 query (select_related)
- Fetch all authors with their posts in 2 queries (prefetch_related)
- Count the N+1 problem: estimate queries for 20 posts with comments
- Write the optimized version that avoids N+1

## 7. 🟢 Migrations
- Create a migration that renames `content` to `body`
- Create a data migration that backfills slugs from titles
- Show the SQL for a migration without running it

## 8. 🟡 Model Inheritance
- Create an abstract `BaseContent` with title and timestamps
- Create `Article(BaseContent)` with body, and `Note(BaseContent)` with priority
- Verify both have title but no BaseContent table
- Create a proxy `ActivePost` that defaults to `is_published=True`

## 9. 🟡 Custom Managers
- Create `PublishedManager` scoping to published posts
- Create `PostQuerySet` with `.popular(n)`, `.by_author(name)`, `.recent(days)`
- Register as_manager() and chain all three methods
- Create `FeaturedManager` with `.trending(threshold)`

## 10. 🔴 Integration: Reporting Dashboard
Build a complete dashboard that:
- Shows published/draft counts
- Lists top 5 posts by engagement (likes/views ratio)
- Groups posts by author with totals
- Shows monthly publishing activity
- Lists popular drafts (unpublished with > N likes)
- Breaks down posts by category with per-category likes/views
- Accepts a date range parameter
