import React from 'react';
import Navbar from './components/Navbar';
import HomePage from './components/Homepage'; // Ensure the correct import path and casing
import Service3 from './components/Eda'; // Ensure the correct import path and casing
import './index.css'; // Ensure to import the index.css for Tailwind CSS
import { Routes, Route } from 'react-router-dom';
import { Helmet } from "react-helmet";

const App = () => {
  window.embeddedChatbotConfig = {
    chatbotId: "i_tqSm2CJv8nkbDJizp-g",
    domain: "www.chatbase.co"
  };
  
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/Homepage/eda" element={<Service3 />} /> {/* Add the new route */}
      </Routes>
      <Helmet>
        <script
          src="https://www.chatbase.co/embed.min.js"
          chatbotId="i_tqSm2CJv8nkbDJizp-g"
          domain="www.chatbase.co"
          defer>
        </script>
      </Helmet>
    </div>
  );
};

export default App;