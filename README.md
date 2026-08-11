# File Operations Lab: Kestrel-1, Second Morning

Hands-on lab for Experiment 2 (Linux Terminal: File Operations and Productivity) of 26RA2308, Git for Software
Development and Collaboration. It is the second morning at the Kestrel-1 rover lab and the team's `robot-controller`
folder needs tidying before the field test: read files with `cat`, `head` and `tail`, write with `echo`, `>` and `>>`,
edit in `nano`, copy with `cp`, move with `mv`, delete with `rm`, and search with `grep` and `find`.

## Get started

```bash
cd ~
git clone https://github.com/qbit-glitch/26RA2308-gitlab-2-file-operations-lab.git file-operations-lab
cd file-operations-lab
cp submission/outputs.template.txt submission/outputs.txt
```

1. Read `ASSIGNMENT.md` (the handout) and do the eight tasks in order.
2. Paste each command's output into `submission/outputs.txt`, under the matching `--- N.M` line.
3. Check your work any time with:

```bash
python3 ~/file-operations-lab/tests/grade.py
```

The grader only reads files: it never runs anything you wrote. Needs `python3`, `nano` and `git`.
