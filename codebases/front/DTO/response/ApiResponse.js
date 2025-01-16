export class ApiResponse {
    constructor({ status = '', message = '', data = {} } = {}) {
        this.status = status;
        this.message = message;
        this.data = data;
    }

    toJson() {
        return JSON.stringify({
            status: this.status,
            message: this.message,
            data: this.data
        });
    }

    getStatus() {
        return this.status;
    }

    getMessage() {
        return this.message;
    }

    getData() {
        return this.data;
    }
}