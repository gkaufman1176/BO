import React from 'react';
import { NavLink } from 'react-router-dom';
import { SparklesIcon } from './Icons';

interface NavItem {
  path?: string;
  label: string;
  isHeader?: boolean;
  isAction?: boolean;
  icon?: React.ReactNode;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Dashboard' },
  { isHeader: true, label: 'Data Management' },
  { path: '/ingredients', label: 'Ingredients' },
  { path: '/extractions', label: 'Extraction Trials' },
  { path: '/assays', label: 'Assays' },
  { path: '/functional-tests', label: 'Functional Tests' },
  { isHeader: true, label: 'Analysis' },
  { path: '/visualize', label: 'Visualize' },
  { path: '/notes', label: 'Notes & Files' },
  { isAction: true, label: 'AI Copilot', icon: <SparklesIcon /> },
];

interface SidebarProps {
  onToggleChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onToggleChat }) => {
  const baseLinkClasses = "flex items-center gap-3 w-full text-left px-4 py-2 rounded-md transition-colors duration-200";
  const activeLinkClasses = "bg-blue-600 text-white";
  const inactiveLinkClasses = "text-gray-400 hover:bg-gray-700 hover:text-white";

  const handleItemClick = (item: NavItem) => {
    if (item.isAction && item.label === 'AI Copilot') {
      onToggleChat();
    }
  };

  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col h-screen fixed z-20">
      <div className="text-white text-2xl font-bold mb-8">
        R&D Lab Manager
      </div>
      <nav className="flex-grow">
        <ul>
          {navItems.map((item, index) => (
            <li key={index} className={item.isHeader ? "mt-6 mb-2" : ""}>
              {item.isHeader ? (
                <span className="text-gray-500 text-sm font-bold uppercase px-4">{item.label}</span>
              ) : item.isAction ? (
                <button
                  onClick={() => handleItemClick(item)}
                  className={`${baseLinkClasses} ${inactiveLinkClasses}`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ) : (
                <NavLink
                  to={item.path!}
                  className={({ isActive }) => `${baseLinkClasses} ${isActive ? activeLinkClasses : inactiveLinkClasses}`}
                >
                  {item.label}
                </NavLink>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};
