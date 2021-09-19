export function createAndDownloadFile(inputString: string, filename: string, extension: string): void {
    const bytes = new Uint8Array(inputString.length);
    const body = bytes.map((byte, i) => inputString.charCodeAt(i));
    const blob = new Blob([body]);
    const fileName = `${filename}.${extension}`;
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', fileName);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}