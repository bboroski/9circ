import unittest

from ninecirc.system import system_snapshot


class SystemTests(unittest.TestCase):
    def test_snapshot_is_on_demand_and_read_only(self):
        result = system_snapshot()
        for key in ("os", "os_release", "architecture", "logical_cpus", "memory_total", "disk_free", "collection", "mode"):
            self.assertIn(key, result)
        self.assertEqual(result["collection"], "On demand")
        self.assertEqual(result["mode"], "Local / read-only")
        self.assertIsInstance(result["os"], str)


if __name__ == "__main__":
    unittest.main()
