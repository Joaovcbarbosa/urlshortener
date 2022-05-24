"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Pdf = void 0;
class Pdf {
    constructor(title, url) {
        this.title = title;
        this.url = url;
    }
    equals(pdf) {
        return this.title === pdf.title;
    }
}
exports.Pdf = Pdf;
