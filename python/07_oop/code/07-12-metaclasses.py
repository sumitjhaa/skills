"""07-12-metaclasses.py — ORM-style: Metaclass auto-generating table names."""

class ModelMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)

        snake = "".join("_" + c if c.isupper() else c for c in name).lower().lstrip("_")
        namespace["__tablename__"] = namespace.get("__tablename__", snake)

        print(f"[Meta] Created {name} → table {namespace['__tablename__']}")
        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self) -> str:
        fields = [k for k in self.__dict__]
        values = [str(v) for v in self.__dict__.values()]
        return f"INSERT INTO {self.__tablename__} ({', '.join(fields)}) VALUES ({', '.join(values)})"


class User(Model):
    __tablename__ = "users"


class BlogPost(Model):
    pass  # table name auto-generated as "blog_post"


user = User(id=1, name="Alice", email="alice@example.com")
print(user.save())

post = BlogPost(title="My First Post", author="Alice")
print(post.save())
print(f"Post table: {BlogPost.__tablename__}")
