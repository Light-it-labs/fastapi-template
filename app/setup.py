import setuptools

from app.commands.seed_users import SeedUsersCommand

setuptools.setup(
    name="API",
    packages=["app"],
    cmdclass={"seed_users": SeedUsersCommand},
)
