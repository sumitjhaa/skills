# 🏁 Integration: Task Manager
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Combine all pytest features into a comprehensive test suite for a task manager app.

## The App (task_manager.py)

```python
class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.tasks = storage.load()
    
    def add(self, title, priority="medium"):
        if not title.strip():
            raise ValueError("Title required")
        task = {"id": len(self.tasks) + 1, "title": title,
                "priority": priority, "done": False}
        self.tasks.append(task)
        self.storage.save(self.tasks)
        return task
    
    def complete(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                self.storage.save(self.tasks)
                return task
        raise KeyError(f"Task {task_id} not found")
    
    def list_by_priority(self, priority):
        return [t for t in self.tasks if t["priority"] == priority]
```

## Test Suite

```python
# Fixture for storage mock
@pytest.fixture
def mock_storage(mocker):
    storage = mocker.Mock()
    storage.load.return_value = []
    return storage

@pytest.fixture
def manager(mock_storage):
    return TaskManager(mock_storage)

# Parametrized test
@pytest.mark.parametrize("title, priority", [
    ("Buy milk", "high"),
    ("Read book", "low"),
    ("Write report", "medium"),
])
def test_add(manager, title, priority):
    task = manager.add(title, priority)
    assert task["title"] == title
    assert task["priority"] == priority
    assert not task["done"]

# Exception test
def test_empty_title(manager):
    with pytest.raises(ValueError, match="Title required"):
        manager.add("")

# Mock verification
def test_persists(manager, mock_storage):
    manager.add("Task 1")
    mock_storage.save.assert_called_once()

# Parametrize + fixtures
@pytest.mark.parametrize("completed_id, expected", [
    (1, True),
    (99, False),  # KeyError
])
def test_complete(manager, completed_id, expected):
    manager.add("Test task")
    if expected:
        task = manager.complete(completed_id)
        assert task["done"]
    else:
        with pytest.raises(KeyError):
            manager.complete(completed_id)
```

## Run the Code

```bash
pytest code/15-integration-taskmanager.py -v
```
