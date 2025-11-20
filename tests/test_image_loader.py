"""Tests for image loading utilities."""

import unittest
import tempfile
import os
from pathlib import Path
from PIL import Image
from src.io.image_loader import get_image_files, load_image


class TestImageLoader(unittest.TestCase):
    """Test image loading functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_dir_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_image(self, filename):
        """Create a test image file."""
        img = Image.new('RGB', (100, 100), color='red')
        filepath = self.test_dir_path / filename
        img.save(filepath)
        return filepath
    
    def test_get_image_files_empty_directory(self):
        """Test getting image files from empty directory."""
        files = get_image_files(self.test_dir)
        self.assertEqual(len(files), 0)
    
    def test_get_image_files_finds_png(self):
        """Test that PNG files are found."""
        self.create_test_image('test.png')
        files = get_image_files(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue('test.png' in files[0])
    
    def test_get_image_files_finds_jpg(self):
        """Test that JPG files are found."""
        self.create_test_image('test.jpg')
        files = get_image_files(self.test_dir)
        self.assertEqual(len(files), 1)
    
    def test_get_image_files_ignores_non_images(self):
        """Test that non-image files are ignored."""
        # Create a text file
        text_file = self.test_dir_path / 'test.txt'
        text_file.write_text('not an image')
        
        # Create an image
        self.create_test_image('test.png')
        
        files = get_image_files(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue('test.png' in files[0])
    
    def test_get_image_files_returns_sorted(self):
        """Test that files are returned sorted."""
        self.create_test_image('b.png')
        self.create_test_image('a.png')
        self.create_test_image('c.png')
        
        files = get_image_files(self.test_dir)
        filenames = [Path(f).name for f in files]
        self.assertEqual(filenames, ['a.png', 'b.png', 'c.png'])
    
    def test_load_image_valid_file(self):
        """Test loading a valid image file."""
        image_path = self.create_test_image('test.png')
        img = load_image(str(image_path))
        self.assertIsNotNone(img)
        self.assertEqual(img.size, (100, 100))
    
    def test_load_image_invalid_file(self):
        """Test loading an invalid image file."""
        invalid_path = self.test_dir_path / 'nonexistent.png'
        img = load_image(str(invalid_path))
        self.assertIsNone(img)
    
    def test_load_image_nonexistent_directory(self):
        """Test getting files from nonexistent directory."""
        files = get_image_files('/nonexistent/directory')
        self.assertEqual(len(files), 0)


if __name__ == '__main__':
    unittest.main()

