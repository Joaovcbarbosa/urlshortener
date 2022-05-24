"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateCourse = void 0;
class CreateCourse {
    constructor(repo) {
        this.repo = repo;
    }
    async perform(request) {
        this.repo.add(request);
    }
}
exports.CreateCourse = CreateCourse;
