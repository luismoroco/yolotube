import React from 'react';
import { FaBars } from 'react-icons/fa';
import Search from "./Search";

interface HeaderProps {
  onSidebarToggle: () => void;
  onSearch: (query: string) => void;
}

const Header: React.FC<HeaderProps> = ({onSearch, onSidebarToggle}) => {

  const handleReturnHome = () => {
    window.location.href = '/';
  };

  const handleSearch = (query: string) => {
    onSearch(query);
  };

  return (
    <div className="header">
      <div className="header__menu">
        <button onClick={onSidebarToggle}>
          <FaBars />
        </button>
      </div>

      <div className="header__logo" onClick={handleReturnHome}>
          <img src="src/assets/yolotube.png" alt="YouTube Logo" />
          <span className="header__text">YoloTube</span>
      </div>

      <Search onSearch={handleSearch}  />
    </div>
  );
}

export default Header;
