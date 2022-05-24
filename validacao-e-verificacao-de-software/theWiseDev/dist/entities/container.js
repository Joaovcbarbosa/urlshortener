"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Container = void 0;
const either_1 = require("../shared/either");
const existing_element_error_1 = require("./errors/existing-element-error");
const invalid_position_error_1 = require("./errors/invalid-position-error");
const unexisting_element_error_1 = require("./errors/unexisting-element-error");
class Container {
    constructor() {
        this.elements = [];
    }
    get numberOfElements() {
        return this.elements.length;
    }
    add(element) {
        if (!this.includes(element))
            return either_1.right(this.push(element));
        return either_1.left(new existing_element_error_1.ExistingElementError());
    }
    push(element) {
        this.elements.push(element);
    }
    includes(element) {
        return this.elements.find(p => p.equals(element) === true) !== undefined;
    }
    move(element, to) {
        if (to > this.elements.length || to < 1)
            return either_1.left(new invalid_position_error_1.InvalidPositionError());
        if (!this.includes(element))
            return either_1.left(new unexisting_element_error_1.UnexistingElementError());
        const from = this.position(element).value;
        return either_1.right(moveInArray(this.elements, from - 1, to - 1));
    }
    position(element) {
        const elementInContainer = this.elements.find(p => p.equals(element));
        if (elementInContainer === undefined) {
            return either_1.left(new unexisting_element_error_1.UnexistingElementError());
        }
        return either_1.right(this.elements.indexOf(elementInContainer) + 1);
    }
    remove(element) {
        if (!this.includes(element))
            return either_1.left(new unexisting_element_error_1.UnexistingElementError());
        const positionInArray = this.position(element).value - 1;
        return either_1.right(this.splice(positionInArray, 1));
    }
    splice(position, numberOfElements) {
        this.elements.splice(position, numberOfElements);
    }
}
exports.Container = Container;
function moveInArray(array, from, to) {
    const element = array.splice(from, 1)[0];
    array.splice(to, 0, element);
}
