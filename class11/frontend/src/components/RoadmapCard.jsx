import React from 'react';

function RoadmapCard({ title, isNew = false }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg flex items-center justify-between">
      <h3 className="text-xl font-semibold text-white">{title}</h3>
      {isNew && (
        <span className="ml-2 px-2 py-1 bg-purple-600 text-white text-xs font-bold rounded-full">New</span>
      )}
      <span className="text-gray-400">&#9633;</span> {/* Placeholder for icon */}
    </div>
  );
}

export default RoadmapCard;