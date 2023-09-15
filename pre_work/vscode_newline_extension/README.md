# latex-newline
Replaces end of sentences with new lines in LaTeX files.
```latex
This is a sentence. This is another sentence.
```
becomes
```latex
This is a sentence.
This is another sentence.
```

This will only add new lines, if the sentence has a $\w$ before the period and spaces after the period.
All spaces after the period will be removed.


# Installation

Copy the latex-newline-version.vsix into the VS Code extensions folder located at

- Windows `%USERPROFILE%\.vscode\extensions`
- macOS `~/.vscode/extensions`
- Linux `~/.vscode/extensions`

or execute 
```bash
code --install-extension latex-newline-version.vsix
```


## Known Issues

### 0.0.1
Initial Release

---
