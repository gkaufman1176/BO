import React, { useState, useEffect, useCallback, ChangeEvent, useRef } from 'react';
import { PlusIcon, TrashIcon, DuplicateIcon, ExportIcon, AttachmentIcon, UploadIcon, MicrophoneIcon } from './common/Icons';
import { ExtractionStage, Ingredient } from '../types';
import { ingredientApi } from '../services/apiService';
import { VoiceInputModal } from './VoiceInputModal';

// FIX: Export the Column interface
export interface Column<T> {
  key: keyof T;
  header: string;
  type?: 'text' | 'number' | 'date' | 'select' | 'attachments' | 'link';
  options?: string[];
  linkSource?: 'ingredients';
  readOnly?: boolean;
}

interface Api<T> {
  getAll?: () => Promise<T[]>;
  getByStage?: (stage: ExtractionStage) => Promise<T[]>;
  create: (item: Omit<T, 'id'>) => Promise<T>;
  update: (id: string, updates: Partial<T>) => Promise<T>;
  delete: (id: string) => Promise<void>;
}

interface WorksheetPageProps<T> {
  title: string;
  dataType: string;
  columns: Column<T>[];
  api: Api<T>;
  defaultNewRow: Omit<T, 'id'>;
}

interface Stage {
  key: ExtractionStage;
  label: string;
}

const stages: Stage[] = [
  { key: ExtractionStage.STAGE1, label: 'Stage 1 - Raw Material' },
  { key: ExtractionStage.STAGE2, label: 'Stage 2 - Cold Salt Extract' },
  { key: ExtractionStage.STAGE3, label: 'Stage 3 - Separation' },
  { key: ExtractionStage.STAGE4, label: 'Stage 4 - Micelle Collection' },
];

export const WorksheetPage = <T extends { id: string; attachments?: any[] }>({ title, dataType, columns, api, defaultNewRow }: WorksheetPageProps<T>) => {
  const [rows, setRows] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());
  const [editingCell, setEditingCell] = useState<{ rowId: string; key: keyof T } | null>(null);
  const [linkedData, setLinkedData] = useState<{ ingredients: Ingredient[] }>({ ingredients: [] });
  const [activeStage, setActiveStage] = useState<Stage>(stages[1]); // Default to Stage 2 for extractions
  const [isUploading, setIsUploading] = useState(false);
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const importCsvInputRef = useRef<HTMLInputElement>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      let data;
      if (dataType === 'extractions' && api.getByStage) {
        data = await api.getByStage(activeStage.key);
      } else if (api.getAll) {
        data = await api.getAll();
      }
      setRows(data || []);

      if (columns.some(c => c.type === 'link')) {
        const ingredients = await ingredientApi.getAll();
        setLinkedData(prev => ({ ...prev, ingredients }));
      }
    } catch (error) {
      console.error(`Failed to fetch ${dataType}:`, error);
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [api, dataType, activeStage.key]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSelectionChange = (id: string) => {
    setSelectedRows(prev => {
      const newSelection = new Set(prev);
      if (newSelection.has(id)) {
        newSelection.delete(id);
      } else {
        newSelection.add(id);
      }
      return newSelection;
    });
  };

  const handleSelectAll = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedRows(new Set(rows.map(r => r.id)));
    } else {
      setSelectedRows(new Set());
    }
  };

  const handleAddRow = async () => {
    try {
      let newRowData = defaultNewRow;
      if (dataType === 'extractions') {
          newRowData = {...defaultNewRow, stage: activeStage.key, stage_label: activeStage.label};
      }
      const newRow = await api.create(newRowData);
      setRows(prev => [...prev, newRow]);
    } catch (error) {
      console.error('Failed to add row:', error);
    }
  };

  const handleDeleteSelected = async () => {
    // FIX: The provided error 'Argument of type 'unknown' is not assignable to parameter of type 'string'' at line 116 points here.
    // While the types seem correct (`selectedRows` is `Set<string>`), this could be a subtle issue with TypeScript's type inference.
    // Explicitly casting the id to a string ensures the `api.delete` contract is met, resolving the reported error.
    const promises = Array.from(selectedRows).map(id => api.delete(id as string));
    await Promise.all(promises);
    setRows(prev => prev.filter(r => !selectedRows.has(r.id)));
    setSelectedRows(new Set());
  };

  const handleUpdateCell = async (rowId: string, key: keyof T, value: any) => {
    const originalRows = [...rows];
    const updatedRows = rows.map(r => r.id === rowId ? {...r, [key]: value} : r);
    setRows(updatedRows);

    try {
        await api.update(rowId, { [key]: value } as Partial<T>);
    } catch (error) {
        console.error('Failed to update cell:', error);
        setRows(originalRows); // Revert on error
    }
  };

  const handleExportCsv = () => {
    if (!rows.length) return;
    const headers = columns.map(c => c.header);
    const lines = rows.map(r => columns.map(c => {
      let v: any = (r as any)[c.key];
      if (c.type === 'date' && v) v = new Date(String(v)).toLocaleDateString();
      if (c.type === 'link' && c.linkSource === 'ingredients') {
        const ing = linkedData.ingredients.find(i => i.id === v);
        v = ing?.name ?? v ?? '';
      }
      const s = (v ?? '').toString().replace(/"/g, '""');
      return `"${s}"`;
    }).join(','));
    const csv = [headers.join(','), ...lines].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${title.replace(/\s+/g, '_')}.csv`;
    a.click();
  };

  const handleDuplicateSelected = async () => {
    const ids = Array.from(selectedRows);
    for (const id of ids) {
      const original = rows.find(r => r.id === id)!;
      const { id:_, ...rest } = original as any;
      // preserve stage for extractions
      const payload = dataType === 'extractions'
        ? { ...rest, stage: (original as any).stage, stage_label: (original as any).stage_label }
        : rest;
      const newRow = await api.create(payload);
      setRows(prev => [...prev, newRow]);
    }
  };

  const handleCsvUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const text = await file.text();
      const lines = text.split('\n').filter(line => line.trim() !== '');
      if (lines.length < 2) {
        throw new Error("CSV file must have a header and at least one data row.");
      }

      const csvHeadersRaw = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, '').toLowerCase());

      const headerToKeyMap = new Map<string, { key: keyof T; col: Column<T> }>();
      columns.forEach(col => {
        headerToKeyMap.set(col.header.toLowerCase(), { key: col.key, col });
      });

      const newRowsData: Omit<T, 'id'>[] = [];
      for (let i = 1; i < lines.length; i++) {
        // Regex to handle quoted commas
        const values = (lines[i].match(/(".*?"|[^",\r\n]+)(?=\s*,|\s*$)/g) || [])
          .map(v => v.trim().replace(/^"|"$/g, ''));

        if (values.length !== csvHeadersRaw.length) {
          console.warn(`Skipping malformed row ${i + 1}: number of columns does not match header.`);
          continue;
        }

        const rowObject: any = { ...defaultNewRow };

        csvHeadersRaw.forEach((header, index) => {
          const mapping = headerToKeyMap.get(header);
          if (mapping) {
            const { key, col } = mapping;
            let value: any = values[index];

            if (col.type === 'number') {
              value = value === '' || isNaN(parseFloat(value)) ? null : parseFloat(value);
            } else if (col.type === 'date') {
              value = value ? new Date(value).toISOString() : new Date().toISOString();
            } else if (col.type === 'link' && col.linkSource === 'ingredients') {
              const ing = linkedData.ingredients.find(i => i.name.toLowerCase() === value.toLowerCase() || i.batch_id.toLowerCase() === value.toLowerCase());
              value = ing ? ing.id : ''; // Assign empty if not found, could also throw an error
            }
            rowObject[key] = value;
          }
        });

        if (dataType === 'extractions') {
          rowObject.stage = activeStage.key;
          rowObject.stage_label = activeStage.label;
        }

        newRowsData.push(rowObject);
      }

      await Promise.all(newRowsData.map(rowData => api.create(rowData)));

      await fetchData();
      alert(`${newRowsData.length} rows imported successfully!`);

    } catch (error) {
      console.error("Failed to import CSV:", error);
      alert(`An error occurred during CSV import: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsUploading(false);
      if (importCsvInputRef.current) {
        importCsvInputRef.current.value = '';
      }
    }
  };


  const renderCellContent = (row: T, col: Column<T>) => {
    const value = row[col.key];

    if (editingCell?.rowId === row.id && editingCell?.key === col.key && !col.readOnly) {
       if (col.type === 'select' && col.options) {
        return (
          <select
            // FIX: Safely handle value for select input
            value={String(value ?? '')}
            onChange={(e) => handleUpdateCell(row.id, col.key, e.target.value)}
            onBlur={() => setEditingCell(null)}
            autoFocus
            className="w-full bg-gray-900 border border-blue-500 rounded px-1"
          >
            {col.options.map(opt => <option key={opt} value={opt}>{opt || 'None'}</option>)}
          </select>
        );
       }
       if (col.type === 'link' && col.linkSource === 'ingredients') {
        return (
          <select
            // FIX: Safely handle value for select input
            value={String(value ?? '')}
            onChange={(e) => handleUpdateCell(row.id, col.key, e.target.value)}
            onBlur={() => setEditingCell(null)}
            autoFocus
            className="w-full bg-gray-900 border border-blue-500 rounded px-1"
          >
            <option value="">Select Ingredient</option>
            {linkedData.ingredients.map(ing => <option key={ing.id} value={ing.id}>{ing.name} ({ing.batch_id})</option>)}
          </select>
        );
       }
       if (col.type === 'date') {
        return (
          <input
            type="date"
            value={(value ? String(value).slice(0, 10) : '')}
            onChange={(e) => {
              const v = e.target.value ? new Date(e.target.value).toISOString() : '';
              setRows(rows.map(r => r.id === row.id ? { ...r, [col.key]: v } : r));
            }}
            onBlur={(e) => {
              const v = e.target.value ? new Date(e.target.value).toISOString() : '';
              handleUpdateCell(row.id, col.key, v);
              setEditingCell(null);
            }}
            autoFocus
            className="w-full bg-gray-900 border border-blue-500 rounded px-1"
          />
        );
      }
        return (
            <input
                type={col.type === 'number' ? 'number' : 'text'}
                // FIX: Safely handle value for text/number input to avoid uncontrolled component warnings and type errors.
                value={String(value ?? '')}
                onChange={(e) => {
                    const newValue = col.type === 'number' ? (e.target.value === '' ? null : parseFloat(e.target.value)) : e.target.value;
                    setRows(rows.map(r => r.id === row.id ? {...r, [col.key]: newValue} : r));
                }}
                onBlur={(e) => {
                    const newValue = col.type === 'number' ? (e.target.value === '' ? null : parseFloat(e.target.value)) : e.target.value;
                    handleUpdateCell(row.id, col.key, newValue);
                    setEditingCell(null);
                }}
                onKeyDown={(e) => { if(e.key === 'Enter') e.currentTarget.blur() }}
                autoFocus
                className="w-full bg-gray-900 border border-blue-500 rounded px-1"
            />
        );
    }

    if (col.type === 'attachments') {
        return (
            <div className="flex items-center gap-2">
                <button
                    onClick={() => fileInputRef.current?.click()}
                    className="p-1 hover:bg-gray-600 rounded"
                >
                    <AttachmentIcon />
                </button>
                <input type="file" ref={fileInputRef} className="hidden" />
                <span>{(row.attachments || []).length} file(s)</span>
            </div>
        );
    }

    if (col.type === 'link' && col.linkSource === 'ingredients') {
        const ingredient = linkedData.ingredients.find(ing => ing.id === value);
        // FIX: Ensure value is a string before rendering to prevent React errors with object children.
        return <span className="text-blue-400">{ingredient?.name || String(value ?? '')}</span>;
    }

    if (col.type === 'date') {
        return value ? new Date(String(value)).toLocaleDateString() : '';
    }

    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }

    return String(value ?? '');
  };

  const getRowClass = (row: any) => {
    let classes = 'hover:bg-gray-700/50 transition-colors duration-150';
    if (selectedRows.has(row.id)) {
      classes += ' bg-blue-900/50';
    }
    if (dataType === 'extractions' && row.yield_pct > 60) {
      classes += ' bg-green-600/30';
    }
    return classes;
  };

  return (
    <div className="p-8 h-full flex flex-col">
      <h1 className="text-3xl font-bold text-white mb-6">{title}</h1>

      {dataType === 'extractions' && (
        <div className="flex gap-1 mb-4 border-b border-gray-700">
            {stages.map(s => (
            <button key={s.key}
                onClick={() => setActiveStage(s)}
                className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors duration-200 ${activeStage.key===s.key ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}>
                {s.label}
            </button>
            ))}
        </div>
      )}

      <div className="flex items-center gap-2 mb-4 flex-wrap">
        <button onClick={handleAddRow} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"><PlusIcon /> Add Row</button>
        <button onClick={() => setIsVoiceModalOpen(true)} className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"><MicrophoneIcon /> Add by Voice</button>
        <button onClick={handleDeleteSelected} disabled={selectedRows.size === 0} className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors duration-200"><TrashIcon /> Delete Selected</button>
        <button onClick={handleDuplicateSelected} disabled={selectedRows.size === 0} className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors duration-200"><DuplicateIcon /> Duplicate</button>
        <button onClick={handleExportCsv} className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"><ExportIcon /> Export CSV</button>
        <button onClick={() => importCsvInputRef.current?.click()} disabled={isUploading} className="flex items-center gap-2 bg-teal-600 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors duration-200">
            <UploadIcon /> {isUploading ? 'Importing...' : 'Import CSV'}
        </button>
        <input type="file" ref={importCsvInputRef} onChange={handleCsvUpload} accept=".csv" className="hidden" />
      </div>

      <div className="flex-grow overflow-auto bg-gray-800 rounded-lg shadow-lg">
        {loading ? <div className="p-8 text-center">Loading data...</div> : (
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-700/50 sticky top-0">
            <tr>
              <th scope="col" className="p-4">
                <input type="checkbox" onChange={handleSelectAll} className="h-4 w-4 rounded bg-gray-700 border-gray-600 text-blue-600 focus:ring-blue-500"/>
              </th>
              {columns.map(col => (
                <th key={String(col.key)} scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">{col.header}</th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-gray-800 divide-y divide-gray-700">
            {rows.map((row) => (
              <tr key={row.id} className={getRowClass(row)}>
                <td className="p-4">
                  <input type="checkbox" checked={selectedRows.has(row.id)} onChange={() => handleSelectionChange(row.id)} className="h-4 w-4 rounded bg-gray-700 border-gray-600 text-blue-600 focus:ring-blue-500"/>
                </td>
                {columns.map(col => (
                  <td key={String(col.key)} onDoubleClick={() => !col.readOnly && setEditingCell({ rowId: row.id, key: col.key })} className="px-6 py-2 whitespace-nowrap text-sm text-gray-200 cursor-pointer">
                    {renderCellContent(row, col)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        )}
      </div>

      <VoiceInputModal
        isOpen={isVoiceModalOpen}
        onClose={() => setIsVoiceModalOpen(false)}
        onDataAdded={(addedDataType) => {
            if (addedDataType === dataType) {
                fetchData();
            }
        }}
      />
    </div>
  );
};
