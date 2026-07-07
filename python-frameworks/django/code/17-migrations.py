"""Migrations deep: detecting model changes and generating migration operations."""


class Field:
    def __init__(self, name: str, ftype: str, **opts):
        self.name = name
        self.ftype = ftype
        self.opts = opts

    def __repr__(self) -> str:
        return f"{self.name}: {self.ftype}"


class ModelMeta:
    """Tracks model schema for migration diffing."""
    def __init__(self, name: str, fields: list[Field], options: dict = None):
        self.name = name
        self.fields = {f.name: f for f in fields}
        self.options = options or {}

    def field_names(self) -> set:
        return set(self.fields.keys())

    def __repr__(self) -> str:
        return f"Model({self.name}, fields={list(self.fields.values())})"


class MigrationOp:
    """Base class for migration operations."""
    pass


class CreateModel(MigrationOp):
    def __init__(self, model: ModelMeta):
        self.model = model

    def __repr__(self) -> str:
        return f"CreateModel({self.model.name}, fields={list(self.model.fields.values())})"


class DeleteModel(MigrationOp):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __repr__(self) -> str:
        return f"DeleteModel({self.model_name})"


class AddField(MigrationOp):
    def __init__(self, model_name: str, field: Field):
        self.model_name = model_name
        self.field = field

    def __repr__(self) -> str:
        return f"AddField({self.model_name}.{self.field})"


class RemoveField(MigrationOp):
    def __init__(self, model_name: str, field_name: str):
        self.model_name = model_name
        self.field_name = field_name

    def __repr__(self) -> str:
        return f"RemoveField({self.model_name}.{self.field_name})"


class AlterField(MigrationOp):
    def __init__(self, model_name: str, field: Field):
        self.model_name = model_name
        self.field = field

    def __repr__(self) -> str:
        return f"AlterField({self.model_name}.{self.field})"


class RenameField(MigrationOp):
    def __init__(self, model_name: str, old_name: str, new_name: str):
        self.model_name = model_name
        self.old_name = old_name
        self.new_name = new_name

    def __repr__(self) -> str:
        return f"RenameField({self.model_name}: {self.old_name} → {self.new_name})"


class RenameModel(MigrationOp):
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name

    def __repr__(self) -> str:
        return f"RenameModel({self.old_name} → {self.new_name})"


def diff_models(old_models: dict[str, ModelMeta], new_models: dict[str, ModelMeta]) -> list[MigrationOp]:
    """Generate migration ops by diffing old and new model schemas."""
    ops: list[MigrationOp] = []
    old_names = set(old_models.keys())
    new_names = set(new_models.keys())

    for name in new_names - old_names:
        ops.append(CreateModel(new_models[name]))

    for name in old_names - new_names:
        ops.append(DeleteModel(name))

    for name in old_names & new_names:
        old = old_models[name]
        new = new_models[name]
        old_fields = old.field_names()
        new_fields = new.field_names()

        for fname in new_fields - old_fields:
            ops.append(AddField(name, new.fields[fname]))
        for fname in old_fields - new_fields:
            ops.append(RemoveField(name, fname))
        for fname in old_fields & new_fields:
            if old.fields[fname].ftype != new.fields[fname].ftype:
                ops.append(AlterField(name, new.fields[fname]))

        old_opts = old.options
        new_opts = new.options
        if old_opts.get("db_table") != new_opts.get("db_table"):
            ops.append(RenameModel(old.name, new.name) if new.name != old.name else None)

    return [op for op in ops if op is not None]


# --- Simulation ---
print("=== Initial Schema: CreateModel ===")
v1 = {
    "Post": ModelMeta("Post", [
        Field("id", "AutoField", primary_key=True),
        Field("title", "CharField", max_length=200),
        Field("content", "TextField"),
        Field("author", "ForeignKey", to="Author"),
    ]),
    "Author": ModelMeta("Author", [
        Field("id", "AutoField", primary_key=True),
        Field("name", "CharField", max_length=100),
    ]),
}
ops = diff_models({}, v1)
for op in ops:
    print(f"  {op}")

print("\n=== V2: Add fields, remove fields ===")
v2 = {
    "Post": ModelMeta("Post", [
        Field("id", "AutoField", primary_key=True),
        Field("title", "CharField", max_length=200),
        Field("content", "TextField"),
        Field("author", "ForeignKey", to="Author"),
        Field("likes", "IntegerField", default=0),
        Field("is_published", "BooleanField", default=False),
    ]),
    "Author": ModelMeta("Author", [
        Field("id", "AutoField", primary_key=True),
        Field("name", "CharField", max_length=100),
        Field("email", "EmailField"),
    ]),
    "Category": ModelMeta("Category", [
        Field("id", "AutoField", primary_key=True),
        Field("name", "CharField", max_length=50),
    ]),
}
ops = diff_models(v1, v2)
for op in ops:
    print(f"  {op}")

print("\n=== V3: Rename model, alter field type ===")
v3 = {
    "Article": ModelMeta("Article", [
        Field("id", "AutoField", primary_key=True),
        Field("headline", "CharField", max_length=300),
        Field("body", "TextField"),
        Field("author", "ForeignKey", to="Author"),
        Field("likes", "IntegerField", default=0),
        Field("is_published", "BooleanField", default=False),
    ]),
    "Author": ModelMeta("Author", [
        Field("id", "AutoField", primary_key=True),
        Field("name", "CharField", max_length=100),
        Field("email", "EmailField"),
    ]),
    "Category": ModelMeta("Category", [
        Field("id", "AutoField", primary_key=True),
        Field("name", "CharField", max_length=50),
    ]),
}
ops = diff_models(v2, v3)
for op in ops:
    print(f"  {op}")
