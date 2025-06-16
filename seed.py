from app import app, db, Hero, Power, HeroPower

with app.app_context():
    db.drop_all()
    db.create_all()

    heroes = [
        Hero(name="Kamala Khan", super_name="Ms. Marvel"),
        Hero(name="Doreen Green", super_name="Squirrel Girl"),
        Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
        Hero(name="Janet Van Dyne", super_name="The Wasp"),
        Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
        Hero(name="Carol Danvers", super_name="Captain Marvel"),
        Hero(name="Jean Grey", super_name="Dark Phoenix"),
        Hero(name="Ororo Munroe", super_name="Storm"),
        Hero(name="Kitty Pryde", super_name="Shadowcat"),
        Hero(name="Elektra Natchios", super_name="Elektra"),
    ]
    powers = [
        Power(name="super strength", description="gives the wielder super-human strengths and can lift heavy objects."),
        Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed easily."),
        Power(name="super human senses", description="allows the wielder to use her senses at a super-human level, detecting danger."),
        Power(name="elasticity", description="can stretch the human body to extreme lengths without injury."),
    ]
    db.session.add_all(heroes)
    db.session.add_all(powers)
    db.session.commit()

    db.session.add(HeroPower(strength="Strong", hero_id=1, power_id=2))
    db.session.add(HeroPower(strength="Average", hero_id=3, power_id=1))
    db.session.commit()
    print("Database seeded!")