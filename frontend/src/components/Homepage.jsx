import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSun, FaMoon, FaMicrophone, FaMicrophoneSlash } from 'react-icons/fa';
import { Mail, Phone, Github, Linkedin, Twitter } from "lucide-react";

const HomePage = () => {
    const navigate = useNavigate();
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef(new Audio('/images/introduction.mp3'));

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode);
    };

    const toggleAudio = () => {
        const audio = audioRef.current;
        audio.loop = false;

        if (isPlaying) {
            audio.pause();
        } else {
            audio.play();
        }

        setIsPlaying(!isPlaying);
    };

    const handleRedirect = (path, isExternal = false) => {
        if (isExternal) {
            window.location.href = 'http://localhost:8000';
        } else {
            navigate(path);
        }
    };

    return (
        <div className={`flex flex-col min-h-screen ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-white text-black'}`}>
            <style>
                {`
                @keyframes fadeInScale {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }

                .fade-in-scale {
                    animation: fadeInScale 2s ease-in-out;
                }

                .bg-animation {
                    background: linear-gradient(135deg, #000038 25%, #000050 75%);
                    background-size: 400% 400%;
                    animation: gradientAnimation 15s ease infinite;
                }

                @keyframes gradientAnimation {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                .hover-effect:hover {
                    transform: scale(1.05) rotate(1deg);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                }
                `}
            </style>

            <header className="relative h-screen flex flex-col justify-center items-center text-white w-full" id="home">
                <button
                    onClick={toggleTheme}
                    className="absolute top-13 right-4 bg-teal-500 text-white p-3 rounded-full z-50"
                >
                    {isDarkMode ? <FaSun /> : <FaMoon />}
                </button>

                <video
                    className="absolute w-full h-full object-cover"
                    src="/images/intro.mp4"
                    autoPlay
                    loop
                    muted
                    playsInline
                >
                    Your browser does not support the video tag.
                </video>

                <button
                    onClick={toggleAudio}
                    className="absolute bottom-10 left-1/2 transform -translate-x-1/2 bg-teal-500 text-white p-3 rounded-full z-50 text-xl shadow-md"
                    title="click to start/pause Audio"
                >
                    {isPlaying ? <FaMicrophone /> : <FaMicrophoneSlash />}
                </button>

                <div className="bg-black bg-opacity-50 p-6 md:p-10 lg:p-14 xl:p-20 rounded max-w-4xl mx-auto w-full text-center relative z-10">
                    <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
                        <img
                            style={{ height: '60px', width: '120px', margin: 'auto' }}
                            src="https://www.ragex.co.za/wp-content/uploads/2022/10/rAgeX-Logo-Master-SMALLER-2.png"
                            alt="RAGEX Logo"
                        />
                    </h1>
                    <h1 className="text-2xl md:text-3xl lg:text-4xl mb-2">Unlocking meaningful insights from the data</h1>
                    <h1 className="text-2xl md:text-3xl lg:text-4xl text-[#9eeb47]">Bringing Excel and AI into seamless harmony</h1>
                </div>
            </header>

            <main className="flex-grow">
 <section
  className={`py-12 md:py-16 lg:py-20 ${isDarkMode ? 'bg-gray-800' : 'bg-gradient-to-r from-[#000038] to-[#000050]'} w-full`}
  id="about"
>
  <div className="max-w-5xl mx-auto px-6 text-center">
    <h2 className="text-3xl md:text-4xl font-extrabold text-teal-400 tracking-wide fade-in-scale mb-4">
      Meet RAGEX
    </h2>
    <p className={`text-lg md:text-xl leading-relaxed fade-in-scale ${isDarkMode ? 'text-gray-100' : 'text-white'}`}>
      <strong>RAGEX</strong> isn’t just another chatbot it’s your personal data analyst.   
      Combining the power of local LLMs  Mistral, intelligent vector search, and dynamic SQL generation, 
      RAGEX empowers you to explore Excel data through natural conversation.
    </p>
    <p className={`text-md md:text-lg mt-4 text-gray-300 fade-in-scale`}>
      Designed for speed, privacy, and real-time insights, RAGEX runs entirely offline,
      ensuring your data stays secure while delivering answers in seconds  
    </p>
    <div className="mt-8">
      <span className="inline-block text-sm uppercase tracking-wider text-teal-300 bg-white bg-opacity-10 px-4 py-2 rounded-full">
        Transforming Excel Into AI-Powered Insights — Secure, Swift, and Seamless
      </span>
    </div>
  </div>
</section>

                <section className={`py-12 md:py-16 lg:py-20 ${isDarkMode ? 'bg-gray-800' : 'bg-white'} w-full`}>
                    <div className="max-w-4xl mx-auto px-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {[
                                {
                                    title: 'Data at Rest',
                                    desc: 'Ragex securely handles your Excel data by processing it locally during each session. No data is stored permanently or transmitted to external servers, ensuring complete privacy and control. Your dataset remains fully accessible for querying and analysis, offering a secure and seamless experience without any risk of data breach.'
                                },
                                {
                                    title: 'Data in Motion',
                                    desc: 'Interact naturally with your uploaded data through Ragex AI-powered conversational interface. Using a hybrid method that blends RAG and SQL, Ragex converts your questions into accurate queries. This real-time process delivers relevant, context-aware answers from your dataset, enabling intelligent and efficient data exploration.'
                                },
                                {
                                    title: 'Data in Action',
                                    desc: 'Discover insights with Ragex powerful visualization tools that turn your data into interactive graphs. From bar charts to heatmaps, you can explore trends, distributions, and patterns visually. The customizable and intuitive interface makes complex analysis simple, helps to unlock the full value of the data.'
                                }
                            ].map((item, i) => (
                                <div key={i} className="bg-white p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105 hover:shadow-2xl hover:-translate-y-2">
                                    <h3 className="text-xl font-bold mb-4 text-green-600">{item.title}</h3>
                                    <p className="text-gray-800">{item.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                <section className={`py-12 md:py-16 lg:py-20 ${isDarkMode ? 'bg-gray-700' : 'bg-teal-50'} w-full`} id="services">
                    <div className="max-w-4xl mx-auto px-4">
                        <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold mb-6 text-teal-500 text-center">RAGEX Hub</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div
                                className="bg-white p-6 rounded-lg shadow-md cursor-pointer hover:bg-gray-100 transition duration-300 transform hover:scale-105 hover:shadow-xl"
                                onClick={() => handleRedirect('/Homepage/EIM_Assistant', true)}
                            >
                                <h3 className="text-xl font-semibold mb-4 text-teal-500">RAGEX Bot</h3>
                                <p className="text-base text-gray-800">
                                    RAGEX is an AI chatbot that lets you interact naturally with Excel or CSV data. Using a hybrid of RAG and SQL, it provides accurate, intelligent answers powered by the locally hosted Mistral-7B model offering fast, reliable, and secure insights without external servers
                                </p>
                            </div>
                            <div
                                className="bg-white p-6 rounded-lg shadow-md cursor-pointer hover:bg-gray-100 transition duration-300 transform hover:scale-105 hover:shadow-xl"
                                onClick={() => handleRedirect('/Homepage/eda')}
                            >
                                <h3 className="text-xl font-semibold mb-4 text-teal-500">Data Visualizer</h3>
                                <p className="text-base text-gray-800">
                                    The Data Visualizer offers an interactive way to explore Excel. Preview your dataset, select columns, and create customizable charts with color options. It handles data types automatically for smooth visual analysis
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

<footer className="bg-gray-900 text-white py-10" id="contact">
  <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center md:items-start gap-10">
    {/* Contact Info */}
    <div className="text-center md:text-left">
      <h2 className="text-xl font-semibold mb-3">Contact Us</h2>
      <p className="flex items-center justify-center md:justify-start gap-2 mb-1">
        <Mail size={18} /> support@ragex.ai
      </p>
      <p className="flex items-center justify-center md:justify-start gap-2">
        <Phone size={18} /> +91 7075590398
      </p>
    </div>

    {/* Social Media */}
    <div className="text-center md:text-left">
      <h2 className="text-xl font-semibold mb-3">Follow Us</h2>
      <div className="flex justify-center md:justify-start gap-6">
        <a href="https://github.com/yaswanthnallamalli/Ragex" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">
          <Github size={22} />
        </a>
        <a href="https://www.linkedin.com/company/ragex-ai" target="_blank" rel="noopener noreferrer" className="hover:text-blue-400">
          <Linkedin size={22} />
        </a>
        <a href="https://twitter.com/ragex_ai" target="_blank" rel="noopener noreferrer" className="hover:text-blue-300">
          <Twitter size={22} />
        </a>
      </div>
    </div>
  </div>

  {/* Divider and Footer Bottom */}
  <div className="border-t border-gray-700 mt-8 pt-4 text-center text-sm text-gray-400">
    &copy; 2025 RAGEX · All rights reserved.
  </div>
</footer>
        </div>
    );
};

export default HomePage;
