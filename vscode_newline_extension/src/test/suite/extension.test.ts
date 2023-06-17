import * as assert from 'assert';

// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
import * as vscode from 'vscode';
// import * as myExtension from '../../extension';
import { replaceDots } from '../../extension';

suite('Extension Test Suite', () => {
	vscode.window.showInformationMessage('Start all tests.');
	test('New Line for end of sentence', () => {
		assert.strictEqual(replaceDots('Hello World. New Line'), 'Hello World.\nNew Line');
		assert.strictEqual(replaceDots('Hello World. New Line. New Line'), 'Hello World.\nNew Line.\nNew Line');
	});
	test('Double Dots do not break', () => {
		assert.strictEqual(replaceDots('Hello World.. New Line'), 'Hello World.. New Line');
	});

	test('No Dots do not break', () => {
		assert.strictEqual(replaceDots('Hello World New Line'), 'Hello World New Line');
	});

	test('Dots at begging do not break', () => {
		assert.strictEqual(replaceDots('.Hello World New Line'), '.Hello World New Line');
	});

	test('Dots at end do not break', () => {
		assert.strictEqual(replaceDots('Hello World New Line.'), 'Hello World New Line.');
		assert.strictEqual(replaceDots('Hello World New Line.  '), 'Hello World New Line.  ');
	});

	test('single Letter words do not end sentence', () => {
		assert.strictEqual(replaceDots('Hello W. Not Newline'), 'Hello W. Not Newline');
		assert.strictEqual(replaceDots('Hello World. Z. Not New Line'), 'Hello World.\nZ. Not New Line');
	});

	test('Abbreviations do not end sentence', () => {
		assert.strictEqual(replaceDots('Hello Mr. Not Newline'), 'Hello Mr. Not Newline');
		assert.strictEqual(replaceDots('Hello World. Mr. Not New Line'), 'Hello World.\nMr. Not New Line');
		
	});
});
