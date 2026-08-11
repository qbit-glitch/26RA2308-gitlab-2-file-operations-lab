# File Operations Lab Assignment: Kestrel-1, Second Morning

**Course:** 26RA2308 Git for Software Development and Collaboration
**Based on:** Experiment 2 (Linux Terminal: File Operations and Productivity)
**Time allowed:** 1 hour 30 minutes. **Marks:** 100

---

## The story

It is 08:00 on your second morning at the Kestrel-1 rover lab. Today is the field test and the truck leaves at noon.
**Asha** writes the C firmware, **Ben** plans the routes and keeps the team log, **Chitra** tunes the camera detector.
All three want something from `robot-controller`, the project folder from yesterday: it now holds the team log, old
notes, C and Python sources and a few leftovers. There is no desktop and no mouse, so you work in the terminal, and
this morning the lab has two rules:

> **Read before you change. Delete only what you meant to delete.**

During your shift you will read files, write a note, edit a file in nano, copy, move and delete files, and search the
folder for words and for file names. Every command is from Experiment 2: `cat`, `head`, `tail -5`, `echo` with `>` and
`>>`, `cp` and `cp -r`, `mv`, `rm`, `rm -r` and `rm -i`, `grep -rn` and `find`, plus `nano` and Tab completion.
`pwd`, `ls`, `cd` and `mkdir` are from Experiment 1.

## What you need

A terminal on Ubuntu or Debian, macOS Terminal, or Git Bash on Windows (Windows is the least tested), with
`python3`, `nano` and `git`. Check with `python3 --version && git --version` (on Windows Git Bash, if `python3` is not
found, type `python` instead of `python3` here and in every command). Git is used for two commands only:
cloning the lab, and `git checkout --` to bring back a lab file you deleted by mistake. nano comes with Ubuntu and
macOS; do not test it by giving it options, because on a Mac that opens the editor (leave it with `Ctrl+X`). If a long
output opens in a pager (a screen with `:` or `(END)` at the bottom), press `q` to leave it.

## Start: get the lab

Clone into your **home directory** (the folder `cd ~` takes you to), so that every "Start here" line below works.
This is not a numbered step and nothing is pasted for it.

```bash
cd ~
git clone https://github.com/qbit-glitch/26RA2308-gitlab-2-file-operations-lab.git file-operations-lab
cd file-operations-lab
cp submission/outputs.template.txt submission/outputs.txt
```

Now open your answer file in nano, press `Ctrl+E` (the cursor jumps to the end of line 1, which reads
`Name   :`), type a space and your full name, then save and leave (next section).

```bash
nano submission/outputs.txt
```

## How to edit a file with nano

Every file you write in this lab is written in the `nano` editor, with two exceptions that the tasks point out:
Task 2 and step 8.2 write files with `>` and `>>` on purpose.

1. `nano <file>` opens the file (a new file is created when you save).
2. The cursor starts at the **top**. Type exactly the text shown. Do **not** press `Enter` after the last line:
   nano ends the file with a line break by itself.
3. Save with `Ctrl+O` and then `Enter` (that confirms the file name).
4. Leave with `Ctrl+X`.

If nano says "Save modified buffer?", press `Y` and then `Enter`. If you typed into the wrong file, press `Ctrl+X`,
then `N`, and start again. Whenever the text shows `Your Full Name`, type your own name, exactly as on line 1 of
`submission/outputs.txt`.

## Rules

1. Remember the house rules: read before you change, delete only what you meant to delete. `rm` has no undo. Work
   **only inside your own clone**, in your home directory, and only in `robot-controller` (and `submission`).
2. Use only the commands shown.
3. Type the commands yourself. The grader checks that your pasted output matches what is really in your clone, so
   output copied from a classmate is detected.
4. **Every task starts with a "Start here" line.** Run it first. It puts you in the right folder whatever you did
   before, so a task you skipped never gets in the way of the next one.
5. A Finder `.DS_Store` file may show up in a listing on a Mac: that is fine, but any other extra file in a listing (one
   you saved in the wrong folder, for example) makes that step's check fail, so look before you paste. The group and
   other permission letters, the owner, the group, the dates and the link counts differ from computer to computer, so
   they are never marked. The order of the lines `grep` and `find` print differs too, and the grader does not mind.

## How you hand in your work

1. You copied `submission/outputs.template.txt` to `submission/outputs.txt` and wrote your name at the top.
2. After **each numbered step** (they are numbered **1.1**, **1.2**, ...), paste what the terminal printed under the
   matching `--- N.M` line of `submission/outputs.txt`, replacing `(paste output here)`. Do not edit or delete the
   `=== TASK` and `--- N.M` lines. Type your answers after the colon of the `ANSWER-n :` lines (the line just below
   each `# Qn` question). Any editor is fine for `submission/outputs.txt`, for example a second terminal with nano or
   VS Code: the nano rule is for the files you create in the lab. To open `submission/outputs.txt` again from any folder
   (a second terminal starts in your home folder), type:

   ```bash
   nano ~/file-operations-lab/submission/outputs.txt
   ```

3. Run the automatic grader whenever you want to see where you stand. This command works from any folder, so you do
   not have to leave `robot-controller`:

   ```bash
   python3 ~/file-operations-lab/tests/grade.py
   ```

   It prints **PASS** or **FAIL** for every task, tells you exactly which check failed, and shows your score out of
   100. You can fix a mistake and run it again as often as you like.
4. When you are done, show the final grader output to your instructor (it is also saved in `submission/results.txt`)
   and submit `submission/outputs.txt` as instructed.

## Time plan

| Task | Time on the clock | Topic | Suggested time | Marks |
|---|---|---|---|---|
| | 08:00 | Setup: clone the lab, copy the template, write your name | 5 min | |
| 1 | 08:05 | Read what is there | 7 min | 14 |
| 2 | 08:12 | Write with echo | 7 min | 12 |
| 3 | 08:19 | Edit with nano | 8 min | 12 |
| 4 | 08:27 | Copy | 6 min | 12 |
| 5 | 08:33 | Move and rename | 5 min | 10 |
| 6 | 08:38 | Delete | 8 min | 14 |
| 7 | 08:46 | Search | 10 min | 16 |
| 8 | 08:56 | Productivity and report | 7 min | 10 |
| | | Buffer for the grader and for fixing mistakes | 27 min | |

**Skipped a task, or running behind?** You do not lose the rest of the lab. Tasks 1 to 4 do not depend on each other.
Task 5 needs the copy that Task 4 makes, and Task 6 needs what Tasks 4 and 5 leave behind: each of them has a
**catch-up box** that rebuilds what you missed in a few lines. Tasks 7 and 8 only read your folder, so they work
whatever you skipped.

---

## Task 1: Read what is there (14 marks)

**Start here:** you have just cloned the lab, so run `cd ~/file-operations-lab/robot-controller`.  
**Needs:** nothing.

> **Ben:** Morning! Yesterday you built `robot-controller`, and it is full of our stuff now. Before you touch
> anything, read the team log. `cat` prints a whole file, `head` the first ten lines, `tail -5` the last five.

```bash
cd ~/file-operations-lab/robot-controller
```

**1.1** Print the folder you are in. It must end in `file-operations-lab/robot-controller`.

```bash
pwd
```

**1.2** Print the whole team log.

```bash
cat mission_log.txt
```

**1.3** Print only the first lines of it.

```bash
head mission_log.txt
```

**Question 1.** How many lines of `mission_log.txt` did `head` **not** show? Compare 1.2 and 1.3. Type the number on
the `ANSWER-1` line of `submission/outputs.txt`.

**1.4** Print only the last five lines.

```bash
tail -5 mission_log.txt
```

**Question 2.** At what time is the last entry of the log (see 1.4)? Type it on the `ANSWER-2` line.

*Think (not marked):* what would `tail` print without the `-5`?

## Task 2: Write with echo (12 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** nothing.

> **Asha:** I need a short notes file for the field test. `echo "text"` prints text. Put `>` after it and the text
> goes into a file instead, **replacing everything that was in it**. Put `>>` and it is **added at the end**. In this
> task you write with `>` and `>>`, not with nano.

```bash
cd ~/file-operations-lab/robot-controller
```

**2.1** `notes.txt` already holds something old. Look at it first.

```bash
cat notes.txt
```

**Question 3.** How many lines did `notes.txt` hold before you change it (see 2.1)? Type the number on the `ANSWER-3`
line. You are about to lose them for good.

**2.2** Write the first line with a single `>` and print the file. What happened to the old lines?

```bash
echo "# Lab notes" > notes.txt && cat notes.txt
```

**2.3** Add a line at the end with `>>`.

```bash
echo "Sensor threshold: 50 cm" >> notes.txt && cat notes.txt
```

**2.4** Add a third line with `>>`.

```bash
echo "TODO: test with real hardware" >> notes.txt && cat notes.txt
```

*Think (not marked):* what would have happened to the first two lines if you had used `>` again in 2.3?

## Task 3: Edit with nano (12 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** nothing.

> **Chitra:** `sensor.py` is empty, and I need a function there that says whether the rover must stop. Write it in
> nano and put your name in the first line.

```bash
cd ~/file-operations-lab/robot-controller
```

**3.1** Open `sensor.py` in nano and type these three lines (with your own name), save and leave. Then print the file.
The indentation of the third line is four spaces.

```bash
nano sensor.py
```

```text
# sensor.py - Your Full Name
def stop_distance(cm):
    return cm < 50
```

```bash
cat sensor.py
```

**3.2** Look at the file's size.

```bash
ls -l sensor.py
```

**Question 4.** How many bytes is `sensor.py` in the 3.2 listing? It is the number just before the date. Type it on the
`ANSWER-4` line.

## Task 4: Copy (12 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** nothing. (An empty `sensor.py` copies just as well.)

> **Asha:** Before the field test we keep copies of everything we touch. `cp` copies a file. A folder needs
> `cp -r`, which copies everything inside it too.

```bash
cd ~/file-operations-lab/robot-controller
```

**4.1** Copy `sensor.py` to `sensor_backup.py` and list everything in the folder, hidden names included.

```bash
cp sensor.py sensor_backup.py && ls -la
```

**4.2** Copy the whole `src` folder to `src_backup` and list the folder.

```bash
cp -r src src_backup && ls
```

**4.3** Look inside the copy: it must hold the same as `src/motor`.

```bash
ls src_backup/motor
```

## Task 5: Move and rename (10 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** the copy `sensor_backup.py` of Task 4. If you skipped Task 4, run this catch-up box first:

```bash
cd ~/file-operations-lab/robot-controller
cp sensor.py sensor_backup.py
```

> **Ben:** Tidy up: the backup needs a better name, and old files belong in an archive folder. `mv` renames a file;
> `mv file folder/` moves it. Nothing is copied: the file is simply somewhere else afterwards.

```bash
cd ~/file-operations-lab/robot-controller
```

**5.1** Rename `sensor_backup.py` to `sensor_old.py` and list the folder.

```bash
mv sensor_backup.py sensor_old.py && ls
```

**5.2** Make a folder `archive`, move `sensor_old.py` into it, and list what is in `archive`.

```bash
mkdir archive && mv sensor_old.py archive/ && ls archive/
```

**5.3** List the folder you are in. Where did `sensor_old.py` go?

```bash
ls
```

## Task 6: Delete (14 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** the folder `archive` with `sensor_old.py` in it (Task 5) and the copy `src_backup` (Task 4). If you skipped
Task 4 or Task 5, run this catch-up box first:

```bash
cd ~/file-operations-lab/robot-controller
mkdir -p archive
cp sensor.py archive/sensor_old.py
cp -r src src_backup
```

> **Asha:** Now the dangerous part: `rm` deletes for good, there is no Recycle Bin. `rm file` deletes a file,
> `rm -r folder/` deletes a folder with everything in it, and `rm -i file` asks you first. Read each command twice
> before you press Enter. Delete the copies, never the originals.

```bash
cd ~/file-operations-lab/robot-controller
```

**6.1** Delete the file in `archive` and list the folder with hidden names. It must be empty now.

```bash
rm archive/sensor_old.py && ls -la archive
```

**6.2** Delete the empty folder `archive` and list the folder you are in.

```bash
rm -r archive/ && ls
```

**6.3** `old_motor.c` is obsolete. Delete it, but let `rm` ask you first. It asks something like `remove old_motor.c?`:
type `y` and press `Enter`. Then list the folder.

```bash
rm -i old_motor.c
```

```bash
ls
```

**6.4** Delete the copy of the source folder (the copy, not `src`!) and list the folder.

```bash
rm -r src_backup && ls
```

*Think (not marked):* what would `rm -r src` have done instead of 6.4? The last section of this handout shows how to
bring a deleted lab file back.

## Task 7: Search (16 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** nothing. (These steps read whatever your folder holds.)

> **Chitra:** Last job before the truck leaves: what is still open, and where is everything? `grep -rn "word" .`
> looks for a word in every file below the current folder (`.`), and prints `./file:line number:the line`. `find`
> looks for files by name. The lines may come in any order.

```bash
cd ~/file-operations-lab/robot-controller
```

**7.1** Find every line with the word `TODO`.

```bash
grep -rn "TODO" .
```

**Question 5.** How many lines did that print? Type the number on the `ANSWER-5` line.

**7.2** Find every line with the word `import`.

```bash
grep -rn "import" .
```

**Question 6.** Which file has the most lines with `import` in the 7.2 output? Type the file name only on the
`ANSWER-6` line.

**7.3** List every Python file in the folder tree.

```bash
find . -name "*.py"
```

**7.4** Python leaves compiled copies (`.pyc`) behind. Make two fake ones with `cp` and list them.

```bash
cp sensor.py sensor.pyc && cp src/motor/pwm.py src/motor/pwm.pyc && find . -name "*.pyc"
```

**7.5** Delete all `.pyc` files with one command, then list `src/motor` to see that `pwm.py` is still there.

```bash
find . -name "*.pyc" -delete && ls src/motor
```

*Think (not marked):* why is `grep -rn "import" .` not a good way to find all Python files?

## Task 8: Productivity and report (10 marks)

**Start here:** `cd ~/file-operations-lab/robot-controller`  
**Needs:** nothing.

> **Ben:** A good shell saves typing. Press `Tab` and it completes a name for you; and `>` can save the output of
> any command in a file, not only of `echo`.

```bash
cd ~/file-operations-lab/robot-controller
```

**8.1** Type `ls -l mis` and press `Tab`: the shell completes the file name. Check that the line reads as below, then
press `Enter`.

```bash
ls -l mission_log.txt
```

**8.2** Save the list of Python files in a file with `>`, and print that file.

```bash
find . -name "*.py" > py_files.txt && cat py_files.txt
```

**8.3** Open a new file `summary.txt` in nano and type this one line (with your own name), save and leave. Then print
the file.

```bash
nano summary.txt
```

```text
Summary: all files organised - Your Full Name
```

```bash
cat summary.txt
```

*Try (not marked):* press the **Up** arrow to bring back the last command; `Ctrl+L` clears the screen; `Ctrl+A` and
`Ctrl+E` jump to the start and the end of the line you are typing; `Ctrl+C` stops a command that hangs. Run
`history | grep git` to see which git commands you typed today.

---

## Marks

| Task | Topic | Marks |
|---|---|---|
| 1 | Read what is there | 14 |
| 2 | Write with echo | 12 |
| 3 | Edit with nano | 12 |
| 4 | Copy | 12 |
| 5 | Move and rename | 10 |
| 6 | Delete | 14 |
| 7 | Search | 16 |
| 8 | Productivity and report | 10 |

About three quarters of the marks come from the text you pasted. The rest is checked against your real folder: that
`notes.txt` and `sensor.py` hold what you typed, that the backups, `archive` and `old_motor.c` are gone, that the
files the lab gave you are still there, that no `.pyc` is left, and that `py_files.txt` and `summary.txt` are right.
Run `python3 ~/file-operations-lab/tests/grade.py` to see every check.

## If something goes wrong

* **`No such file or directory`.** You are in the wrong folder or mistyped a name. Run `pwd`, then the task's
  **Start here** line, and use Tab to complete names.
* **You skipped Task 4 or 5 and a later task fails.** Run the catch-up box once, then carry on. A skipped task costs
  only its own pasted marks.
* **`cp` says `-r not specified; omitting directory`.** Copying a folder needs `cp -r`.
* **The `echo` line shows `>` at the start of the next line and nothing happens.** A quote was not closed. Press
  `Ctrl+C` and type the line again.
* **`notes.txt` lost lines you wanted.** Run steps 2.2, 2.3 and 2.4 again in that order: `>` starts the file afresh.
* **`rm -i` asked and you typed something other than `y`.** Nothing was deleted. Run it again and type `y`.
* **You deleted a file or folder of the lab that should still be there.** `rm` has no undo, but your clone does: from
  your **Start here** folder, run `git checkout -- <name>` with the name of what you lost (for example `src`):

  ```bash
  git checkout -- src
  ```

  It puts back the lab's version. Do not use it on `notes.txt` or `sensor.py`: it would also throw away what you
  typed there.
* **`grep` or `find` printed nothing.** Check that you are in `robot-controller`, that the quotes and the `.` are
  there, and that the word is spelled as shown.
* **nano says a directory does not exist.** You are in the wrong folder. Run the **Start here** line and open the
  file again. For `submission/outputs.txt` use the `nano ~/file-operations-lab/submission/outputs.txt` command of
  "How you hand in".
* **The grader says your `pwd` is not this clone.** The outputs in `submission/outputs.txt` were not produced in this
  folder. Redo the steps in your own clone and paste again.
* **Your listing shows a `.DS_Store` file or different permission letters.** That is normal; nothing is lost. Any other
  extra file is yours: move it away with `mv` or delete it, and list again.
* **You typed into the wrong file in nano.** `Ctrl+X`, then `N` throws the change away. If you already saved, open the
  file again and fix it.
* **Everything is a mess.** Copy your answers out first, then delete the clone:

  ```bash
  cp ~/file-operations-lab/submission/outputs.txt ~/outputs_backup.txt
  cd ~
  rm -r file-operations-lab
  ```

  Then clone again with the commands of "Start: get the lab" and redo the tasks (your pasted outputs must be produced
  in the new clone).
