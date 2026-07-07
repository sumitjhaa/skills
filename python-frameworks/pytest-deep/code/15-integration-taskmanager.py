"""Integration: Task Manager — combining all pytest features."""
import pytest


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

    def get_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        return {"total": total, "done": done, "pending": total - done}


@pytest.fixture
def mock_storage(mocker):
    storage = mocker.Mock()
    storage.load.return_value = []
    return storage


@pytest.fixture
def manager(mock_storage):
    return TaskManager(mock_storage)


@pytest.mark.parametrize("title, priority", [
    ("Buy milk", "high"),
    ("Read book", "low"),
    ("Write report", "medium"),
])
def test_add_task(manager, title, priority):
    task = manager.add(title, priority)
    assert task["title"] == title
    assert task["priority"] == priority
    assert not task["done"]
    assert task["id"] > 0


def test_empty_title(manager):
    with pytest.raises(ValueError, match="Title required"):
        manager.add("")


def test_add_persists(manager, mock_storage):
    manager.add("Task 1")
    mock_storage.save.assert_called_once()


@pytest.mark.parametrize("task_id, should_succeed", [
    (1, True),
    (99, False),
])
def test_complete_task(manager, task_id, should_succeed):
    manager.add("Test task")
    if should_succeed:
        task = manager.complete(task_id)
        assert task["done"]
    else:
        with pytest.raises(KeyError):
            manager.complete(task_id)


def test_complete_updates_storage(manager, mock_storage):
    manager.add("Task 1")
    mock_storage.save.reset_mock()
    manager.complete(1)
    assert mock_storage.save.call_count == 1


def test_list_by_priority(manager):
    manager.add("Task 1", "high")
    manager.add("Task 2", "low")
    manager.add("Task 3", "high")
    high_tasks = manager.list_by_priority("high")
    assert len(high_tasks) == 2
    assert all(t["priority"] == "high" for t in high_tasks)


def test_stats(manager):
    manager.add("Task 1")
    manager.add("Task 2")
    manager.complete(1)
    stats = manager.get_stats()
    assert stats == {"total": 2, "done": 1, "pending": 1}


@pytest.mark.slow
def test_many_tasks(manager):
    for i in range(100):
        manager.add(f"Task {i}")
    assert len(manager.tasks) == 100
