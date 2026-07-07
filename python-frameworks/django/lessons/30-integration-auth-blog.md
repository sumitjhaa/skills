# 📘 Django Phase 03 — Lesson 10: Integration — Auth Blog

> 🎯 **Goal**: Build a complete blog with authentication — login-required views, per-user content, and permission-based publishing.

## 📖 Concepts

### What We're Building
A blog where:
- Anyone can **view published** posts
- Logged-in users can **create posts**
- Users can only **edit their own posts**
- Users with `can_publish` permission can **publish posts**
- Anyone can **comment** (if logged in)

### Architecture
```
Auth System         Blog System
├── User model      ├── Post (author FK)
├── authenticate()  ├── Comment (author FK)
├── login/logout    ├── LoginRequired mixins
├── permissions     └── Object-level checks
└── groups
```

### View Authorization Matrix

| View | Auth Required | Permission | Object Check |
|------|-------------|------------|-------------|
| Post list | No | — | — |
| Post detail | No | — | — |
| Create post | Yes | — | — |
| Edit post | Yes | — | Author only |
| Delete post | Yes | `blog.delete_post` | Author or superuser |
| Publish post | Yes | `blog.can_publish` | — |
| Add comment | Yes | — | — |

### Per-User Content Pattern
```python
# Show only user's posts
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'my_posts.html', {'posts': posts})

# Object ownership check
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    # ... process form
```

### Signals for Ownership
```python
# Auto-set author on create
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### ADHD-Friendly Summary
```
Anon: read only
Auth: create + own edit
Perm: publish
Admin: everything
```

## 🛠️ Code

```python
# models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [('can_publish', 'Can publish posts')]

    def can_edit(self, user):
        return user == self.author or user.has_perm('blog.change_post')

# views.py
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'my_posts.html', {'posts': posts})
```

## 🧪 Practice

Build the full auth blog:
1. Models: `Post(author FK)`, `Comment(author FK)`
2. List view: published posts only (anon can see)
3. Create view: `@login_required`, auto-set author
4. Edit view: author-only check, raise `PermissionDenied`
5. Publish view: `@permission_required('blog.can_publish')`
6. My Posts view: filter by `request.user`
7. Test: alice can't edit bob's post, anon gets 302 on create

## 🧠 Key Takeaways

- Always set `post.author = request.user` before saving
- Object-level permission = `post.author == request.user`
- `@permission_required` for admin actions (publish, feature)
- Anonymous users see only published content
- Signals aren't needed here — form_valid() handles author assignment
