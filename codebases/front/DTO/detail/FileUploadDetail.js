export class FileUploadDetail {
  constructor(fileName, status, fileType) {
    this.fileName = fileName;
    this.status = status;
    this.fileType = fileType;
  }

  toFileUploadArray() {
    return {
      fileName: this.fileName,
      status: this.status,
      fileType: this.fileType,
    };
  }

  getFileName() {
    return this.fileName;
  }

  getStatus() {
    return this.status;
  }

  getFileType() {
    return this.fileType;
  }
}
