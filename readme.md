# Python Web-Launcher

## Visual Studio Solution

### Build Output

Good read on how to copy output to the appropriate directory. [https://social.technet.microsoft.com/wiki/contents/articles/53248.visual-studio-copying-files-to-debug-or-release-folder.aspx]

```
copy "$(OutDir)\launcher.exe" $(SolutionDir)..
```
### Icon

[https://stackoverflow.com/questions/2393863/set-an-exe-icon-for-my-program]

## Virtual Environment

You can package a python virtual environment so the end users don't need to install python.

Follow this guide to install a virtualenv in the repo. [https://docs.python.org/3.6/tutorial/venv.html]

Use the venv to install dependencies.

### Errors
If you encounter this error,

```
...
cannot be loaded because running scripts is disabled on this system.
...
```

Try using the following command in another powershell running as admin. 

```
powershell Set-ExecutionPolicy RemoteSigned
```