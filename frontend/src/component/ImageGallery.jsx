import { useState, useEffect } from 'react';
import './ImageGallery.css'; // optional - keep your existing styles

function ImageGallery() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('/api/images', {
          headers: {
            'Accept': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();

        if (!data.images || !Array.isArray(data.images)) {
          throw new Error('Invalid response format - "images" array expected');
        }

        // Sort filenames assuming they are unix-timestamp.jpg
        // Newest first (largest timestamp → most recent)
        const sortedFilenames = data.images.sort((a, b) => {
          // Extract the number part before .jpg
          const getTimestamp = (filename) => {
            const match = filename.match(/(\d{10,})/); 
            return match ? Number(match[1]) : 0;
          };

          const tsA = getTimestamp(a);
          const tsB = getTimestamp(b);
          return tsB - tsA; // descending = newest first
          // return tsA - tsB; // uncomment for oldest first
        });

        setImages(sortedFilenames);
      } catch (err) {
        setError(err.message || 'Failed to load images');
        console.error('Image fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, []);

  if (loading) {
    return (
      <div className="gallery-loading">
        Loading images...
      </div>
    );
  }

  if (error) {
    return (
      <div className="gallery-error">
        Error: {error}
      </div>
    );
  }

  if (images.length === 0) {
    return (
      <div className="gallery-empty">
        No images found
      </div>
    );
  }

  return (
    <div className="image-gallery">
      {images.map((filename) => (
        <div key={filename} className="gallery-item">
          <img
            src={`/api/images/${filename}`}
            alt={`Image ${filename}`}
            loading="lazy"
            onError={(e) => {
              e.target.style.opacity = '0.5';
              e.target.title = 'Image failed to load';
            }}
          />
          {/* Optional: show timestamp or filename */}
          {<p className="image-caption">
            {new Date(Number(filename.replace('.jpg', '')) * 1000).toLocaleString()}
          </p>}
        </div>
      ))}
    </div>
  );
}

export default ImageGallery;
