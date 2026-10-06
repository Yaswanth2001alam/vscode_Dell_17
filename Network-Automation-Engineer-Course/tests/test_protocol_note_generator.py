import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_course.protocol_catalog import PROTOCOLS


GENERATOR_PATH = (
    Path(__file__).resolve().parents[1] / "tools" / "generate_protocol_notes.py"
)
SPEC = importlib.util.spec_from_file_location("generate_protocol_notes", GENERATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load protocol note generator")
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class ProtocolNoteGeneratorTests(unittest.TestCase):
    def test_slugify_is_safe_and_stable(self):
        self.assertEqual(GENERATOR.slugify("802.1X/EAPOL"), "802-1x-eapol")
        self.assertEqual(GENERATOR.slugify("HTTP/HTTPS"), "http-https")

    def test_each_protocol_renders_required_sections(self):
        for protocol in PROTOCOLS:
            with self.subTest(protocol=protocol.name):
                output = GENERATOR.render_protocol(protocol)
                self.assertIn(f"# {protocol.name}", output)
                self.assertIn("## Positive tests", output)
                self.assertIn("## Negative and failure tests", output)
                self.assertIn("## Security tests", output)
                self.assertIn("## Python catalog example", output)

    def test_main_generates_exactly_one_file_per_protocol(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "protocols"
            with patch.object(GENERATOR, "OUTPUT_DIR", output_dir):
                exit_code = GENERATOR.main()

            generated = list(output_dir.glob("layer-*/*.md"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(generated), len(PROTOCOLS))
            self.assertTrue((output_dir / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
