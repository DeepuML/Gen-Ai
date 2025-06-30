import React from 'react';
import RoadmapCard from './RoadmapCard';

function RoadmapSection() {
  const roadmaps = [
    { title: 'Frontend' },
    { title: 'Backend' },
    { title: 'DevOps' },
    { title: 'Full Stack' },
    { title: 'AI Engineer', isNew: true },
    { title: 'Data Analyst' },
    { title: 'AI and Data Scientist' },
    { title: 'Android' },
    { title: 'iOS' },
    { title: 'PostgreSQL' },
    { title: 'Blockchain' },
    { title: 'QA' },
    { title: 'Software Architect' },
    { title: 'Cyber Security' },
    { title: 'UX Design' },
    { title: 'Game Developer' },
    { title: 'Technical Writer' },
    { title: 'MLOps' },
    { title: 'Product Manager' },
    { title: 'Engineering Manager' },
    { title: 'Developer Relations' },
  ];

  return (
    <section className="py-12 bg-gray-900 text-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <span className="inline-block bg-gray-700 text-gray-300 text-sm px-4 py-2 rounded-full mb-8">Role-based Roadmaps</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {roadmaps.map((roadmap, index) => (
            <RoadmapCard key={index} title={roadmap.title} isNew={roadmap.isNew} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default RoadmapSection;