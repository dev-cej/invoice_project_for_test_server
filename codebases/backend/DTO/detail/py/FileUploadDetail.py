class FileUploadDetail:
    """
    파일 업로드의 세부 정보를 저장하는 클래스
    """

    def __init__(self, status: str, file_type: str):
        self._status = status
        self._file_type = file_type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    def to_dict(self) -> dict:
        return {
            'status': self.status,
            'fileType': self.file_type,
        }
