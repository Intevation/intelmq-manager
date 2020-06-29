import unittest
import tempfile
import os
from pathlib import Path

from intelmq_manager.session import SessionStore


class TestSessionStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def test_basic_usage(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"))
        session_data = {"csrf_token": "very-secret"}
        store.set("some-uniqe-id", session_data)
        self.assertTrue(store.exists("some-uniqe-id"))
        self.assertEqual(store.get("some-uniqe-id"), session_data)

    def test_exists_non_existing(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"))
        self.assertFalse(store.exists("some-unknown-id"))

    def test_set_overwriting(self):
        store = SessionStore(os.path.join(self.temp_dir.name, "sessiondb"))
        store.set("just-a-session-id", {"some": "thing"})
        new_data = {"some": "other-thing"}
        store.set("just-a-session-id", new_data)
        self.assertEqual(store.get("just-a-session-id"), new_data)
