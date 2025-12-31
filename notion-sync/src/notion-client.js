import { Client } from '@notionhq/client';
import { NOTION_TOKEN } from './config.js';

if (!NOTION_TOKEN) {
  console.error('Missing NOTION_TOKEN in .env file');
  process.exit(1);
}

export const notion = new Client({ auth: NOTION_TOKEN });

export async function testConnection() {
  try {
    const user = await notion.users.me();
    console.log(`Connected as: ${user.name || user.id}`);
    return true;
  } catch (error) {
    console.error('Failed to connect to Notion:', error.message);
    return false;
  }
}
