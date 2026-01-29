import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_FILE = resolve(__dirname, '../cache/id-map.json');

class IdMapper {
  constructor() {
    this.map = this.load();
    this.databases = {};
  }

  load() {
    try {
      if (existsSync(CACHE_FILE)) {
        return JSON.parse(readFileSync(CACHE_FILE, 'utf8'));
      }
    } catch (error) {
      console.warn('Could not load ID map cache:', error.message);
    }
    return { pages: {}, databases: {} };
  }

  save() {
    try {
      writeFileSync(CACHE_FILE, JSON.stringify(this.map, null, 2));
    } catch (error) {
      console.error('Could not save ID map cache:', error.message);
    }
  }

  getNotionPageId(localId, dbName) {
    return this.map.pages[dbName]?.[localId];
  }

  setNotionPageId(localId, notionId, dbName) {
    if (!this.map.pages[dbName]) {
      this.map.pages[dbName] = {};
    }
    this.map.pages[dbName][localId] = notionId;
    this.save();
  }

  getNotionDatabaseId(dbName) {
    return this.map.databases[dbName];
  }

  setNotionDatabaseId(dbName, notionId) {
    this.map.databases[dbName] = notionId;
    this.save();
  }

  getAllPageIds(dbName) {
    return this.map.pages[dbName] || {};
  }

  clear() {
    this.map = { pages: {}, databases: {} };
    this.save();
  }
}

export const idMapper = new IdMapper();
