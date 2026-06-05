from __future__ import annotations

import unittest

from cultural_memory_reddit.records import sanitize_listing_child


class TestSanitizeListingChild(unittest.TestCase):
    def test_keeps_limited_public_video_metadata(self) -> None:
        record = sanitize_listing_child(
            {
                "data": {
                    "id": "abc123",
                    "subreddit": "youtubehaiku",
                    "title": "old viral moment resurfaces",
                    "permalink": "/r/youtubehaiku/comments/abc123/example/",
                    "url": "https://youtu.be/example",
                    "created_utc": 1780668000,
                    "score": 120,
                    "over_18": False,
                    "is_self": False,
                    "is_gallery": False,
                    "post_hint": "rich:video",
                    "author": "not stored",
                }
            }
        )

        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record["post_id"], "abc123")
        self.assertEqual(record["source"], "reddit")
        self.assertEqual(record["subreddit"], "youtubehaiku")
        self.assertEqual(record["created_utc"], "2026-06-05T14:00:00+00:00")
        self.assertNotIn("author", record)

    def test_drops_self_gallery_image_and_unapproved_hosts(self) -> None:
        base = {
            "id": "abc123",
            "subreddit": "x",
            "title": "x",
            "permalink": "/r/x/comments/abc123/example/",
            "created_utc": 1780682400,
            "score": 1,
        }
        cases = [
            {**base, "url": "https://youtu.be/x", "is_self": True},
            {**base, "url": "https://youtu.be/x", "is_gallery": True},
            {**base, "url": "https://i.imgur.com/x.jpg", "post_hint": "image"},
            {**base, "url": "https://example.com/x", "post_hint": "rich:video"},
        ]
        for data in cases:
            with self.subTest(data=data):
                self.assertIsNone(sanitize_listing_child({"data": data}))


if __name__ == "__main__":
    unittest.main()
