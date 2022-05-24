"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Lecture = void 0;
const container_1 = require("./container");
class Lecture {
    constructor(title, videoUrl) {
        this.materials = new container_1.Container();
        this.title = title;
        this.videoUrl = videoUrl;
    }
    add(material) {
        return this.materials.add(material);
    }
    includes(material) {
        return this.materials.includes(material);
    }
    remove(material) {
        return this.materials.remove(material);
    }
    position(material) {
        return this.materials.position(material);
    }
    move(material, to) {
        return this.materials.move(material, to);
    }
    equals(other) {
        return this.title === other.title;
    }
}
exports.Lecture = Lecture;
