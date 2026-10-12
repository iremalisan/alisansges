/// <reference types="vitest/config" />
import type { Connect, Plugin } from 'vite';
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { WORD_DOCUMENT_FILENAME, WORD_DOCUMENT_PATH } from './src/downloads';

function wordFileDownloadPlugin(): Plugin {
  const disposition = `attachment; filename="2025-is-akim-semasi-ve-proses-ozeti-vaziyet-planlari.docx"; filename*=UTF-8''${encodeURIComponent(WORD_DOCUMENT_FILENAME)}`;

  const attach: Connect.NextHandleFunction = (req, res, next) => {
    const path = decodeURIComponent((req.url ?? '').split('?')[0] ?? '');
    if (path === WORD_DOCUMENT_PATH) {
      res.setHeader(
        'Content-Type',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      );
      res.setHeader('Cache-Control', 'no-store');
      res.setHeader('Content-Disposition', disposition);
    }
    next();
  };

  return {
    name: 'word-file-download',
    configureServer(server) {
      server.middlewares.use(attach);
    },
    configurePreviewServer(server) {
      server.middlewares.use(attach);
    },
  };
}

export default defineConfig({
  plugins: [wordFileDownloadPlugin(), react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
  },
});
