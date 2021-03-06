.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated and properly credited! As a developer or a user, you can contribute in different ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~
If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Submit Feedback
~~~~~~~~~~~~~~~~~~

Feedbacks are always welcome. If you, as a user, are proposing a new feature then please explain in detail regarding the desired feature, its functioning.


Get Started!
------------

Ready to contribute? Here's how to set up `rasta` for local development.

1. Fork the `rasta` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/rasta.git

3. Install your local copy into a virtual environment. Assuming you have conda installed, this is how you set up your fork for local development::

    $ conda create -n rasta_dev python=3.8
    $ cd rasta
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 rasta tests
    $ black rasta tests
    $ python setup.py test or pytest

   To get flake8, just pip install them into your conda environment. If you wish, you can add pre-commit hooks for both flake8 and black to make all formatting easier.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.