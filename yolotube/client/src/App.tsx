import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import VideoList from './components/VideoList';
import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import VideoPlayer from './components/VideoPlayer';


function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <BrowserRouter>
      <div className="app">
        <Header onSidebarToggle={handleSidebarToggle} onSearch={handleSearch} />
        <div className="app__body">
          <Sidebar isOpen={sidebarOpen} />
          <Routes>
            <Route path="/">
              <Route index element={<VideoList searchQuery={searchQuery} />} />
              <Route path="media/:title/:url/:description" element={<VideoPlayer/>} />
            </Route>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;