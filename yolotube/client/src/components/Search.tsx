import { useEffect, useState } from 'react';
import { FaSearch } from 'react-icons/fa';
import { useLocation, useNavigate } from 'react-router-dom';

interface SearchProps {
  onSearch: (query: string) => void;
}

const Search: React.FC<SearchProps> = ({ onSearch })  => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searched, setSearched] = useState(false);


  const navigate = useNavigate();
  const location = useLocation();

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
    setSearched(false);
  };

  const handleSearch = () => {
    onSearch(searchQuery);
    setSearched(true);
  };

  const handleKeyDown = (e: any) => {
    if (e.code === "Enter") {
      handleSearch();
    }
  };

  useEffect(() => {
    if (searched && location.pathname !== '/') {
      setSearched(false);
      navigate('/');
    }
  }, [location.pathname, navigate, searched, setSearched]);

  return (
    <div className="search">
      <div className="search__box">
        <input 
          type="text"
          placeholder="Buscar..."
          value={searchQuery}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />
        <button>
          <FaSearch />
        </button>
      </div>
    </div>
  );
}

export default Search;