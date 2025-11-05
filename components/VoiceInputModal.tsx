import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Modal } from './common/Modal';
import { MicrophoneIcon, LoadingSpinnerIcon } from './common/Icons';
import { aiService } from '../services/aiService';
import { apiService } from '../services/apiService';
import { worksheetConfigs } from '../worksheetConfig';

type Status = 'idle' | 'requesting_permission' | 'permission_denied' | 'recording' | 'processing' | 'verifying' | 'saving' | 'error' | 'success';

interface VoiceInputModalProps {
    isOpen: boolean;
    onClose: () => void;
    onDataAdded: (dataType: string) => void;
}

// FIX: Cast window to `any` to access non-standard SpeechRecognition APIs
// without causing TypeScript errors.
const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

export const VoiceInputModal: React.FC<VoiceInputModalProps> = ({ isOpen, onClose, onDataAdded }) => {
    const [status, setStatus] = useState<Status>('idle');
    const [transcript, setTranscript] = useState('');
    const [parsedData, setParsedData] = useState<{ dataType: string; data: any } | null>(null);
    const [error, setError] = useState<string | null>(null);
    const recognitionRef = useRef<any>(null);

    const resetState = useCallback(() => {
        setStatus('idle');
        setTranscript('');
        setParsedData(null);
        setError(null);
        if (recognitionRef.current) {
            recognitionRef.current.stop();
            recognitionRef.current = null;
        }
    }, []);

    // Reset when modal is closed
    useEffect(() => {
        if (!isOpen) {
            // Use a timeout to allow the closing animation to finish
            setTimeout(resetState, 300);
        }
    }, [isOpen, resetState]);

    const handleStartRecording = async () => {
        if (!SpeechRecognition) {
            setError("Speech recognition is not supported in your browser.");
            setStatus('error');
            return;
        }

        try {
            // Check for permission, this will prompt the user if not granted
            await navigator.mediaDevices.getUserMedia({ audio: true });

            setStatus('recording');
            setTranscript('');
            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;

            let finalTranscriptHolder = '';
            recognition.onresult = (event) => {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscriptHolder += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                setTranscript(finalTranscriptHolder + interimTranscript);
            };

            recognition.onend = () => {
                // Check status to ensure we are in a state where we should process.
                // Prevents processing on an explicit cancel or error.
                setStatus(currentStatus => {
                    if (currentStatus === 'recording') {
                        handleProcessTranscript(finalTranscriptHolder);
                        return 'processing';
                    }
                    return currentStatus;
                });
            };

            recognition.onerror = (event) => {
                setError(`Speech recognition error: ${event.error}`);
                setStatus('error');
            };

            recognition.start();
            recognitionRef.current = recognition;

        } catch (err) {
            console.error('Microphone access denied:', err);
            setStatus('permission_denied');
        }
    };

    const handleStopRecording = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    };

    const handleProcessTranscript = async (finalTranscript: string) => {
        if (!finalTranscript.trim()) {
            setStatus('idle');
            return;
        }
        setError(null);
        try {
            const result = await aiService.parseTextToData(finalTranscript);
            setParsedData(result);
            setStatus('verifying');
        } catch (e) {
            setError(e instanceof Error ? e.message : "An unknown error occurred during parsing.");
            setStatus('error');
        }
    };

    const handleConfirmAndSave = async () => {
        if (!parsedData) return;
        setStatus('saving');
        setError(null);
        try {
            await apiService.createRecord(parsedData.dataType, parsedData.data);
            setStatus('success');
            onDataAdded(parsedData.dataType);
            setTimeout(() => {
                onClose();
            }, 1500); // Close after showing success message
        } catch (e) {
            setError(e instanceof Error ? e.message : "Failed to save the record.");
            setStatus('error');
        }
    };

    const renderContent = () => {
        switch (status) {
            case 'idle':
            case 'requesting_permission':
                return (
                    <div className="text-center">
                        <p className="mb-6 text-gray-400">Press the button and speak naturally to add a new data entry. For example: "Log a new extraction for batch HPI-2024-01 with a pH of 6.8 and a yield of 82 percent."</p>
                        <button onClick={handleStartRecording} className="inline-flex items-center gap-3 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full transition-colors duration-200 text-lg">
                            <MicrophoneIcon />
                            Start Recording
                        </button>
                    </div>
                );
            case 'permission_denied':
                return (
                    <div className="text-center text-red-400">
                        <p className="font-bold">Microphone Access Denied</p>
                        <p>Please enable microphone permissions for this site in your browser settings to use this feature.</p>
                    </div>
                );
            case 'recording':
                return (
                    <div className="text-center">
                        <div className="mb-4">
                            <div className="animate-pulse text-red-500 font-bold">RECORDING</div>
                            <div className="w-16 h-16 mx-auto bg-red-500 rounded-full flex items-center justify-center text-white">
                                <MicrophoneIcon />
                            </div>
                        </div>
                        <p className="min-h-[72px] bg-gray-900 p-3 rounded-md text-left text-gray-300">{transcript || 'Listening...'}</p>
                        <button onClick={handleStopRecording} className="mt-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                            Stop & Process
                        </button>
                    </div>
                );
            case 'processing':
            case 'saving':
                return (
                    <div className="flex flex-col items-center justify-center gap-4 p-8">
                        <LoadingSpinnerIcon className="w-12 h-12 text-blue-500" />
                        <p className="text-lg text-gray-300">{status === 'processing' ? 'Analyzing your speech...' : 'Saving record...'}</p>
                    </div>
                );
            case 'verifying':
                if (!parsedData) return null;
                const config = worksheetConfigs[parsedData.dataType as keyof typeof worksheetConfigs];
                return (
                    <div>
                        <h3 className="text-lg font-semibold mb-2 text-white">Please verify the extracted data:</h3>
                        <p className="mb-4 text-gray-400">We think you want to add a new <span className="font-bold text-blue-400">{config.title.slice(0,-1)}</span>. Does this look correct?</p>
                        <div className="bg-gray-900 p-4 rounded-lg max-h-60 overflow-y-auto">
                            <dl className="grid grid-cols-2 gap-x-4 gap-y-2">
                            {Object.entries(parsedData.data).map(([key, value]) => {
                                // Find the column definition to get the proper header
                                const column = config.columns.find(c => c.key === key);
                                if (!value && typeof value !== 'number') return null; // Don't show empty fields
                                return (
                                    <React.Fragment key={key}>
                                        <dt className="text-sm font-medium text-gray-400 truncate">{column?.header || key}</dt>
                                        <dd className="text-sm text-gray-200">{String(value)}</dd>
                                    </React.Fragment>
                                );
                            })}
                            </dl>
                        </div>
                        <div className="mt-6 flex justify-end gap-3">
                            <button onClick={resetState} className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Try Again</button>
                            <button onClick={handleConfirmAndSave} className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Confirm & Add</button>
                        </div>
                    </div>
                );
            case 'success':
                 return (
                    <div className="text-center p-8">
                        <div className="w-16 h-16 mx-auto bg-green-500 rounded-full flex items-center justify-center text-white mb-4">
                            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                        </div>
                        <p className="text-xl font-bold text-white">Record Added Successfully!</p>
                    </div>
                );
            case 'error':
                 return (
                    <div className="text-center">
                        <p className="font-bold text-red-400 mb-2">An Error Occurred</p>
                        <p className="bg-red-900/50 p-3 rounded-md text-red-300 mb-4">{error}</p>
                        <button onClick={resetState} className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                            Try Again
                        </button>
                    </div>
                );
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="Add Data by Voice" size="md">
            {renderContent()}
        </Modal>
    );
};
