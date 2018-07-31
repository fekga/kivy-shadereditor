# kivy-shadereditor
(see also <https://kivy.org/docs/examples/gen__demo__shadereditor__main__py.html>)

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

## Developer Notes
### how to only fix the issues in fekga version and not make 3D:
Add the following to the end of shader:
```kv
        Label:
            id: lineLabel
            text: ''
            size_hint_y: None
            height: 16
        Label:
            id: colLabel
            text: ''
            size_hint_y: None
            height: 16
```

and add the following method to class GameApp:
```python
    def show_cursor_info(self, cursor_row, cursor_col):
        self.ids.lineLabel.text = "line " + str(cursor_row+1)
        self.ids.colLabel.text = " column " + str(cursor_col+1)
```

So when you get a shader error in the console such as:
```
[ERROR  ] [Shader      ] <fragment> failed to compile (gl:0)
[INFO   ] [Shader      ] fragment shader: <b"0:89(45): error: syntax error, unexpected ';', expecting ')' or ','">
```

Then you can fix a problem by finding and fixing the line.

To actually fix the initial commit version of the shader code:
* add the missing ')' before the semicolon on line 89 (as per error shown above); same for line 95.
* rename the shader function `vec2 cmult` to `vec2 c_mul`
* change all 3 instances of z. to a. on line 37
