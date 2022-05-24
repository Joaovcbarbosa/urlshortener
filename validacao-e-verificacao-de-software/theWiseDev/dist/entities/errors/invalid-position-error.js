"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.InvalidPositionError = void 0;
class InvalidPositionError extends Error {
    constructor() {
        super('Invalid position.');
        this.name = 'InvalidPositionError';
    }
}
exports.InvalidPositionError = InvalidPositionError;
