import nox


@nox.session
def docs(session):
    # docs dependencies
    session.install("sphinx", "sphinx-rtd-theme")
    # self
    session.install(".")
    # build docs
    session.run("sphinx-build", "-b", "html", "docs/", "html/")
