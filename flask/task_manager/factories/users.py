from faker import Faker
import click
from flask.cli import with_appcontext
from models.users import UserRole


def create_user(username, first_name, last_name, email, password, role):
    from models.users import UserModel
    user = UserModel(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role=role
    )
    user.save()
    return user

@click.command()
@with_appcontext
def generateusers():
    fake = Faker()
    for _ in range(2):
        create_user(
            fake.unique.user_name(),
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.password(),
            UserRole.ADMIN.value
        )
    for _ in range(24):
        create_user(
            fake.unique.user_name(),
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.password(),
            UserRole.DEVELOPER.value
        )
    for _ in range(174):
        create_user(
            fake.unique.user_name(),
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.password(),
            UserRole.USER.value
        )
    click.echo("Users generated successfully.")

    
@click.command()
@with_appcontext
def deleteallusers():
    """
    Delete all rows from the users table.
    """
    from models.users import UserModel
    try:
        # Get all users and delete them one by one
        users = UserModel.query.all()
        for user in users:
            user.delete()
        click.echo("All users deleted successfully.")
    except Exception as e:
        UserModel.query.session.rollback()
        click.echo(f"Error deleting users: {str(e)}")