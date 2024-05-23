Contributing
============

Bug reports, feature suggestions, and other contributions are greatly
appreciated!  pysat is a community-driven project and welcomes both feedback and
contributions.

Short version
-------------

* Submit bug reports, feature requests, and questions at
  [GitHub](https://github.com//KCollins/conjugate_map/issues)

* Make pull requests to the ``develop`` branch

Issues
------

Bug reports, questions, and feature requests should all be made as GitHub
Issues.  Templates are provided for each type of issue, to help you include
all the necessary information.

Questions
^^^^^^^^^

Not sure how something works?  Ask away!  The more information you provide, the
easier the question will be to answer.

Bug reports
^^^^^^^^^^^

When [reporting a bug](https://github.com//KCollins/conjugate_map/issues) please
include:

* Your operating system name and version

* Any details about your local setup that might be helpful in troubleshooting

* Detailed steps to reproduce the bug

Feature requests and feedback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The best way to send feedback is to file an
[issue](https://github.com/KCollins/conjugate_map/issues).

If you are proposing a new feature or a change in something that already exists:

* Explain in detail how it would work.

* Keep the scope as narrow as possible, to make it easier to implement.

* Remember that this is a volunteer-driven project, and that code contributions
  are welcome :)

Development
-----------

To set up `conjugate_map` for local development:

1. [Fork conjugate_map on GitHub](https://github.com/KCollins/conjugate_map/fork).

2. Clone your fork locally:

  ```
    git clone git@github.com:your_name_here/conjugate_map.git
  ```

3. Create a branch for local development:

  ```
    git checkout -b name-of-your-bugfix-or-feature
  ```

   Now you can make your changes locally.

   Tests for custom functions should be added to the appropriately named file
   once we develop unit tests.

4. When you're done making changes, check for pylint or flake8 for style:

   ```
   flake8 . --count --select=D,E,F,H,W --show-source --statistics
   ```

5. Update/add documentation in the docstrings.  Even if you don't think it's
   relevant, check to see if any existing examples have changed.

6. Add your name to the .zenodo.json file as an author

7. Commit your changes:
   ```
   git add .
   git commit -m "Brief description of your changes"

9. Once you are happy with the local changes, push to GitHub:
   ```
   git push origin name-of-your-bugfix-or-feature
   ```
   Note that each push will trigger the Continuous Integration workflow.

10. Submit a pull request through the GitHub website. Pull requests should be
    made to the ``develop`` branch.  Note that automated tests will be run on
    GitHub Actions, but these must be initialized by a project developer for
    first-time contributors.


Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code, just
make a pull request. Pull requests should be made to the ``develop`` branch.

For merging, you should:

1. Include an example for use
2. Add a note to ``CHANGELOG.md`` about the changes
3. Update the author list in ``zenodo.json`` and ``CITATION.cff``, if applicable
4. Ensure that all checks passed (current checks include GitHub Actions)

If you don't have all the necessary Python versions available locally or have
trouble building all the testing environments, you can rely on GitHub Actions to
run the tests for each change you add in the pull request. Because testing here
will delay tests by other developers, please ensure that the code passes all
tests on your local system first.


Project Style Guidelines
------------------------

In general, `conjugate=map` follows PEP8 and numpydoc guidelines.  Pylint
checks for style.  However, there are certain additional style elements that
have been adopted to ensure the project maintains a consistent coding style.
These include:

* Line breaks should occur before a binary operator (ignoring flake8 W503)
* Combine long strings using `join`
* Preferably break long lines on open parentheses rather than using `\`
* Use no more than 79 characters per line
* Several dependent packages have common nicknames, including:
  * `import datetime as dt`
  * `import numpy as np`
  * `import pandas as pd`
* When incrementing a timestamp, use `dt.timedelta` instead of `pd.DateOffset`
  when possible to reduce program runtime
* All classes should have `__repr__` and `__str__` functions
* Try to avoid creating a try/except statement where except passes
* Block and inline comments should use proper English grammar and punctuation
  with the exception of single sentences in a block, which may then omit the
  final period
* When casting is necessary, use `np.int64` and `np.float64` to ensure operating
  system agnosticism
