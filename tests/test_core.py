
import tempfile
import unittest
from pathlib import Path

from raja_enhancer.config import DEFAULT_CONFIG
from raja_enhancer.processor import build_ffmpeg_command
from raja_enhancer.media import validate_video, find_videos

class CoreTests(unittest.TestCase):
    def test_command_contains_ffmpeg_and_audio(self):
        command = build_ffmpeg_command("input.mp4", "output.mp4", DEFAULT_CONFIG)
        self.assertEqual(command[0], "ffmpeg")
        self.assertIn("-c:a", command)
        self.assertIn("aac", command)

    def test_command_does_not_claim_ai(self):
        command = build_ffmpeg_command("input.mp4", "output.mp4", DEFAULT_CONFIG)
        joined = " ".join(command)
        self.assertNotIn("realesrgan", joined.lower())

    def test_validate_video_rejects_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            validate_video("/path/that/does/not/exist.mp4")

    def test_find_videos_filters_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.mp4").write_bytes(b"x")
            (root / "b.txt").write_text("not video")
            found = find_videos(root)
            self.assertEqual([p.name for p in found], ["a.mp4"])

if __name__ == "__main__":
    unittest.main()
