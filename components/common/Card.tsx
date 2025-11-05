import React from 'react';

interface CardProps {
  title: string;
  value: string | number;
  children?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, value, children }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h3 className="text-sm font-medium text-gray-400">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-3xl font-semibold text-white">{value}</p>
        {children}
      </div>
    </div>
  );
};
