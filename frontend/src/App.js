import './App.css';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import VideoPlayer from './component/VideoPlayer';
import TimelapseTrigger from './component/Timelapse.jsx';
import ImageGallery from './component/ImageGallery.jsx';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={
          <div className='container'>
            <VideoPlayer />
            <TimelapseTrigger />
            <NavLink to='/gallery'>Gallery</NavLink>
          </div>
        } />
      <Route path = "/gallery" element={
        <ImageGallery />
        } />
      </Routes>
    </div>
  );
}

export default App;
