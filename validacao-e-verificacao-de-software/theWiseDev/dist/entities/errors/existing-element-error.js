"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExistingElementError = void 0;
class ExistingElementError extends Error {
    constructor() {
        super('Element already exists.');
        this.name = 'ExistingElementError';
    }
}
exports.ExistingElementError = ExistingElementError;
