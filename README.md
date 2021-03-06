# MathTreadmill-TUI
## Installation
``git clone https://github.com/michaelskyba/MathTreadmill-TUI.git``
## Usage
```
cd /path/to/MathTreadmill-TUI
python main.py
```
Add
``alias mt="cd /path/to/MathTreadmill-TUI && python main.py"``
or something similar to your shell's config file to make it faster to type!

``python /path/to/MathTreadmill-TUI`` will break, because the script needs to use the other files in the directory.

### Controls
- Up/Down arrow keys OR k/j: Move up or down, respectively, in menus
- 0-9: Append a number to your answer
- "-" (dash/minus): Add a negation sign to the start of your answer, only if it's blank
- Enter: Submit your answer, or choose the currently selected option in a menu
- q: Quit
- f: Forfeit the current question, revealing the answer

## Making your own level
A 'level' is a set of questions that you might want to practice together.
1. Create a config file for your level, which will just have one line in the
   form "\<starting time\> \<decrement\>", both of which are in seconds.
2. Create a 'questions' file for your level, which will specify a list of
   question types, in the form "\<type\> \<first min\> \<first max\> \<second min\>
   \<second max\> [AN]". Look at the auto_questions or example_*_questions files
   for examples, although it's important to note that the auto_questions file
   will have 'skill numbers' (e.g. 3.2), which you shouldn't include.
3. Edit ``MathTreadmill-TUI/custom/levels`` to source the two files that you just made. Look inside the file for the syntax.

If you've read the instructions and tinkered with the examples but still can't get something to work,
email me at michaelskyba1411@gmail.com, and I'll try to help you out.

## Supported Operating Systems
The only 'officially' supported OS is GNU/Linux (i.e. I won't help you install
it on Windows 10, for instance), but you should be able to get it working on
anything that supports Python and ncurses.

## Screenshot
![Screenshot](https://michaelskyba.github.io/assets/mt-TUI.png)
