import unittest
import tempfile
import pathlib
import os
from thumbnail import *


class TestUniqueQueue(unittest.TestCase):
    
    def test_put_and_get(self):
        """Test basic put and get functionality."""
        q = UniqueQueue()
        self.assertTrue(q.empty())
        
        q.put("item1")
        self.assertFalse(q.empty())
        
        item = q.get()
        self.assertEqual(item, "item1")
        self.assertTrue(q.empty())
        q.close()

    def test_uniqueness_enforcement(self):
        """Test that duplicate items are rejected while queued."""
        q = UniqueQueue()
        
        # First put should succeed and return True
        self.assertTrue(q.put("apple"))
        
        # Duplicate put should be blocked and return False
        self.assertFalse(q.put("apple"))
        self.assertEqual(q.qsize(), 1)
        
        # Retrieve the item, which should free it up from tracking
        self.assertEqual(q.get(), "apple")
        
        # Now we should be able to put "apple" back in
        self.assertTrue(q.put("apple"))
        self.assertEqual(q.get(), "apple")
        q.close()

    def test_queue_size_and_empty_state(self):
        """Test qsize and empty methods during operations."""
        q = UniqueQueue()
        self.assertTrue(q.empty())
        self.assertEqual(q.qsize(), 0)
        
        q.put("a")
        q.put("b")
        self.assertEqual(q.qsize(), 2)
        
        self.assertEqual(q.get(), "a")
        self.assertEqual(q.qsize(), 1)
        
        self.assertEqual(q.get(), "b")
        self.assertTrue(q.empty())
        self.assertEqual(q.qsize(), 0)
        q.close()

class TestThumbnailHelpers(unittest.TestCase):
    
    def test_is_jpeg(self):
        """Test that is_jpeg correctly identifies jpg/JPEG and rejects other formats."""
        self.assertTrue(is_jpeg("image.jpg"))
        self.assertTrue(is_jpeg("IMAGE.JPEG"))
        self.assertTrue(is_jpeg(pathlib.Path("photo.jpeg")))
        
        self.assertFalse(is_jpeg("image.png"))
        self.assertFalse(is_jpeg("document.pdf"))
        self.assertFalse(is_jpeg("no_extension"))

    def test_thumb_name(self):
        """Test that thumb_name correctly inserts '_thumb' before the extension."""
        self.assertEqual(thumb_name("image.jpg"), "image_thumb.jpg")
        self.assertEqual(thumb_name("path/to/photo.png"), "path/to/photo_thumb.png")
        self.assertEqual(thumb_name("my.file.name.JPG"), "my.file.name_thumb.JPG")

    def test_get_filename_from_thumb(self):
        """Test that get_filename_from_thumb strips '_thumb' to get the original filename."""
        self.assertEqual(get_filename_from_thumb("image_thumb.jpg"), "image.jpg")
        self.assertEqual(get_filename_from_thumb("path/to/photo_thumb.png"), "path/to/photo.png")
        
        # Test edge case where '_thumb' isn't present
        self.assertEqual(get_filename_from_thumb("image.jpg"), "image.jpg")

class TestGetFilesToThumb(unittest.TestCase):

    def test_get_files_to_thumb(self):
        """Test that get_files_to_thumb returns only JPEGs that lack a corresponding thumbnail."""
        with tempfile.TemporaryDirectory() as tmp_img_dir, tempfile.TemporaryDirectory() as tmp_thumb_dir:
            # 1. Create test files in the image directory
            img_needs_thumb = "photo1.jpg"
            img_has_thumb = "photo2.JPEG"
            not_an_image = "document.txt"
            not_jpeg = "image.png"
            
            for filename in [img_needs_thumb, img_has_thumb, not_an_image, not_jpeg]:
                pathlib.Path(os.path.join(tmp_img_dir, filename)).touch()
                
            # 2. Create a thumbnail ONLY for photo2.JPEG in the thumbnail directory
            thumb_name_for_photo2 = thumb_name(img_has_thumb)  # "photo2_thumb.JPEG"
            pathlib.Path(os.path.join(tmp_thumb_dir, thumb_name_for_photo2)).touch()
            
            # 3. Run the function
            result = get_files_to_thumb(tmp_img_dir, tmp_thumb_dir)
            
            # 4. Assert expectations:
            # - "photo1.jpg" should be included (is JPEG, no thumbnail exists)
            # - "photo2.JPEG" should be excluded (already has a thumbnail)
            # - "document.txt" and "image.png" should be excluded (not JPEGs)
            self.assertEqual(result, ["photo1.jpg"])

if __name__ == "__main__":
    unittest.main()