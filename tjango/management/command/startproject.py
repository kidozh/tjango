from ..command import BaseCommand
from ...utils.crypto import get_random_string
class Command(BaseCommand):

    def handle(self,**options):
        project_name = options.pop('name')
        target = options.pop('directory')
        # Create a random SECRET_KEY to put it in the main setting

        options['SECRET_KEY'] = get_random_string()

        super().handle('project',project_name,target)
        pass