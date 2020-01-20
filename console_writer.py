import os
import datetime

DASHBOARD_WIDTH = 50


class WebPerformanceDashboard:
    def __init__(self):
        self.data = {}
        self.persisted_messages = []

    def add_persisted_message(self, msg: str):
        self.persisted_messages.append(msg)

    def yield_dashboard_lines(self):
        if self.data:
            yield "-" * DASHBOARD_WIDTH
            yield f"|" + " " * 15 + f"{self.data['url']}"
            yield "-" * DASHBOARD_WIDTH
            yield "|" + " " * 15 + "Current Dashboard"
            yield "-" * DASHBOARD_WIDTH
            max_key_length = max([len(k) for k in self.data])

            for k, v in self.data.items():

                if not k == "url":
                    additional_spaces_to_add = max_key_length - len(k)
                    yield f"| " + " " * additional_spaces_to_add + f" {k} -> {v}"

            yield "-" * DASHBOARD_WIDTH
            yield "|"+" " * 15 + "Persisted Messages"
            for msg in self.persisted_messages:
                yield f"| {msg}"
            yield "-" * DASHBOARD_WIDTH


class ConsoleWriter:
    def __init__(self):
        self.clear_screen()
        self.BOLD_LINE = "=" * DASHBOARD_WIDTH
        self.SINGLE_LINE = "-" * DASHBOARD_WIDTH
        self.WELCOME_MSG = "Website monitoring application"
        self.GOODBYE_MSG = "Come back soon!"
        self.web_performance_dashboards = []

    def add_dashboard(self, wp_dashboard: WebPerformanceDashboard):
        self.web_performance_dashboards.append(wp_dashboard)

    def clear_screen(self):
        os.system("cls -y")

    def greet(self):
        self.clear_screen()
        greeting = f"{self.BOLD_LINE}\n{self.WELCOME_MSG}\n{self.SINGLE_LINE}"
        print(greeting)

    def goodbye(self):
        print(f"{self.SINGLE_LINE}\n{self.GOODBYE_MSG}\n{self.BOLD_LINE}")

    def update(self, data: dict = None, dashboard: WebPerformanceDashboard = None):
        """
        """
        self.clear_screen()
        # self.print_persisted_msgs()

        dashboard.data = data

        # for line in dashboard.yield_dashboard_lines():
        #     print(line)

        multi_dashboard_length = DASHBOARD_WIDTH*len(self.web_performance_dashboards)

        print("-" * multi_dashboard_length)
        print("|"+" "*int(multi_dashboard_length/3) + "         Website Monitoring Application" + " "*(9+int(multi_dashboard_length/3))+"|")
        self.write_dashboards_to_console()

    def write_dashboards_to_console(self):

        dashboard_text_generators = [
            db.yield_dashboard_lines() for db in self.web_performance_dashboards
        ]

        for line_items in zip(*dashboard_text_generators):

            line_to_print = ""
            for line in line_items:
                line_to_print += self.pad_lines(line, DASHBOARD_WIDTH)

            if line_to_print[-1] == " ":
                line_to_print = line_to_print[:-1] + "|"

            print(line_to_print)

    def pad_lines(self, text_string, max_length):

        num_additional_chars = max_length - len(text_string)

        if num_additional_chars < 0:
            return text_string[:DASHBOARD_WIDTH-1]
        padded_string = text_string + " " * num_additional_chars
        return padded_string
