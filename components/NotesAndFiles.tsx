import React from 'react';

export const NotesAndFiles: React.FC = () => {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-6">Notes & Files</h1>
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
        <p className="text-gray-400">This section will allow users to upload files, record audio, and write text notes. They can be filtered by parent (e.g., Ingredient, Extraction).</p>
        <div className="mt-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Upload File
            </button>
        </div>
      </div>
    </div>
  );
};
