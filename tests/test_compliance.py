from __future__ import annotations

import unittest

from cultural_memory_reddit.compliance import RetentionPolicy, tombstone_record


class TestComplianceHelpers(unittest.TestCase):
    def test_default_policy_is_limited_and_research_focused(self) -> None:
        policy = RetentionPolicy()
        self.assertEqual(policy.delete_unavailable_content_within_hours, 48)
        self.assertFalse(policy.store_author_fields)
        self.assertFalse(policy.store_full_comment_threads_by_default)
        self.assertFalse(policy.train_general_purpose_ai_models)
        self.assertFalse(policy.resell_reddit_data)
        self.assertFalse(policy.build_user_level_marketing_audiences)

    def test_tombstone_record_is_minimal(self) -> None:
        record = tombstone_record("abc123", "deleted_or_unavailable_on_reddit")
        self.assertEqual(record["source"], "reddit")
        self.assertEqual(record["post_id"], "abc123")
        self.assertEqual(record["status"], "deleted_from_research_store")
        self.assertNotIn("title", record)


if __name__ == "__main__":
    unittest.main()

