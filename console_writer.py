import os

DASHBOARD_WIDTH = 50


class WebPerformanceDashboard:
    def __init__(self):
        self.data = {}
        self.persisted_messages = []

    def yield_persisted_messages(self):
        yield "_" * DASHBOARD_WIDTH
        yield "Alert History"
        yield "_" * DASHBOARD_WIDTH

        if self.persisted_messages:
            for msg in self.persisted_messages:
                yield msg
        else:
            yield "..."

        yield "_" * DASHBOARD_WIDTH

    def add_persisted_message(self, msg: str):
        self.persisted_messages.append(msg)

    def yield_dashboard_body_lines(self):

        if self.data:
            yield self.data["url"]
            yield "_" * DASHBOARD_WIDTH
            yield "Timeframe (in minutes): " + self.data["timeframe"]
            yield "Report time: " + self.data["timestamp"]
            yield "_" * DASHBOARD_WIDTH
            for k, v in self.data.items():
                if k not in ["url", "timestamp", "timeframe"]:
                    yield f"{k} -> {v}"


class ConsoleWriter:
    def __init__(self):
        self.BOLD_LINE = "=" * 50
        self.SINGLE_LINE = "-" * 50
        self.WELCOME_MSG = "Website monitoring application"
        self.GOODBYE_MSG = "Come back soon!"
        self.APPLICATION_TITLE = "Web Monitoring Application"
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

    def yield_application_header_lines(self):

        multi_dashboard_length = len(self.web_performance_dashboards) * DASHBOARD_WIDTH

        title_length = len(self.APPLICATION_TITLE)

        yield "=" * multi_dashboard_length

        yield self.format_line(
            self.APPLICATION_TITLE,
            close_lines=True,
            pad_lines=True,
            max_length=multi_dashboard_length,
        )

        yield "=" * multi_dashboard_length

    def write_dashboards_to_console(self):

        self.clear_screen()

        # Print the header
        for header_line in self.yield_application_header_lines():
            print(header_line)

        # Print dashboard bodies
        for dashboard_body_line in self.yield_dashboard_body_lines():
            print(dashboard_body_line)

        # Print alert history
        for alert in self.yield_alert_history_lines():
            print(alert)

    def yield_alert_history_lines(self):

        dashboard_persisted_msg_generators = [
            db.yield_persisted_messages() for db in self.web_performance_dashboards
        ]

        for line_items in zip(*dashboard_persisted_msg_generators):
            multi_db_body_line = ""
            for line in line_items:
                multi_db_body_line += self.format_line(
                    line, close_lines=True, pad_lines=True
                )

            yield multi_db_body_line

    def yield_dashboard_body_lines(self):
        dashboard_body_generators = [
            db.yield_dashboard_body_lines() for db in self.web_performance_dashboards
        ]

        for line_items in zip(*dashboard_body_generators):

            multi_db_body_line = ""
            for line in line_items:
                multi_db_body_line += self.format_line(
                    line, close_lines=True, pad_lines=True
                )

            yield multi_db_body_line

    def truncate_lines(self, text_string, max_length):
        """
        """
        char_set = set(text_string)

        # Single char lines don't need final elipsis
        if len(char_set) == 1:
            result = text_string[:max_length]

        else:
            result = text_string[: max_length - 3] + "..."

        return result

    def pad_lines(self, text_string, max_len):
        line_length = len(text_string)

        pre_padding = int((max_len - line_length) / 2) * " "

        post_padding = (max_len - (line_length + len(pre_padding))) * " "

        text_string = pre_padding + text_string + post_padding

        return text_string

    def format_line(
        self,
        text_string: str,
        close_lines: bool,
        pad_lines: bool,
        max_length=DASHBOARD_WIDTH,
    ) -> str:
        """
        Takes a text input as a single dashboard line
        and formats.

        PARAMETERS: text_string, the line to be written as
                    part of the dashboard
                    close_lines: bool. Should string include
                    | characters at either end
                    pad_lines: bool, should lines match the width
                    of the DASHBOARD constant
        """

        # Keep 2 chars for the closing characters
        max_length = max_length - 2 if close_lines else max_length

        # Truncate if necessary
        if max_length <= len(text_string):
            text_string = self.truncate_lines(text_string, max_length)

        if pad_lines:
            text_string = self.pad_lines(text_string, max_length)

        if close_lines:
            text_string = "|" + text_string + "|"

        return text_string
