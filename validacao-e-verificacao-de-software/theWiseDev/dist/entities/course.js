"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Course = void 0;
const container_1 = require("./container");
class Course {
    constructor(reference, description, title) {
        this.elements = new container_1.Container();
        this.reference = reference;
        this.title = title;
        this.description = description;
    }
    get numberOfElements() {
        return this.elements.numberOfElements;
    }
    add(element) {
        return this.elements.add(element);
    }
    remove(element) {
        return this.elements.remove(element);
    }
    includes(element) {
        return this.elements.includes(element);
    }
    move(element, position) {
        return this.elements.move(element, position);
    }
    position(element) {
        return this.elements.position(element);
    }
    moveLecture(lecture, from, toModule, position) {
        from.remove(lecture);
        toModule.add(lecture);
        const currentLecturePosition = toModule.position(lecture).value;
        if (currentLecturePosition !== position)
            toModule.move(lecture, position);
    }
    equals(other) {
        return this.title === other.title || this.reference === other.reference;
    }
}
exports.Course = Course;
