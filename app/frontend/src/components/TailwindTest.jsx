import React from 'react';

const TailwindTest = () => {
  return (
    <div className="p-6 max-w-md mx-auto bg-blue-500 rounded-xl shadow-md flex items-center space-x-4 my-4">
      <div>
        <div className="text-xl font-medium text-white">Tailwind Test Component</div>
        <p className="text-blue-200">This should be styled by Tailwind CSS</p>
      </div>
    </div>
  );
};

export default TailwindTest; 