import React, { useState } from 'react';
import { CloseIcon } from './common/Icons';

interface ChatProps {
    onClose: () => void;
}

export const Chat: React.FC<ChatProps> = ({ onClose }) => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setResponse('');
        // Mock AI response
        setTimeout(() => {
            if (prompt.toLowerCase().includes('yield > 70')) {
                setResponse("Found 2 extractions with yield > 70%:\n- Extraction #ext_1 (78.5%)\n- Extraction #ext_2 (82.1%)");
            } else if (prompt.toLowerCase().includes('assays for extraction')) {
                 setResponse("Found 1 assay for Extraction #ext_1:\n- Solubility (PSI): 92%");
            } else {
                setResponse("I can help with queries like 'show me extractions with yield > 70%' or 'list assays for Extraction #ext_1'.");
            }
            setIsLoading(false);
        }, 1500);
    };

    return (
        <div className="w-80 bg-gray-800 p-4 flex flex-col h-screen fixed right-0 top-0 border-l border-gray-700 shadow-2xl z-10 transform transition-transform duration-300 ease-in-out">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-white">AI Copilot</h2>
                <button onClick={onClose} className="p-1 rounded-full hover:bg-gray-700 transition-colors">
                    <CloseIcon />
                </button>
            </div>

            <div className="flex-grow bg-gray-900 rounded-lg p-3 overflow-y-auto mb-4">
                {response ? (
                    <pre className="text-sm text-gray-300 whitespace-pre-wrap font-sans">{response}</pre>
                ) : (
                    <p className="text-gray-500 text-sm">Ask a question about your data...</p>
                )}
                {isLoading && <p className="text-blue-400 text-sm">Thinking...</p>}
            </div>

            <form onSubmit={handleSubmit}>
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="e.g., show extractions with yield > 70%"
                    className="w-full h-24 p-2 bg-gray-700 text-gray-200 border border-gray-600 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button type="submit" className="w-full mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200" disabled={isLoading}>
                    {isLoading ? 'Processing...' : 'Ask'}
                </button>
            </form>
        </div>
    );
};
