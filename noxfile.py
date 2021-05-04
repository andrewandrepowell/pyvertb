import nox


@nox.session
def docs(session):
    session.install("sphinx")
    session.install(".")
    session.run("sphinx-build", "-b", "html", "docs/", "html/")
