from random import randint

from .utils import seed
from .utils.reference import client as Reference
from .app import user, organization, push, sessions

class Lunogram:
    def __init__(self, api_key, project_id):
        # Every Client API endpoint is scoped to a project. The project UUID is
        # supplied once here and injected into every request path automatically;
        # callers never pass it per request.
        self.reference = Reference(project_id)
        self.user = user(api_key, self.reference)
        self.organization = organization(api_key, self.reference)
        self.push = push(api_key, self.reference)
        self.sessions = sessions(api_key, self.reference)

# Seeder data to generate a random user should you need it, this is mainly for testing purposes
def random_user():
    firstname = seed.user.firstname()
    lastname = seed.user.lastname()
    email = seed.user.email(firstname, lastname)
    phone = seed.user.phone()

    external_id = f"user_{randint(10000, 99999)}"
    anonymous_id = f"anon_{randint(1000, 9999)}"

    return {
        "identifier": [{
            "source": "default",
            "external_id": external_id,
            "metadata": None,
            "created_at": "2025-11-19T14:18:42.960Z",
            "updated_at": "2025-11-23T17:20:00.021Z"
        }],
        "external_id": external_id,
        "anonymous_id": anonymous_id,
        "email": email,
        "phone": phone,
        "timezone": "Europe/Amsterdam",
        "locale": "nl-NL",
        "data": {
            "first_name": firstname,
            "last_name": lastname,
            "has_completed_onboarding": True
        }
    }
def main() -> None:
    """
    Example use ->

    client = Lunogram("Your API key here", "your-project-uuid-here")

    > The project UUID is required and is injected into every Client API path,
    > e.g. /api/client/projects/<project_id>/users

    > All sdk actions return a list with the api response on index 0, possible errors on index 1

    req = client.user.upsert(random_user())
    print(req[0])
    """

if __name__ == "__main__":
    main()