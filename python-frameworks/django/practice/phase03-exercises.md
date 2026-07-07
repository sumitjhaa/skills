# 🏋️ Django Practice — Phase 03: Auth & Users

## 1. 🟢 Login/Logout
- Create a login view with `authenticate()` + `login()`
- Create a logout view
- Show different navbar for authenticated vs anonymous users
- Handle invalid credentials gracefully (show error message)

## 2. 🟡 Registration & Profile
- Create a `SignUpForm` with validation (username unique, password match, email format)
- Auto-login after signup
- Create a `Profile` model linked to User via OneToOneField
- Auto-create Profile via signal when User is created
- Create a profile edit view (bio, location, avatar)

## 3. 🟡 Permissions
- Protect 3 views with `@login_required`
- Protect 1 view with `@permission_required('blog.add_post')`
- Show/hide UI elements based on `perms` in template
- Test: anonymous → 302, wrong perm → 403, OK → 200

## 4. 🟡 Groups
- Create 3 groups: Editors, Writers, Moderators
- Add custom permissions to each group
- Assign 3 users to different groups
- Verify `user.has_perm()` works for group-inherited permissions

## 5. 🟢 Password Management
- Build a password change form with old/new/confirm fields
- Call `update_session_auth_hash()` after save
- Wire up password reset URLs using Django's built-in views
- Customize the password reset email template

## 6. 🟡 Social Auth
- Install django-allauth
- Configure Google as an OAuth provider
- Add "Login with Google" button
- Handle `user_signed_up` signal to create a profile
- Test: connect a social account and verify `SocialAccount` is created

## 7. 🔴 Custom User Model
- Create a custom User model extending `AbstractUser` with `bio`, `phone`, `location`
- Set `AUTH_USER_MODEL` in settings.py
- Create a superuser and verify admin access
- Reference via `get_user_model()` in a Post ForeignKey
- Compare: when would you use AbstractBaseUser instead?

## 8. 🟡 Email Authentication
- Create a custom `EmailAuthBackend` authenticating by email
- Add it to `AUTHENTICATION_BACKENDS`
- Create a login view using email instead of username
- Create a signup form without username field
- Test all edge cases: wrong email, wrong password, duplicate email

## 9. 🟡 Session & Security
- Store a user preference (theme) in the session
- Verify it persists across requests
- Add `{% csrf_token %}` to a form and test CSRF protection
- Configure session security settings (HTTPOnly, Secure, SameSite)
- Test session fixation prevention (session ID changes after login)

## 10. 🔴 Integration: Auth Blog
Build a complete auth-protected blog:
- `Post` model with author FK and `Meta.permissions`
- `Comment` model with author FK
- Post list: show published posts (anon visible)
- Create post: `@login_required`, auto-set author
- Edit post: author-only check raises `PermissionDenied`
- Publish post: `@permission_required('blog.can_publish')`
- My Posts: filter by `request.user`
- Test all 4 user roles: anon, logged-in, publisher, superuser
