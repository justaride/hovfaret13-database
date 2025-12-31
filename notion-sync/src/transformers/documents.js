import { readFileSync } from 'fs';
import { resolve } from 'path';
import { DATA_DIR } from '../config.js';

export function loadDocuments() {
  const filePath = resolve(DATA_DIR, 'documents.json');
  const data = JSON.parse(readFileSync(filePath, 'utf8'));
  return data.documents || [];
}

export const documentsSchema = {
  'File Name': { title: {} },
  'ID': { rich_text: {} },
  'File Type': { select: {} },
  'Document Type': { select: {} },
  'Category': { select: {} },
  'Source Folder': { rich_text: {} },
  'Extraction Date': { date: {} },
  'Has Error': { checkbox: {} }
};

export function transformDocument(doc) {
  return {
    'File Name': { title: [{ text: { content: (doc.file_name || 'Untitled').slice(0, 2000) } }] },
    'ID': { rich_text: [{ text: { content: doc.id || '' } }] },
    'File Type': doc.file_type ? { select: { name: doc.file_type.slice(0, 100) } } : undefined,
    'Document Type': doc.document_type ? { select: { name: doc.document_type.slice(0, 100) } } : undefined,
    'Category': doc.category ? { select: { name: doc.category.slice(0, 100) } } : undefined,
    'Source Folder': { rich_text: [{ text: { content: (doc.source_folder || '').slice(0, 2000) } }] },
    'Extraction Date': doc.extraction_date ? { date: { start: doc.extraction_date } } : undefined,
    'Has Error': { checkbox: doc.has_error || false }
  };
}
