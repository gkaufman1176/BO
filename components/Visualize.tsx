import React, { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  ScatterChart, Scatter,
  BarChart, Bar,
  CartesianGrid, XAxis, YAxis,
  Tooltip, Legend,
} from 'recharts';
import { extractionApi, assayApi, functionalTestApi } from '../services/apiService';
import { Extraction, Assay, FunctionalTest } from '../types';

export const Visualize: React.FC = () => {
  const [extractions, setExtractions] = useState<Extraction[]>([]);
  const [assays, setAssays] = useState<Assay[]>([]);
  const [functionalTests, setFunctionalTests] = useState<FunctionalTest[]>([]);
  const [mergedAssayExtractionData, setMergedAssayExtractionData] = useState<any[]>([]);
  const [functionalAverages, setFunctionalAverages] = useState<any[]>([]);

  // Load all datasets
  useEffect(() => {
    const fetchData = async () => {
      try {
        const ext = await extractionApi.getAll!();
        const asy = await assayApi.getAll();
        const ft = await functionalTestApi.getAll();

        setExtractions(ext);
        setAssays(asy);
        setFunctionalTests(ft);

        // --- Join assay + extraction data (for PSI correlation)
        const merged = asy
          .filter(a => a.assay_type === 'Solubility')
          .map(a => {
            const extractionRecord = ext.find(e => e.id === a.extraction_id);
            if (extractionRecord && a.value !== null && extractionRecord.yield_pct !== null) {
              return {
                yield_pct: extractionRecord.yield_pct,
                psi: a.value,
                extraction_id: extractionRecord.id,
              };
            }
            return null;
          })
          .filter((x): x is { yield_pct: number; psi: number; extraction_id: string } => !!x);
        setMergedAssayExtractionData(merged);

        // --- Compute average functional test performance
        const grouped: Record<string, number[]> = {};
        ft.forEach(f => {
          const numeric = parseFloat(f.score_or_value);
          if (!isNaN(numeric)) {
            if (!grouped[f.application_type]) grouped[f.application_type] = [];
            grouped[f.application_type].push(numeric);
          }
        });
        const avg = Object.keys(grouped).map(k => ({
          application_type: k,
          avg_value:
            grouped[k].reduce((a, b) => a + b, 0) / grouped[k].length,
        }));
        setFunctionalAverages(avg);

      } catch (err) {
        console.error('Failed to load visualization data:', err);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-6">Visualize</h1>

      {/* 1️⃣ Yield % vs pH */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
        <h2 className="text-xl font-bold text-white mb-4">Yield % vs pH</h2>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
            <XAxis type="number" dataKey="ph" name="pH" stroke="#a0aec0" />
            <YAxis type="number" dataKey="yield_pct" name="Yield (%)" stroke="#a0aec0" />
            <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{ backgroundColor: '#2d3748', border: 'none', color: '#e2e8f0' }}
            />
            <Legend />
            <Scatter name="Extraction" data={extractions} fill="#3b82f6" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* 2️⃣ Yield % vs Salt Conc. (%) */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
        <h2 className="text-xl font-bold text-white mb-4">Yield % vs Salt Conc. (%)</h2>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
            <XAxis type="number" dataKey="salt_conc" name="Salt Conc. (%)" stroke="#a0aec0" />
            <YAxis type="number" dataKey="yield_pct" name="Yield (%)" stroke="#a0aec0" />
            <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{ backgroundColor: '#2d3748', border: 'none', color: '#e2e8f0' }}
            />
            <Legend />
            <Scatter name="Salt Trials" data={extractions} fill="#82ca9d" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* 3️⃣ PSI vs Yield % */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
        <h2 className="text-xl font-bold text-white mb-4">PSI vs Yield %</h2>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
            <XAxis type="number" dataKey="yield_pct" name="Yield (%)" stroke="#a0aec0" />
            <YAxis type="number" dataKey="psi" name="PSI (%)" stroke="#a0aec0" />
            <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{ backgroundColor: '#2d3748', border: 'none', color: '#e2e8f0' }}
            />
            <Legend />
            <Scatter
              name="Solubility Correlation"
              data={mergedAssayExtractionData}
              fill="#8884d8"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* 4️⃣ Application Type vs Avg Functional Value */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-bold text-white mb-4">
          Application Type vs Avg Functional Value
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={functionalAverages}>
            <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
            <XAxis dataKey="application_type" stroke="#a0aec0" />
            <YAxis stroke="#a0aec0" />
            <Tooltip
                contentStyle={{ backgroundColor: '#2d3748', border: 'none', color: '#e2e8f0' }}
                cursor={{ fill: 'rgba(99, 179, 237, 0.1)' }}
            />
            <Legend />
            <Bar dataKey="avg_value" name="Avg. Value (Numeric)" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
