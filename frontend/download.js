// Utility to trigger download of a file from /files directory
function triggerDownload(filename) {
  const link = document.createElement('a');
  link.href = `/files/${filename}`;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Example usage:
// triggerDownload('asma');

// You can call triggerDownload('yourfilename') from anywhere in your app.
