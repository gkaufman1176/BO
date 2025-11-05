import React, { useState } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { Sidebar } from './common/Sidebar';
import { Dashboard } from './Dashboard';
import { WorksheetPage } from './WorksheetPage';
import { Visualize } from './Visualize';
import { NotesAndFiles } from './NotesAndFiles';
import { Chat } from './Chat';
import { worksheetConfigs } from '../worksheetConfig';
import { Ingredient, Extraction, Assay, FunctionalTest } from '../types';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleToggleChat = () => {
    setIsChatOpen(prev => !prev);
  };

  return (
    <HashRouter>
      <div className="flex h-screen bg-gray-900 text-gray-200">
        <Sidebar onToggleChat={handleToggleChat} />
        <main className="flex-grow ml-64 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/ingredients" element={<WorksheetPage<Ingredient> {...worksheetConfigs.ingredients} />} />
            <Route path="/extractions" element={<WorksheetPage<Extraction> {...worksheetConfigs.extractions} />} />
            <Route path="/assays" element={<WorksheetPage<Assay> {...worksheetConfigs.assays} />} />
            <Route path="/functional-tests" element={<WorksheetPage<FunctionalTest> {...worksheetConfigs.functionalTests} />} />
            <Route path="/visualize" element={<Visualize />} />
            <Route path="/notes" element={<NotesAndFiles />} />
          </Routes>
        </main>
        {isChatOpen && <Chat onClose={handleToggleChat} />}
      </div>
    </HashRouter>
  );
}

export default App;
