import { useState, useEffect } from 'react';
import './ImageGallery.css'; // optional - see styles below

function ImageGallery() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('/images', {
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

        setImages(data.images);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load images');
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
      {images.map((filename, index) => (
        <div key={filename} className="gallery-item">
          <img
            src={`/images/${filename}`}
            alt={`Image ${index + 1}`}
            loading="lazy"
            onError={(e) => {
              // Optional: show fallback / broken image style
              (e.target).style.opacity = '0.5';
              (e.target).title = 'Image failed to load';
            }}
          />
          {/* Optional caption */}
          {/* <p className="image-filename">{filename}</p> */}
        </div>
      ))}
    </div>
  );
}

export default ImageGallery;
