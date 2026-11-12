import tempfile
import unittest
from pathlib import Path

from ninecirc.store import LocalStore


class StoreTests(unittest.TestCase):
    def test_add_is_idempotent_and_remove_keeps_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            repo = base / "sample"
            repo.mkdir()
            store = LocalStore(base / "state")
            self.assertEqual(store.add_repository(repo)["path"], store.add_repository(repo)["path"])
            self.assertEqual(len(store.repositories), 1)
            self.assertTrue(store.remove_repository(str(repo)))
            self.assertTrue(repo.is_dir())
            self.assertEqual(store.repositories, [])

    def test_local_events_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            store = LocalStore(Path(temp) / "state")
            store.append_event("test", "Local event")
            events = store.read_events()
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["type"], "test")
            self.assertEqual(events[0]["message"], "Local event")


if __name__ == "__main__":
    unittest.main()
