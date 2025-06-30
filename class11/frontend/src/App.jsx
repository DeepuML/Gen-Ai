import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Hero from './components/Hero';
import RoadmapSection from './components/RoadmapSection';

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      <Hero />
      <RoadmapSection />
      <footer className="mt-12 text-center text-gray-500 text-sm py-4">
        Made with ❤️ by AI Enthusiasts | roadmap.sh clone
      </footer>
    </div>
  );
}

export default App;