from random import choice, randint

class user:
    def firstname() -> str:
        names = [
            "James", "Mary", "John", "Patricia", "Robert",
            "Jennifer", "Michael", "Linda", "William", "Elizabeth",
            "David", "Barbara", "Richard", "Susan", "Joseph",
            "Jessica", "Thomas", "Sarah", "Charles", "Karen"
        ]

        return choice(names)
    
    def lastname() -> str:
        names = [
            "Smith", "Johnson", "Williams",
            "Brown", "Jones", "Garcia",
            "Miller", "Davis", "Rodriguez",
            "Martinez", "Hernandez", "Lopez",
            "Gonzalez", "Wilson", "Anderson"
        ]

        return choice(names)
    
    def email(firstname: str, lastname: str) -> str:
        domains = [
            "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", 
            "icloud.com", "aol.com", "protonmail.com", "live.com", 
            "msn.com", "mail.com", "zoho.com", "gmx.com", 
            "yandex.com", "fastmail.com", "hushmail.com"
        ]

        return f"{firstname[0].lower()}.{lastname.lower()}@{choice(domains)}"
    
    def phone() -> str:
        return f"+316{randint(10000000, 99999999)}"