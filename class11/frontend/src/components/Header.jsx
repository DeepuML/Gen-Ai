import React from 'react';

function Header() {
  return (
    <header className="bg-gray-900 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center">
          <img src="/favicon.svg" alt="Logo" className="h-8 w-8 mr-2" />
          <span className="text-xl font-bold">roadmap.sh</span>
        </div>
        <nav className="hidden md:flex space-x-4">
          <a href="#" className="hover:text-blue-400">Start Here</a>
          <a href="#" className="hover:text-blue-400">Roadmaps</a>
          <a href="#" className="hover:text-blue-400">AI Tutor</a>
          <a href="#" className="hover:text-blue-400">Teams</a>
        </nav>
        <div className="space-x-4">
          <button className="px-4 py-2 rounded-md border border-white hover:bg-white hover:text-gray-900 transition-colors">Login</button>
          <button className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 transition-colors">Sign Up</button>
        </div>
      </div>
    </header>
  );
}

export default Header;