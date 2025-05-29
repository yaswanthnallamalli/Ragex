import React from 'react';
import { FaSun, FaMoon } from 'react-icons/fa';

const Navbar = ({ isDarkMode, toggleTheme }) => {
  return (
    <nav className="bg-[#000033] p-3 flex justify-between items-center w-full fixed top-0 left-0 z-50">
      <div className="text-white text-xl font-bold">
        <img style={{ height: '50px', width: '120px', paddingLeft: '10px' }} src="https://www.ragex.co.za/wp-content/uploads/2022/10/rAgeX-Logo-Master-SMALLER-2.png" alt="" />
      </div>
      <ul className="flex space-x-2 md:space-x-4 ml-auto">
        <li><a href="#home" className="text-white hover:text-gray-400">Home</a></li>
        <li><a href="#about" className="text-white hover:text-gray-400">About</a></li>
        <li><a href="#services" className="text-white hover:text-gray-400">Products</a></li>
        <li><a href="#contact" className="text-white hover:text-gray-400">Contact</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;