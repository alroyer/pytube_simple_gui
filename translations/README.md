## Translations

Run the following command to extract text from the source code.

```console
pyside6-lupdate pytube_simple_gui/gui/main_window.py -ts translations/<language>.ts
```

Translate the file **translations/\<language\>.ts** using a text editor. The run the following
command to generate binary file.

```console
pyside6-lrelease translations/<language>.ts -qm pytube_simple_gui/translations/tr.<language>.qm
```
