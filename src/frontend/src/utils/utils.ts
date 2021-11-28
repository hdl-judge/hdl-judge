export function createAndDownloadFile(base64: string, filename: string): void {
    const body = base64ToArrayBuffer(base64);
    const blob = new Blob([body]);
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function base64ToArrayBuffer(base64: string) {
    const binaryString = window.atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    return bytes.map((byte, i) => binaryString.charCodeAt(i));
}

export const getStorageKey = (id: number, user: string) => `project-${id}-user`;

export const getMossKey = (projectId: number) => `moss-${projectId}`;