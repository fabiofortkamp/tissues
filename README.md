# tissues

Inspired by [1], this project creates an executable `tissues` that does the following:

1. Run `ruff check --fix -eq` on the given argument (you run with `tissues FILES`), print the issues and count them;
2. Check that number agains the one recorded in the file `.ruff-issues`, and re-writes the file with the new number;
3. If the reported number is bigger or equal to than the one found previously, then exit with an status code of 1; otherwise, exit succesfully with code 0.

The intention is to be run within a pipeline in a legacy project as recommended by [1]; instead of spending too much time
fixing all linter issues, focus on steadily reducing the number of issues found. If after a code change, you found that you
introduced more issues, this is a problem. To be conservative, even keeping the number of issues constant
is considered bad.

Right now, this tool allows no configuration or customization. Future versions should address this.

If the `.ruff-issues` cannot be found, or its contents cannot be parsed into a positive integer, then `tissues` will report an error;
a second run will succeed (if you actually reduce the number of issues) because the first run creates the file.
You'll probably want to gitignore this file.

The file will not be written if `ruff` cannot be run for some reason (i.e. some
error other than lint violations).
## References

[1]: Wilson, Christie. Grokking Continuous Delivery. Shelter Island: Manning Publications, 2022.
