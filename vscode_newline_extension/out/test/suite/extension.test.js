"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
const vscode = require("vscode");
// import * as myExtension from '../../extension';
const extension_1 = require("../../extension");
suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');
    test('New Line for end of sentence', () => {
        assert.strictEqual((0, extension_1.replaceDots)('Hello World. New Line'), 'Hello World.\nNew Line');
        assert.strictEqual((0, extension_1.replaceDots)('Hello World. New Line. New Line'), 'Hello World.\nNew Line.\nNew Line');
        assert.strictEqual((0, extension_1.replaceDots)('Hellow 1. New Line'), 'Hellow 1.\nNew Line');
    });
    test('Double Dots do not break', () => {
        assert.strictEqual((0, extension_1.replaceDots)('Hello World.. New Line'), 'Hello World.. New Line');
    });
    test('No Dots do not break', () => {
        assert.strictEqual((0, extension_1.replaceDots)('Hello World New Line'), 'Hello World New Line');
    });
    test('Dots at begging do not break', () => {
        assert.strictEqual((0, extension_1.replaceDots)('.Hello World New Line'), '.Hello World New Line');
    });
    test('Dots at end do not break', () => {
        assert.strictEqual((0, extension_1.replaceDots)('Hello World New Line.'), 'Hello World New Line.');
        assert.strictEqual((0, extension_1.replaceDots)('Hello World New Line.  '), 'Hello World New Line.  ');
    });
    test('single Letter words do not end sentence', () => {
        assert.strictEqual((0, extension_1.replaceDots)('Hello W. Not Newline'), 'Hello W. Not Newline');
        assert.strictEqual((0, extension_1.replaceDots)('Hello World. Z. Not New Line'), 'Hello World. Z. Not New Line');
    });
});
//# sourceMappingURL=extension.test.js.map