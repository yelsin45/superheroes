from app import app, db
from models import Hero, Power, HeroPower

with app.app_context():
    db.drop_all()
    db.create_all()

    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    hero3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    power1 = Power(
        name="super strength",
        description="Gives the wielder super-human strengths and can lift heavy objects easily."
    )
    power2 = Power(
        name="flight",
        description="Lets the wielder fly through the skies at supersonic speed."
    )
    power3 = Power(
        name="elasticity",
        description="Can stretch the human body to extreme lengths without injury."
    )

    db.session.add_all([hero1, hero2, hero3, power1, power2, power3])
    db.session.commit()

    hp1 = HeroPower(strength="Strong", hero_id=hero1.id, power_id=power2.id)
    hp2 = HeroPower(strength="Weak", hero_id=hero1.id, power_id=power3.id)
    hp3 = HeroPower(strength="Average", hero_id=hero2.id, power_id=power1.id)

    db.session.add_all([hp1, hp2, hp3])
    db.session.commit()

    print("Database seeded!")