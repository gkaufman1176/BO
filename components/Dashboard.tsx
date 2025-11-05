import React, { useState, useEffect } from 'react';
import { dashboardApi } from '../services/apiService';
import { Card } from './common/Card';
import { Extraction } from '../types';

interface OverviewStats {
  totalIngredients: number;
  totalExtractions: number;
  avgYield: string;
  recentExtractions: Extraction[];
}

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        setLoading(true);
        const data = await dashboardApi.getOverview();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchOverview();
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-lg">Loading dashboard...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card title="Total Ingredients" value={stats?.totalIngredients ?? 0} />
        <Card title="Total Extractions" value={stats?.totalExtractions ?? 0} />
        <Card title="Average Yield" value={`${stats?.avgYield ?? 0}%`} />
      </div>

      <h2 className="text-2xl font-bold text-white mb-4">Recent Extractions</h2>
      <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-700">
            <thead className="bg-gray-700/50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Method</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Yield %</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Operator</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Stage</th>
              </tr>
            </thead>
            <tbody className="bg-gray-800 divide-y divide-gray-700">
              {stats?.recentExtractions.map((ext) => (
                <tr key={ext.id} className="hover:bg-gray-700/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-200">{new Date(ext.date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-200">{ext.method}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{ext.yield_pct?.toFixed(1) ?? 'N/A'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-200">{ext.operator}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-200">{ext.stage_label}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
