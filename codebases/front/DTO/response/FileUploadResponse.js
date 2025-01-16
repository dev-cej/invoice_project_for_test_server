import { ApiResponse } from "./ApiResponse.js";
import { ExtractResult } from "../detail/ExtractResult.js";

export class FileUploadResponse extends ApiResponse {
  constructor({ status = "", message = "", data = {} } = {}) {
    super(status, message, data);

    console.log(
      "FileUploadResponse 생성자 - data.extract_result:",
      data.extract_result
    );
    this.status = status;
    this.message = message;
    this.data = data;
    this.data.extract_result = (data.extract_result || []).map(
      (result) => new ExtractResult(result)
    );
  }

  getExtractResult() {
    return this.data.extract_result;
  }

  setExtractResult(value) {
    this.data.extract_result = value.map((result) => new ExtractResult(result));
  }
}
