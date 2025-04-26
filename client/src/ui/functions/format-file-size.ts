function formatFileSize (bytes: number): string {
  if (bytes < 1024) return bytes + 'B';
  else if (bytes < 1048576) return Math.round(bytes / 1024) + 'KB';
  else return Math.round(bytes / 1048576) + 'MB';
};

export default formatFileSize;