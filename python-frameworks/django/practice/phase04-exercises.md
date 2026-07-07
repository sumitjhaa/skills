# 🏋️ Django Practice — Phase 04 (DRF)

## 1. 🟢 Serializers
Create a `BookSerializer` (ModelSerializer) for a `Book` model with fields: `id`, `title`, `author`, `published_date`, `is_available`. Add validation: title must be 3+ chars, published_date cannot be in the future. Serialize a queryset with `many=True`.

## 2. 🟡 APIView
Create a `BookList` APIView with GET (list all) and POST (create). Create a `BookDetail` APIView with GET, PUT, DELETE. Return proper status codes (201 on create, 204 on delete, 400 on validation error).

## 3. 🟡 Generic Views
Rewrite the Book views using `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView`. Override `perform_create` to set `added_by = request.user`.

## 4. 🟡 ViewSets
Create a `BookViewSet(ModelViewSet)` with `queryset` and `serializer_class`. Add a `@action(detail=True, methods=['post'])` called `checkout` that sets `is_available=False`. Add a `@action(detail=False)` called `available` that returns only available books.

## 5. 🟡 Router
Create a `DefaultRouter`, register `BookViewSet` with basename=`book`. Verify the generated URL patterns. List them.

## 6. 🔴 Permissions
Create permission classes:
- `IsOwner` — only the user who added the book can edit/delete
- `IsAvailableOrReadOnly` — anyone can read, but only when `is_available=True`
- `IsLibrarian` — only staff can create books
Apply them to the BookViewSet.

## 7. 🟡 Pagination
Set up `PageNumberPagination` with `page_size=4` on the Book view. Test with `?page=2&page_size=2`. Add `LimitOffsetPagination` in a second view.

## 8. 🟡 Filtering & Search
Add `DjangoFilterBackend` with `filterset_fields = ['author', 'is_available']`. Add `SearchFilter` with `search_fields = ['title']`. Add `OrderingFilter` with `ordering_fields = ['published_date', 'title']`.

## 9. 🟡 Nested Serializers
Create `AuthorSerializer` with nested `books`. Create `BookSerializer` with nested `author` (read-only). Create `BookDetailSerializer` with nested `author` and nested `reviews`.

## 10. 🔴 Complete REST API
Build a Library REST API:
- `Author` model (name, bio) + `Book` model (title, author FK, is_available, added_by FK)
- `BookViewSet` with full CRUD + checkout/return actions
- `AuthorViewSet` (read-only with nested books)
- Permissions: owner can edit, staff can create, anyone can read
- Pagination: 10/page
- Search: by title, author name
- Throttling: anon 20/min, auth 100/min
- Router at `/api/v1/`
- Test all endpoints
