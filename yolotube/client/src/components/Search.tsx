import { useState } from 'react';
import { FaSearch } from 'react-icons/fa';

interface SearchProps {
  onSearch: (query: string) => void;
}

const Search: React.FC<SearchProps> = ({ onSearch })  => {
  const [searchQuery, setSearchQuery] = useState('');
  
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  };

  const handleSearch = () => {
    // window.location.href = `/data?query=${encodeURIComponent(searchQuery)}`;
    onSearch(searchQuery);
  };

  const handleKeyDown = (e: any) => {
    if (e.code === "Enter") {
      handleSearch();
    }
  };

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