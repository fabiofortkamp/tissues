# tissues

Inspired by [1], this project creates an executable `tissues` that coun`t` the `issues` in a project,
focusing on reducing the number of issues instead of tackling all of them.

The intention is to be run within a pipeline in a legacy project as recommended by [1]; instead of spending too much time
fixing all linter issues, focus on steadily reducing the number of issues found. If after a code change, you found that you
introduced more issues, this is a problem. To be conservative, even keeping the number of issues constant
is considered bad.

By running it with `tissues FILES`, the program does the following:

1. Run `ruff check --fix -eq` on the given argument (you run with `tissues FILES`), print the issues and count them;
2. Check that number agains the one recorded in the file `.ruff-issues`, and re-writes the file with the new number;
3. If the reported number is bigger or equal to than the one found previously, then exit with an status code of 1; otherwise, exit succesfully with code 0.

If the `.ruff-issues` cannot be found, or its contents cannot be parsed into a positive integer, then `tissues` will report an error;
a second run will succeed (if you actually reduce the number of issues) because the first run creates the file.
You'll probably want to gitignore this file.

The file will not be written if `ruff` cannot be run for some reason (i.e. some
error other than lint violations).

You can customize the command to be run with the `--command` flag (the above `ruff` command is the default if this flag is not set).
The argument to `tissues` will be appended to the command, and the control file will be named accordingly. The
number of issues reported is the number of lines in the standard output of the command.

## Installation
Run that in the desired environment:

```shell
pip install git+https://github.com/fabiofortkamp/tissues@main
```
## References

[1]: Wilson, Christie. Grokking Continuous Delivery. Shelter Island: Manning Publications, 2022.
