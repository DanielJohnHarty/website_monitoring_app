import os

class ConsoleWriter:

    def __init__(self):
        self.clear_screen()
        self.LINE_LENGTH = 60
        self.BOLD_LINE = "=" * self.LINE_LENGTH
        self.SINGLE_LINE = "-" * self.LINE_LENGTH
        self.WELCOME_MSG = "Website monitoring application"
        self.GOODBYE_MSG = "Come back soon!"
        self.persisted_messages = []

    def clear_screen(self):
        os.system("cls -y")

    def greet(self):
        self.clear_screen()
        greeting = f"{self.BOLD_LINE}\n{self.WELCOME_MSG}\n{self.SINGLE_LINE}"
        print(greeting)
        self.persisted_messages.append(greeting)

    def goodbye(self):
        self.clear_screen()
        print(f"{self.SINGLE_LINE}\n{self.GOODBYE_MSG}\n{self.BOLD_LINE}")

    def write_update(self, update: str = None, to_persist: bool = False):
        """
        """
        self.clear_screen()
        for msg in self.persisted_messages:
            print(msg)

        update_to_persist = update and to_persist

        if update:
            print(update)

        if update_to_persist:
            self.persisted_messages.append(update)
