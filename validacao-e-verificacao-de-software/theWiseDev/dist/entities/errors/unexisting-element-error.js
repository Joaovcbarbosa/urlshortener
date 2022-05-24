"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.UnexistingElementError = void 0;
class UnexistingElementError extends Error {
    constructor() {
        super('Element does not exist.');
        this.name = 'UnexistingElementError';
    }
}
exports.UnexistingElementError = UnexistingElementError;
