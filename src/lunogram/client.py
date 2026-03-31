from random import randint

from .utils import seed
from .app import user, organization

class Lunogram:
    def __init__(self, api_key):
        self.user = user(api_key)
        self.organization = organization(api_key)

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
    
    client = Lunogram("Your API key here")

    > All sdk actions return a list with the api response on index 0, possible errors on index 1

    req = client.user.upsert(random_user())
    print(req[0])
    """

if __name__ == "__main__":
    main()