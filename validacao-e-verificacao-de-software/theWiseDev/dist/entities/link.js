"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Link = void 0;
class Link {
    constructor(title, url) {
        this.title = title;
        this.url = url;
    }
    equals(link) {
        return this.title === link.title;
    }
}
exports.Link = Link;
