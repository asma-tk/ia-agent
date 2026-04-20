// Utility to trigger download of a file from /files directory
function triggerDownload(filename) {
  const link = document.createElement('a'); // Create a temporary link element
  link.href = `../files/${filename}`;// Set the href to the file URL
  link.download = filename; // Set the download attribute to suggest a filename
  document.body.appendChild(link);// Append the link to the body
  link.click();   // Programmatically click the link to trigger the download
  document.body.removeChild(link); // Clean up by removing the link from the document
}

