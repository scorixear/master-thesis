// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "latex-newline" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('latex-newline.replace_dots', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.activeTextEditor?.edit(editBuilder => {
			editBuilder.replace(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(100000, 100000)), replaceDots(vscode.window.activeTextEditor?.document.getText()) ?? '');
		});
	});

	context.subscriptions.push(disposable);
}

export function replaceDots(text: string | undefined) {
	let allowed = ['Mr.', 
	'Mrs.', 
	'Ms.', 
	'Dr.', 
	'Prof.', 
	'St.', 
	'Mt.', 
	'etc.', 
	'e.g.', 
	'i.e.',
	'cf.',
	'vs.',
	'Fig.',
	'Figs.',
	'Eq.',
	'Eqs.',
	'Sec.',
	'Secs.',
	'Ch.',
	'Chs.',
	'App.',
	'Apps.',
	'Ref.',
	'Refs.',
	'Jan.',
	'Feb.',
	'Mar.',
	'Apr.',
	'Jun.',
	'Jul.',
	'Aug.',
	'Sep.',
	'Sept.',
	'Oct.',
	'Nov.',
	'Dec.',
	'Dez.',
	'Mon.',
	'Tue.',
	'Wed.',
	'Thu.',
	'Fri.',
	'Sat.',
	'Sun.',
	'a.m.',
	'p.m.',
	'et al.',
	'engl.',
	'approx.',
	'z.',
	'Z.',];
	allowed = allowed.map((word) => ' '+word.replace('.', '\\.')+ ' ');
	const allowedRegex = new RegExp('('+allowed.join('|')+')', 'g');
	text = text?.replace(allowedRegex, (match) => match.replace(/\./g, '§§LATEX_NEWLINE§§'));
	text = text?.replace(/(\w{2,}\.) +([^ .]{2})/g, '$1\n$2');
	text = text?.replace(/§§LATEX_NEWLINE§§/g, '.');
	return text;
}

// This method is called when your extension is deactivated
export function deactivate() {}
