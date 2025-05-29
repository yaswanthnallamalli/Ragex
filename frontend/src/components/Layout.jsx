import React from 'react';
import Navbar from './Navbar'; // Adjust the path as necessary

const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main>{children}</main>
    </div>
  );
};

export default Layout;