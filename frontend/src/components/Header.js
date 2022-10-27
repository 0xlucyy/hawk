import React, { useState } from 'react';
import { Menu } from 'semantic-ui-react'
import { Link } from "react-router-dom";

const Header = () => {

  const [activeItem, setActiveItem] = useState('home');

  const handleItemClick = (name) => setActiveItem(name)

  return (
    <Menu secondary pointing>
        <Menu.Item
          as={Link} to="/"
          name='home'
          active={activeItem === 'home'}
          onClick={() => handleItemClick('home')}
        />
        <Menu.Item
          as={Link} to="/table"
          name='table'
          active={activeItem === 'table'}
          onClick={() => handleItemClick('table')} 
        />
      </Menu>

  );
};

export default Header;