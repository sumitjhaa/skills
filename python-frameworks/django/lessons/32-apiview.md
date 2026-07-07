# 📘 Django Phase 04 — Lesson 02: APIView & Request Handling

> 🎯 **Goal**: Use DRF's `APIView` for explicit request handling with status codes and `Response`.

## 📖 Concepts

### APIView
`APIView` is DRF's base class for views. Like Django's `View` but with:
- Built-in `Request` object (parsed JSON, query params)
- `Response` object (serializable to JSON)
- Content negotiation
- Authentication / permission integration

### Method Handlers
```python
class PostList(APIView):
    def get(self, request):      # GET /posts/
    def post(self, request):     # POST /posts/

class PostDetail(APIView):
    def get(self, request, pk):    # GET /posts/:id/
    def put(self, request, pk):    # PUT /posts/:id/
    def patch(self, request, pk):  # PATCH /posts/:id/
    def delete(self, request, pk): # DELETE /posts/:id/
```

### Request Object

| Attribute | Description |
|-----------|-------------|
| `request.data` | Parsed request body (dict) |
| `request.query_params` | GET params (like `request.GET`) |
| `request.user` | Authenticated user |
| `request.auth` | Auth token |
| `request.method` | HTTP method string |

### Response & Status Codes
```python
from rest_framework.response import Response
from rest_framework import status

Response(data, status=status.HTTP_201_CREATED)
Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
Response(data, status=status.HTTP_204_NO_CONTENT)
```

### ADHD-Friendly Summary
```
APIView → class-based, explicit methods
request.data → parsed body
Response(data, status=N) → JSON response
405 if method handler missing
```

## 🛠️ Code

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## 🧪 Practice

1. Create a `BookList` APIView with GET (list) and POST (create)
2. Create a `BookDetail` APIView with GET, PUT, DELETE
3. Return proper status codes everywhere
4. Handle 404 with `get_object_or_404`
5. Add query param filtering: `GET /books/?author=alice`

## 🧠 Key Takeaways

- `APIView` gives full control over request/response cycle
- Always use DRF `status` constants instead of raw ints
- `request.data` handles JSON, form data, multipart automatically
- Missing method handler = 405 Method Not Allowed
- Use `get_object_or_404` for detail views
