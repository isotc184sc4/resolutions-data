import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(__dirname, 'dist');
const publicDir = path.join(__dirname, 'public');

const server = http.createServer((req, res) => {
  // Strip query string from URL
  const urlWithoutQuery = req.url.split('?')[0];
  let filePath = path.join(distDir, urlWithoutQuery);
  
  // Check if file exists in dist
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error reading file');
        return;
      }
      
      const ext = path.extname(filePath);
      let contentType = 'text/html';
      if (ext === '.js') contentType = 'application/javascript';
      if (ext === '.css') contentType = 'text/css';
      if (ext === '.json') contentType = 'application/json';
      if (ext === '.svg') contentType = 'image/svg+xml';
      if (ext === '.png') contentType = 'image/png';
      if (ext === '.ico') contentType = 'image/x-icon';
      
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    });
    return;
  }
  
  // Check if file exists in public
  const publicPath = path.join(publicDir, urlWithoutQuery);
  if (fs.existsSync(publicPath) && fs.statSync(publicPath).isFile()) {
    fs.readFile(publicPath, (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error reading file');
        return;
      }
      
      const ext = path.extname(publicPath);
      let contentType = 'text/html';
      if (ext === '.js') contentType = 'application/javascript';
      if (ext === '.css') contentType = 'text/css';
      if (ext === '.json') contentType = 'application/json';
      if (ext === '.svg') contentType = 'image/svg+xml';
      if (ext === '.png') contentType = 'image/png';
      if (ext === '.ico') contentType = 'image/x-icon';
      
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    });
    return;
  }
  
  // Handle SPA routing - serve index.html for all non-file routes
  fs.readFile(path.join(distDir, 'index.html'), (err, data) => {
    if (err) {
      // Serve 404.html for SPA fallback
      fs.readFile(path.join(distDir, '404.html'), (err2, data2) => {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end(data2 || 'Not Found');
      });
      return;
    }
    
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(data);
  });
});

server.listen(5173, '127.0.0.1', () => {
  console.log('Server running at http://127.0.0.1:5173/');
});
