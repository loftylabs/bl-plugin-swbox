import random
from swapi import get_person, get_planet
from swapi.exceptions import ResourceDoesNotExist

from django.utils.safestring import mark_safe

from wagtail.wagtailcore import hooks


class SWPanel(object):
    order = 500

    def get_random_person(self):

        # Here's a hack, but fetching all people takes a long-ass time.
        # Checked recently and there were 87 people in the API database.
        person_id = random.randint(1, 87)
        try:
            person = get_person(person_id)
        except ResourceDoesNotExist:
            # Default to Luke!
            person = get_person(1)

        # Now get the person's planet
        planet = get_planet(person.homeworld.strip('/').split('/')[-1])
        person.homeworld = planet
        return person

    def render(self):
        random_person = self.get_random_person()

        return mark_safe("""
        <section class="panel summary nice-padding">
        <h2>Star Wars Panel!</h2>
        {person}<br>
        Homeworld: {planet}
        </section>
        """.format(
            person=random_person.name,
            planet=random_person.homeworld.name
        ))


@hooks.register('construct_homepage_panels')
def add_swpanel(request, panels):
    return panels.append(SWPanel())