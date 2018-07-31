# kivy-shadereditor
(see also <https://kivy.org/docs/examples/gen__demo__shadereditor__main__py.html>)
Highlight and check your shader syntax.

## Usage:
* run this program in a IDE that shows console output, such as Geany
* If your shader has errors, look for line number in your console output (such as 89 in:
```
[ERROR  ] [Shader      ] <fragment> failed to compile (gl:0)
[INFO   ] [Shader      ] fragment shader: <b"0:89(45): error: syntax error, unexpected ';', expecting ')' or ','">
```
).
* click on lines to see what line your cursor is currently on until you find the correct line
* fix the line according to whatever error message you see after `fragment shader:`
* If all errors are fixed, then the last line in the console (possibly after former `[Shader      ]` errors, which in this case would no longer be relevant) should now say `Compiled!`.
