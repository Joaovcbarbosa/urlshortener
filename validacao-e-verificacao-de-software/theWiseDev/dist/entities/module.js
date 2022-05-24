"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Module = void 0;
const container_1 = require("./container");
class Module {
    constructor(title) {
        this.lectures = new container_1.Container();
        this.title = title;
    }
    get numberOfLectures() {
        return this.lectures.numberOfElements;
    }
    add(lecture) {
        return this.lectures.add(lecture);
    }
    includes(lecture) {
        return this.lectures.includes(lecture);
    }
    move(lecture, position) {
        return this.lectures.move(lecture, position);
    }
    position(lecture) {
        return this.lectures.position(lecture);
    }
    remove(lecture) {
        return this.lectures.remove(lecture);
    }
    equals(module) {
        return this.title === module.title;
    }
}
exports.Module = Module;
